"""
Unit Tests for Translation Service
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from translation_service import TranslationService, translate_text, translate_blog_post


class TestTranslationService(unittest.TestCase):
    """Test translation service functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = TranslationService(api_key="test_key")
    
    @patch('translation_service.deepl.Translator')
    def test_service_initialization_with_key(self, mock_translator):
        """Test service initializes with API key"""
        service = TranslationService(api_key="test_key")
        mock_translator.assert_called_once_with("test_key")
    
    def test_service_initialization_without_key(self):
        """Test service handles missing API key"""
        service = TranslationService(api_key=None)
        self.assertIsNone(service.translator)
    
    @patch('translation_service.deepl.Translator')
    def test_translate_returns_original_without_translator(self, mock_translator):
        """Test translate returns original text when translator unavailable"""
        service = TranslationService(api_key=None)
        result = service.translate("Hello", "EN", "PL")
        self.assertEqual(result, "Hello")
    
    def test_translate_empty_text(self):
        """Test translating empty text"""
        result = self.service.translate("", "EN", "PL")
        self.assertEqual(result, "")
    
    def test_translate_none(self):
        """Test translating None"""
        result = self.service.translate(None, "EN", "PL")
        self.assertIsNone(result)
    
    @patch('translation_service.deepl.Translator')
    def test_translate_handles_errors(self, mock_translator):
        """Test translate handles API errors gracefully"""
        mock_instance = Mock()
        mock_instance.translate_text.side_effect = Exception("API Error")
        mock_translator.return_value = mock_instance
        
        service = TranslationService(api_key="test_key")
        result = service.translate("Hello", "EN", "PL")
        
        # Should return original text on error
        self.assertEqual(result, "Hello")
    
    def test_is_available_with_translator(self):
        """Test is_available returns True when translator exists"""
        service = TranslationService(api_key="test_key")
        # Mock the translator
        service.translator = Mock()
        self.assertTrue(service.is_available())
    
    def test_is_available_without_translator(self):
        """Test is_available returns False when translator missing"""
        service = TranslationService(api_key=None)
        self.assertFalse(service.is_available())


class TestTranslateBlogPost(unittest.TestCase):
    """Test blog post translation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_post = Mock()
        self.mock_post.id = 1
        self.mock_post.customer_language = "en"
        self.mock_post.title_en = "English Title"
        self.mock_post.title_pl = ""
        self.mock_post.content_en = "English Content"
        self.mock_post.content_pl = ""
        self.mock_post.category_en = "Category"
        self.mock_post.category_pl = ""
        self.mock_post.excerpt_en = "Excerpt"
        self.mock_post.excerpt_pl = ""
    
    @patch('translation_service.get_translation_service')
    def test_translate_blog_post_en_to_pl(self, mock_get_service):
        """Test translating English post to Polish"""
        mock_service = Mock()
        mock_service.is_available.return_value = True
        mock_service.translate.return_value = "Translated"
        mock_service.translate_html.return_value = "Translated HTML"
        mock_get_service.return_value = mock_service
        
        result = translate_blog_post(self.mock_post)
        
        self.assertTrue(result)
        self.assertEqual(self.mock_post.title_pl, "Translated")
        self.assertEqual(self.mock_post.content_pl, "Translated HTML")
    
    @patch('translation_service.get_translation_service')
    def test_translate_blog_post_service_unavailable(self, mock_get_service):
        """Test translation when service unavailable"""
        mock_service = Mock()
        mock_service.is_available.return_value = False
        mock_get_service.return_value = mock_service
        
        result = translate_blog_post(self.mock_post)
        
        self.assertFalse(result)
    
    @patch('translation_service.get_translation_service')
    def test_translate_blog_post_pl_to_en(self, mock_get_service):
        """Test translating Polish post to English"""
        self.mock_post.customer_language = "pl"
        self.mock_post.title_pl = "Polish Title"
        self.mock_post.title_en = ""
        self.mock_post.content_pl = "Polish Content"
        self.mock_post.content_en = ""
        
        mock_service = Mock()
        mock_service.is_available.return_value = True
        mock_service.translate.return_value = "Translated"
        mock_service.translate_html.return_value = "Translated HTML"
        mock_get_service.return_value = mock_service
        
        result = translate_blog_post(self.mock_post)
        
        self.assertTrue(result)
        self.assertEqual(self.mock_post.title_en, "Translated")
        self.assertEqual(self.mock_post.content_en, "Translated HTML")
    
    @patch('translation_service.get_translation_service')
    def test_translate_blog_post_handles_errors(self, mock_get_service):
        """Test translation handles errors gracefully"""
        mock_service = Mock()
        mock_service.is_available.return_value = True
        mock_service.translate.side_effect = Exception("Translation error")
        mock_get_service.return_value = mock_service
        
        result = translate_blog_post(self.mock_post)
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()