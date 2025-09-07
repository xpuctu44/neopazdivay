#!/usr/bin/env python3
"""
Test script for Telegram bot IP checking functionality
"""
import sys
import os
sys.path.append('neopazdivay')

# Add the neopazdivay directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'neopazdivay'))

from datetime import datetime, timedelta, date
from app.database import get_db
from app.models import User, Attendance, AllowedIP, ScheduleEntry
from app.routers.telegram_bot import TelegramBot

def test_ip_checking_logic():
    """Test the IP checking logic for Telegram bot"""
    print("Testing Telegram bot IP checking logic...")

    # Create a mock bot instance
    bot = TelegramBot()

    # Get database session
    db = next(get_db())

    # Test 1: Check with no allowed IPs (should allow)
    print("\nTest 1: No allowed IPs configured")
    allowed_ips = db.query(AllowedIP).filter(AllowedIP.is_active == True).all()
    print(f"Active allowed IPs: {len(allowed_ips)}")

    # Create a test user
    test_user = db.query(User).filter(User.role == "employee").first()
    if not test_user:
        print("No test user found, creating one...")
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            password_hash="test_hash",
            role="employee",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    print(f"Test user ID: {test_user.id}")

    # Test the IP checking method
    is_allowed, message = bot._check_telegram_user_allowed(test_user.id)
    print(f"IP check result: {is_allowed}")
    print(f"Message: {message}")

    # Test 2: Create some allowed IPs and test again
    print("\nTest 2: With allowed IPs configured")
    if not allowed_ips:
        # Create test allowed IP
        test_ip = AllowedIP(
            ip_address="192.168.1.0",
            description="Test network",
            is_active=True
        )
        db.add(test_ip)
        db.commit()
        print("Created test allowed IP: 192.168.1.0")

    # Test again
    is_allowed, message = bot._check_telegram_user_allowed(test_user.id)
    print(f"IP check result with allowed IPs: {is_allowed}")
    print(f"Message: {message}")

    # Test 3: Create recent attendance for the user
    print("\nTest 3: With recent attendance")
    recent_attendance = Attendance(
        user_id=test_user.id,
        started_at=datetime.now() - timedelta(hours=2),
        work_date=date.today()
    )
    db.add(recent_attendance)
    db.commit()

    is_allowed, message = bot._check_telegram_user_allowed(test_user.id)
    print(f"IP check result with recent attendance: {is_allowed}")
    print(f"Message: {message}")

    # Clean up
    if recent_attendance:
        db.delete(recent_attendance)
    if test_user and test_user.email == "test@example.com":
        db.delete(test_user)
    db.commit()

    print("\n✅ IP checking logic test completed!")

if __name__ == "__main__":
    test_ip_checking_logic()