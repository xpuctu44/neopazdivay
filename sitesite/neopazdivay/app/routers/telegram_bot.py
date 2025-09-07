import os
import asyncio
import secrets
import string
from datetime import datetime, timezone, timedelta, date
from typing import Dict, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User, Attendance, Store
from app.security import verify_password, hash_password


class TelegramBot:
    def __init__(self):
        self.application = None
        self.user_sessions: Dict[int, Dict] = {}  # telegram_id -> session data

    def _get_moscow_time(self) -> datetime:
        """Получает текущее время в московском часовом поясе (UTC+3)"""
        moscow_tz = timezone(timedelta(hours=3))
        return datetime.now(moscow_tz)

    def _get_db_session(self) -> Session:
        """Получает сессию базы данных"""
        return next(get_db())

    def _generate_web_credentials(self, name: str) -> tuple[str, str]:
        """Генерирует логин и пароль для веб-доступа"""
        # Генерируем логин на основе имени
        base_username = name.lower().replace(' ', '_').replace('-', '_')
        username = base_username

        # Проверяем уникальность логина
        db = self._get_db_session()
        counter = 1
        while db.query(User).filter(User.web_username == username).first():
            username = f"{base_username}_{counter}"
            counter += 1

        # Генерируем случайный пароль
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for _ in range(8))

        return username, password

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        telegram_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name

        # Проверяем, зарегистрирован ли пользователь
        db = self._get_db_session()
        user = db.query(User).filter(User.email == f"telegram_{telegram_id}@bot.local").first()

        if user:
            self.user_sessions[telegram_id] = {"user_id": user.id, "step": "main_menu"}
            await update.message.reply_text(
                f"Привет, {user.full_name or username}!\n\n"
                "Выберите действие:",
                reply_markup=self._get_main_menu_keyboard(user.id)
            )
        else:
            # Проверяем, есть ли пользователь с новыми учетными данными
            # Ищем по telegram_id в сессиях или по другим признакам
            # Для обратной совместимости проверяем все возможные форматы
            self.user_sessions[telegram_id] = {"step": "register"}
            await update.message.reply_text(
                "Добро пожаловать в систему учета рабочего времени!\n\n"
                "Для начала работы нужно зарегистрироваться.\n"
                "Введите ваше имя:"
            )

    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /register"""
        telegram_id = update.effective_user.id
        self.user_sessions[telegram_id] = {"step": "register"}
        await update.message.reply_text(
            "Регистрация в системе учета рабочего времени.\n"
            "Введите ваше имя:"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        telegram_id = update.effective_user.id
        text = update.message.text

        if telegram_id not in self.user_sessions:
            await update.message.reply_text("Используйте /start для начала работы")
            return

        session = self.user_sessions[telegram_id]
        step = session.get("step")

        if step == "register":
            await self._handle_registration(update, text)
        elif step == "main_menu":
            await self._handle_main_menu(update, text)
        else:
            await update.message.reply_text("Неизвестная команда. Используйте меню.")

    async def _handle_registration(self, update, name):
        """Обработка регистрации пользователя"""
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        db = self._get_db_session()

        # Генерируем учетные данные для веб-доступа
        web_username, web_password = self._generate_web_credentials(name)

        # Создаем пользователя
        user = User(
            email=f"{web_username}@web.local",  # Используем web_username как email
            full_name=name,
            password_hash=hash_password(web_password),  # Хэшируем сгенерированный пароль
            role="employee",
            is_active=True,
            web_username=web_username,
            web_password_plain=web_password  # Сохраняем пароль в открытом виде для показа в боте
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)

            self.user_sessions[telegram_id] = {"user_id": user.id, "step": "main_menu"}

            await update.message.reply_text(
                f"Регистрация завершена!\n\n"
                f"Добро пожаловать, {name}!\n\n"
                f"🔑 Ваши учетные данные для веб-версии:\n"
                f"Логин: {web_username}\n"
                f"Пароль: {web_password}\n\n"
                "Сохраните эти данные для входа на сайт.\n\n"
                "Выберите действие:",
                reply_markup=self._get_main_menu_keyboard(user.id)
            )
        except IntegrityError:
            db.rollback()
            await update.message.reply_text("Ошибка: такой логин уже существует. Попробуйте еще раз.")
        except Exception as e:
            db.rollback()
            await update.message.reply_text("Ошибка при регистрации. Попробуйте еще раз.")

    async def _handle_main_menu(self, update, text):
        """Обработка команд главного меню"""
        telegram_id = update.effective_user.id
        user_id = self.user_sessions[telegram_id]["user_id"]

        if text == "✅ Приход":
            await self._handle_checkin(update, user_id)
        elif text == "❌ Уход":
            await self._handle_checkout(update, user_id)
        elif text == "📊 Статус":
            await self._handle_status(update, user_id)
        else:
            await update.message.reply_text("Выберите действие из меню:")

    async def _handle_checkin(self, update, user_id):
        """Обработка прихода на работу"""
        db = self._get_db_session()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            await update.message.reply_text("Пользователь не найден")
            return

        now = self._get_moscow_time()
        today = now.date()

        # Проверяем, есть ли запись на сегодня
        existing = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today
        ).first()

        if existing:
            if existing.ended_at is None:
                # Уже есть активная смена на сегодня
                await update.message.reply_text(
                    f"У вас уже активная смена на сегодня!\n"
                    f"Начало: {existing.started_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                    "Используйте 'Я ушел' для завершения смены",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
                return
            else:
                # Есть завершенная смена, начинаем новую смену в тот же день
                existing.started_at = now
                existing.ended_at = None
                # Не сбрасываем hours, чтобы суммировать время
                db.add(existing)
                db.commit()
                await update.message.reply_text(
                    f"✅ Приход зафиксирован!\n"
                    f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n\n"
                    "Удачной работы!",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
                return

        # Создаем новую запись на сегодня
        record = Attendance(
            user_id=user_id,
            started_at=now,
            work_date=today
        )

        try:
            db.add(record)
            db.commit()
            await update.message.reply_text(
                f"✅ Приход зафиксирован!\n"
                f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n\n"
                "Удачной работы!",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
        except Exception as e:
            db.rollback()
            await update.message.reply_text("Ошибка при фиксации прихода")

    async def _handle_checkout(self, update, user_id):
        """Обработка ухода с работы"""
        db = self._get_db_session()
        now = self._get_moscow_time()
        today = now.date()

        # Находим активную смену на сегодня
        active = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today,
            Attendance.ended_at.is_(None)
        ).first()

        if not active:
            await update.message.reply_text(
                "У вас нет активной смены на сегодня\n\n"
                "Используйте 'Я пришел' для начала смены",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
            return

        # Завершаем смену
        active.ended_at = now

        # Рассчитываем время работы для этой смены
        started_at = active.started_at
        if started_at.tzinfo is None:
            # Если время naive, предполагаем что оно в московском времени
            moscow_tz = timezone(timedelta(hours=3))
            started_at = started_at.replace(tzinfo=moscow_tz)

        elapsed_seconds = (now - started_at).total_seconds()
        current_hours = round(elapsed_seconds / 3600.0, 2)

        # Суммируем с предыдущим временем
        if active.hours:
            active.hours += current_hours
        else:
            active.hours = current_hours

        try:
            db.add(active)
            db.commit()

            hours = int(active.hours)
            minutes = int((active.hours - hours) * 60)

            await update.message.reply_text(
                f"❌ Уход зафиксирован!\n"
                f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n"
                f"Отработано сегодня: {hours}ч {minutes}мин\n\n"
                "Хорошего отдыха!",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
        except Exception as e:
            db.rollback()
            await update.message.reply_text("Ошибка при фиксации ухода")

    async def _handle_status(self, update, user_id):
        """Показать текущий статус"""
        db = self._get_db_session()
        today = date.today()

        # Получаем активную смену на сегодня
        active = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today,
            Attendance.ended_at.is_(None)
        ).first()

        if active:
            now = self._get_moscow_time()
            started_at = active.started_at
            if started_at.tzinfo is None:
                # Если время naive, предполагаем что оно в московском времени
                moscow_tz = timezone(timedelta(hours=3))
                started_at = started_at.replace(tzinfo=moscow_tz)

            elapsed_seconds = (now - started_at).total_seconds()
            hours = int(elapsed_seconds / 3600)
            minutes = int((elapsed_seconds % 3600) / 60)

            # Показываем общее время за день
            total_hours = active.hours or 0
            total_h = int(total_hours)
            total_m = int((total_hours - total_h) * 60)

            await update.message.reply_text(
                f"📊 Текущий статус:\n\n"
                f"🟢 На работе\n"
                f"Начало смены: {active.started_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"Отработано в этой смене: {hours}ч {minutes}мин\n"
                f"Всего за сегодня: {total_h}ч {total_m}мин",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
        else:
            # Проверяем, есть ли завершенная смена на сегодня
            completed = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.work_date == today,
                Attendance.ended_at.isnot(None)
            ).first()

            if completed:
                total_hours = completed.hours or 0
                total_h = int(total_hours)
                total_m = int((total_hours - total_h) * 60)
                await update.message.reply_text(
                    f"📊 Текущий статус:\n\n"
                    f"🔴 Не на работе\n"
                    f"Отработано сегодня: {total_h}ч {total_m}мин\n\n"
                    "Используйте кнопку 'Я пришел' для начала новой смены",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
            else:
                await update.message.reply_text(
                    f"📊 Текущий статус:\n\n"
                    f"🔴 Не на работе\n\n"
                    "Используйте кнопку 'Я пришел' для начала смены",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )

    def _get_main_menu_keyboard(self, user_id=None):
        """Создает клавиатуру главного меню в зависимости от статуса пользователя"""
        if user_id:
            # Проверяем, есть ли активная смена на сегодня
            db = self._get_db_session()
            today = date.today()
            active = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.work_date == today,
                Attendance.ended_at.is_(None)
            ).first()

            if active:
                # Пользователь на работе - показываем "я ушел" и "статус"
                keyboard = [
                    [InlineKeyboardButton("❌ Я ушел", callback_data="checkout")],
                    [InlineKeyboardButton("📊 Статус", callback_data="status")],
                    [InlineKeyboardButton("🔑 Логин/Пароль", callback_data="show_credentials")]
                ]
            else:
                # Пользователь не на работе - показываем "я пришел" и "статус"
                keyboard = [
                    [InlineKeyboardButton("✅ Я пришел", callback_data="checkin")],
                    [InlineKeyboardButton("📊 Статус", callback_data="status")],
                    [InlineKeyboardButton("🔑 Логин/Пароль", callback_data="show_credentials")]
                ]
        else:
            # По умолчанию показываем "я пришел" и "статус"
            keyboard = [
                [InlineKeyboardButton("✅ Я пришел", callback_data="checkin")],
                [InlineKeyboardButton("📊 Статус", callback_data="status")],
                [InlineKeyboardButton("🔑 Логин/Пароль", callback_data="show_credentials")]
            ]

        return InlineKeyboardMarkup(keyboard)

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()

        telegram_id = query.from_user.id
        if telegram_id not in self.user_sessions:
            await query.edit_message_text("Сессия истекла. Используйте /start")
            return

        user_id = self.user_sessions[telegram_id]["user_id"]
        action = query.data

        if action == "checkin":
            await self._handle_checkin_via_callback(query, user_id)
        elif action == "checkout":
            await self._handle_checkout_via_callback(query, user_id)
        elif action == "status":
            await self._handle_status_via_callback(query, user_id)
        elif action == "show_credentials":
            await self._handle_show_credentials_via_callback(query, user_id)

    async def _handle_checkin_via_callback(self, query, user_id):
        """Обработка прихода через callback"""
        db = self._get_db_session()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            await query.edit_message_text("Пользователь не найден")
            return

        now = self._get_moscow_time()
        today = now.date()

        # Проверяем, есть ли запись на сегодня
        existing = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today
        ).first()

        if existing:
            if existing.ended_at is None:
                # Уже есть активная смена на сегодня
                await query.edit_message_text(
                    f"У вас уже активная смена на сегодня!\n"
                    f"Начало: {existing.started_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                    "Используйте 'Я ушел' для завершения смены\n\n"
                    "Выберите действие:",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
                return
            else:
                # Есть завершенная смена, начинаем новую смену в тот же день
                existing.started_at = now
                existing.ended_at = None
                # Не сбрасываем hours, чтобы суммировать время
                db.add(existing)
                db.commit()
                try:
                    await query.edit_message_text(
                        f"✅ Приход зафиксирован!\n"
                        f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n\n"
                        "Удачной работы!\n\n"
                        "Выберите действие:",
                        reply_markup=self._get_main_menu_keyboard(user_id)
                    )
                except Exception as e:
                    if "Message is not modified" in str(e):
                        await query.answer("Приход уже зафиксирован")
                    else:
                        await query.answer("Ошибка при фиксации прихода")
                return

        # Создаем новую запись на сегодня
        record = Attendance(
            user_id=user_id,
            started_at=now,
            work_date=today
        )

        try:
            db.add(record)
            db.commit()
            try:
                await query.edit_message_text(
                    f"✅ Приход зафиксирован!\n"
                    f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n\n"
                    "Удачной работы!\n\n"
                    "Выберите действие:",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
            except Exception as e:
                if "Message is not modified" in str(e):
                    await query.answer("Приход уже зафиксирован")
                else:
                    await query.answer("Ошибка при фиксации прихода")
        except Exception as e:
            db.rollback()
            await query.answer("Ошибка при фиксации прихода")

    async def _handle_checkout_via_callback(self, query, user_id):
        """Обработка ухода через callback"""
        db = self._get_db_session()
        now = self._get_moscow_time()
        today = now.date()

        # Находим активную смену на сегодня
        active = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today,
            Attendance.ended_at.is_(None)
        ).first()

        if not active:
            await query.edit_message_text(
                "У вас нет активной смены на сегодня\n\n"
                "Используйте 'Я пришел' для начала смены\n\n"
                "Выберите действие:",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
            return

        # Завершаем смену
        active.ended_at = now

        # Рассчитываем время работы для этой смены
        started_at = active.started_at
        if started_at.tzinfo is None:
            # Если время naive, предполагаем что оно в московском времени
            moscow_tz = timezone(timedelta(hours=3))
            started_at = started_at.replace(tzinfo=moscow_tz)

        elapsed_seconds = (now - started_at).total_seconds()
        current_hours = round(elapsed_seconds / 3600.0, 2)

        # Суммируем с предыдущим временем
        if active.hours:
            active.hours += current_hours
        else:
            active.hours = current_hours

        try:
            db.add(active)
            db.commit()

            hours = int(active.hours)
            minutes = int((active.hours - hours) * 60)

            try:
                await query.edit_message_text(
                    f"❌ Уход зафиксирован!\n"
                    f"Время: {now.strftime('%d.%m.%Y %H:%M')}\n"
                    f"Отработано сегодня: {hours}ч {minutes}мин\n\n"
                    "Хорошего отдыха!\n\n"
                    "Выберите действие:",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
            except Exception as e:
                if "Message is not modified" in str(e):
                    await query.answer("Уход уже зафиксирован")
                else:
                    await query.answer("Ошибка при фиксации ухода")
        except Exception as e:
            db.rollback()
            await query.answer("Ошибка при фиксации ухода")

    async def _handle_status_via_callback(self, query, user_id):
        """Показать статус через callback"""
        db = self._get_db_session()
        today = date.today()

        # Получаем активную смену на сегодня
        active = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.work_date == today,
            Attendance.ended_at.is_(None)
        ).first()

        if active:
            now = self._get_moscow_time()
            started_at = active.started_at
            if started_at.tzinfo is None:
                # Если время naive, предполагаем что оно в московском времени
                moscow_tz = timezone(timedelta(hours=3))
                started_at = started_at.replace(tzinfo=moscow_tz)

            elapsed_seconds = (now - started_at).total_seconds()
            hours = int(elapsed_seconds / 3600)
            minutes = int((elapsed_seconds % 3600) / 60)

            # Показываем общее время за день
            total_hours = active.hours or 0
            total_h = int(total_hours)
            total_m = int((total_hours - total_h) * 60)

            try:
                await query.edit_message_text(
                    f"📊 Текущий статус:\n\n"
                    f"🟢 На работе\n"
                    f"Начало смены: {active.started_at.strftime('%d.%m.%Y %H:%M')}\n"
                    f"Отработано в этой смене: {hours}ч {minutes}мин\n"
                    f"Всего за сегодня: {total_h}ч {total_m}мин\n\n"
                    "Выберите действие:",
                    reply_markup=self._get_main_menu_keyboard(user_id)
                )
            except Exception as e:
                # Если сообщение не изменилось, просто отвечаем
                if "Message is not modified" in str(e):
                    await query.answer("Статус не изменился")
                else:
                    await query.answer("Ошибка при обновлении статуса")
        else:
            # Проверяем, есть ли завершенная смена на сегодня
            completed = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.work_date == today,
                Attendance.ended_at.isnot(None)
            ).first()

            if completed:
                total_hours = completed.hours or 0
                total_h = int(total_hours)
                total_m = int((total_hours - total_h) * 60)
                try:
                    await query.edit_message_text(
                        f"📊 Текущий статус:\n\n"
                        f"🔴 Не на работе\n"
                        f"Отработано сегодня: {total_h}ч {total_m}мин\n\n"
                        "Используйте кнопку 'Я пришел' для начала новой смены\n\n"
                        "Выберите действие:",
                        reply_markup=self._get_main_menu_keyboard(user_id)
                    )
                except Exception as e:
                    if "Message is not modified" in str(e):
                        await query.answer("Статус не изменился")
                    else:
                        await query.answer("Ошибка при обновлении статуса")
            else:
                try:
                    await query.edit_message_text(
                        f"📊 Текущий статус:\n\n"
                        f"🔴 Не на работе\n\n"
                        "Используйте кнопку 'Я пришел' для начала смены\n\n"
                        "Выберите действие:",
                        reply_markup=self._get_main_menu_keyboard(user_id)
                    )
                except Exception as e:
                    if "Message is not modified" in str(e):
                        await query.answer("Статус не изменился")
                    else:
                        await query.answer("Ошибка при обновлении статуса")

    async def _handle_show_credentials_via_callback(self, query, user_id):
        """Показать логин и пароль для веб-версии через callback"""
        db = self._get_db_session()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            await query.edit_message_text("Пользователь не найден")
            return

        # Используем сохраненные учетные данные
        if not user.web_username or not user.web_password_plain:
            await query.edit_message_text(
                "Учетные данные для веб-версии не найдены.\n"
                "Возможно, аккаунт был создан до обновления системы.\n\n"
                "Выберите действие:",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
            return

        try:
            await query.edit_message_text(
                f"🔑 Ваши учетные данные для веб-версии:\n\n"
                f"Логин: {user.web_username}\n"
                f"Пароль: {user.web_password_plain}\n\n"
                "Используйте эти данные для входа на сайт.\n\n"
                "Выберите действие:",
                reply_markup=self._get_main_menu_keyboard(user_id)
            )
        except Exception as e:
            if "Message is not modified" in str(e):
                await query.answer("Учетные данные уже показаны")
            else:
                await query.answer("Ошибка при показе учетных данных")

    def setup_bot(self, token: str):
        """Настройка и запуск бота"""
        self.application = Application.builder().token(token).build()

        # Добавляем обработчики
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("register", self.register_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

    async def run_bot(self):
        """Запуск бота"""
        if self.application:
            await self.application.run_polling()
        else:
            raise ValueError("Bot not set up. Call setup_bot() first")

    def run_sync(self):
        """Синхронный запуск бота"""
        if self.application:
            self.application.run_polling()
        else:
            raise ValueError("Bot not set up. Call setup_bot() first")


# Глобальный экземпляр бота
telegram_bot = TelegramBot()