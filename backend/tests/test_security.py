"""
Unit tests for security module.
Tests password hashing and verification functions.
"""
import pytest
from app import security


def test_hash_password():
    """Test that password hashing works"""
    password = "test_password_123"
    hashed = security.hash_password(password)
    
    # Hash should be different from original password
    assert hashed != password
    # Hash should be a string
    assert isinstance(hashed, str)
    # Hash should not be empty
    assert len(hashed) > 0


def test_hash_password_different_hashes():
    """Test that same password produces different hashes (due to salt)"""
    password = "same_password"
    hash1 = security.hash_password(password)
    hash2 = security.hash_password(password)
    
    # Hashes should be different due to different salts
    assert hash1 != hash2


def test_verify_password_correct():
    """Test that correct password verification works"""
    password = "correct_password"
    hashed = security.hash_password(password)
    
    # Verification should succeed with correct password
    assert security.verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test that incorrect password verification fails"""
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed = security.hash_password(password)
    
    # Verification should fail with wrong password
    assert security.verify_password(wrong_password, hashed) is False


def test_verify_password_empty():
    """Test password verification with empty password"""
    password = "test123"
    hashed = security.hash_password(password)
    
    # Empty password should not match
    assert security.verify_password("", hashed) is False


def test_hash_password_special_characters():
    """Test hashing passwords with special characters"""
    password = "p@ssw0rd!#$%^&*()"
    hashed = security.hash_password(password)
    
    # Should hash successfully
    assert isinstance(hashed, str)
    # Should verify correctly
    assert security.verify_password(password, hashed) is True


def test_hash_password_unicode():
    """Test hashing passwords with unicode characters"""
    password = "пароль密码🔒"
    hashed = security.hash_password(password)
    
    # Should hash successfully
    assert isinstance(hashed, str)
    # Should verify correctly
    assert security.verify_password(password, hashed) is True


def test_verify_password_case_sensitive():
    """Test that password verification is case-sensitive"""
    password = "TestPassword"
    hashed = security.hash_password(password)
    
    # Different case should not match
    assert security.verify_password("testpassword", hashed) is False
    assert security.verify_password("TESTPASSWORD", hashed) is False
    # Exact match should work
    assert security.verify_password("TestPassword", hashed) is True
