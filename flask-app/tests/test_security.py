"""
Unit Tests for Security Module
"""

import unittest
from security import RateLimiter, AdminAuth, sanitize_input, validate_file_upload


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.limiter = RateLimiter()
    
    def test_rate_limit_allows_requests(self):
        """Test that requests within limit are allowed"""
        key = "test_user"
        
        # Should allow first 5 requests
        for i in range(5):
            self.assertTrue(
                self.limiter.is_allowed(key, max_requests=5, window_seconds=60)
            )
    
    def test_rate_limit_blocks_excess(self):
        """Test that excess requests are blocked"""
        key = "test_user"
        
        # Use up the limit
        for i in range(5):
            self.limiter.is_allowed(key, max_requests=5, window_seconds=60)
        
        # Next request should be blocked
        self.assertFalse(
            self.limiter.is_allowed(key, max_requests=5, window_seconds=60)
        )
    
    def test_rate_limit_different_keys(self):
        """Test that different keys have separate limits"""
        key1 = "user1"
        key2 = "user2"
        
        # Use up limit for key1
        for i in range(5):
            self.limiter.is_allowed(key1, max_requests=5, window_seconds=60)
        
        # key2 should still be allowed
        self.assertTrue(
            self.limiter.is_allowed(key2, max_requests=5, window_seconds=60)
        )


class TestAdminAuth(unittest.TestCase):
    """Test admin authentication"""
    
    def test_verify_valid_password(self):
        """Test verifying valid admin password"""
        self.assertTrue(AdminAuth.verify_password('admin', 'admin123'))
    
    def test_verify_invalid_password(self):
        """Test verifying invalid password"""
        self.assertFalse(AdminAuth.verify_password('admin', 'wrongpassword'))
    
    def test_verify_invalid_username(self):
        """Test verifying invalid username"""
        self.assertFalse(AdminAuth.verify_password('invalid', 'admin123'))


class TestInputSanitization(unittest.TestCase):
    """Test input sanitization"""
    
    def test_sanitize_normal_text(self):
        """Test sanitizing normal text"""
        text = "Hello World"
        result = sanitize_input(text)
        self.assertEqual(result, "Hello World")
    
    def test_sanitize_removes_null_bytes(self):
        """Test that null bytes are removed"""
        text = "Hello\x00World"
        result = sanitize_input(text)
        self.assertEqual(result, "HelloWorld")
    
    def test_sanitize_strips_whitespace(self):
        """Test that whitespace is stripped"""
        text = "  Hello World  "
        result = sanitize_input(text)
        self.assertEqual(result, "Hello World")
    
    def test_sanitize_truncates_long_text(self):
        """Test that long text is truncated"""
        text = "A" * 20000
        result = sanitize_input(text, max_length=100)
        self.assertEqual(len(result), 100)
    
    def test_sanitize_empty_text(self):
        """Test sanitizing empty text"""
        result = sanitize_input("")
        self.assertEqual(result, "")
    
    def test_sanitize_none(self):
        """Test sanitizing None"""
        result = sanitize_input(None)
        self.assertEqual(result, "")


class TestFileValidation(unittest.TestCase):
    """Test file upload validation"""
    
    def test_validate_allowed_extension(self):
        """Test validating allowed file extension"""
        allowed = {'png', 'jpg', 'jpeg'}
        self.assertTrue(validate_file_upload('image.png', allowed))
        self.assertTrue(validate_file_upload('photo.jpg', allowed))
    
    def test_validate_disallowed_extension(self):
        """Test rejecting disallowed extension"""
        allowed = {'png', 'jpg'}
        self.assertFalse(validate_file_upload('script.exe', allowed))
        self.assertFalse(validate_file_upload('doc.pdf', allowed))
    
    def test_validate_no_extension(self):
        """Test rejecting file without extension"""
        allowed = {'png', 'jpg'}
        self.assertFalse(validate_file_upload('noextension', allowed))
    
    def test_validate_empty_filename(self):
        """Test rejecting empty filename"""
        allowed = {'png', 'jpg'}
        self.assertFalse(validate_file_upload('', allowed))
    
    def test_validate_case_insensitive(self):
        """Test that validation is case insensitive"""
        allowed = {'png', 'jpg'}
        self.assertTrue(validate_file_upload('IMAGE.PNG', allowed))
        self.assertTrue(validate_file_upload('Photo.JPG', allowed))


if __name__ == '__main__':
    unittest.main()