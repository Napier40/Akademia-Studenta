"""
Translation Service
Handles automated translation with caching using DeepL API
"""

import deepl
from functools import lru_cache
from flask import current_app
import logging

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Automated translation service using DeepL API
    Provides high-quality EN ↔ PL translation with caching
    """
    
    def __init__(self, api_key=None):
        """
        Initialize translator with API key
        
        Args:
            api_key: DeepL API key (optional, reads from config if not provided)
        """
        self.api_key = api_key or current_app.config.get('DEEPL_API_KEY')
        if self.api_key:
            try:
                self.translator = deepl.Translator(self.api_key)
                logger.info("DeepL translator initialized successfully")
            except Exception as e:
                self.translator = None
                logger.error(f"Failed to initialize DeepL translator: {e}")
        else:
            self.translator = None
            logger.warning("DeepL API key not configured - translation service disabled")
    
    @lru_cache(maxsize=1000)
    def translate(self, text, source_lang='EN', target_lang='PL'):
        """
        Translate text with caching
        
        Args:
            text: Text to translate
            source_lang: Source language code (EN, PL)
            target_lang: Target language code (EN, PL)
        
        Returns:
            Translated text or original if translation fails
        """
        if not self.translator:
            logger.warning("Translation service not available - returning original text")
            return text
        
        if not text or len(text.strip()) == 0:
            return text
        
        try:
            # DeepL requires EN-US for English target
            if target_lang.upper() == 'EN':
                target_lang = 'EN-US'
            
            result = self.translator.translate_text(
                text,
                source_lang=source_lang.upper(),
                target_lang=target_lang.upper()
            )
            
            logger.info(f"Translated ({source_lang} -> {target_lang}): {text[:50]}...")
            return result.text
            
        except deepl.DeepLException as e:
            logger.error(f"DeepL translation error: {e}")
            return text
        except Exception as e:
            logger.error(f"Unexpected translation error: {e}")
            return text
    
    def translate_html(self, html, source_lang='EN', target_lang='PL'):
        """
        Translate HTML content while preserving tags
        
        Args:
            html: HTML content to translate
            source_lang: Source language code
            target_lang: Target language code
        
        Returns:
            Translated HTML or original if translation fails
        """
        if not self.translator:
            return html
        
        try:
            if target_lang.upper() == 'EN':
                target_lang = 'EN-US'
            
            result = self.translator.translate_text(
                html,
                source_lang=source_lang.upper(),
                target_lang=target_lang.upper(),
                tag_handling='html'
            )
            
            logger.info(f"Translated HTML ({source_lang} -> {target_lang})")
            return result.text
            
        except deepl.DeepLException as e:
            logger.error(f"DeepL HTML translation error: {e}")
            return html
        except Exception as e:
            logger.error(f"Unexpected HTML translation error: {e}")
            return html
    
    def translate_batch(self, texts, source_lang='EN', target_lang='PL'):
        """
        Translate multiple texts at once (more efficient)
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
        
        Returns:
            List of translated texts
        """
        if not self.translator:
            return texts
        
        try:
            if target_lang.upper() == 'EN':
                target_lang = 'EN-US'
            
            results = self.translator.translate_text(
                texts,
                source_lang=source_lang.upper(),
                target_lang=target_lang.upper()
            )
            
            translated = [result.text for result in results]
            logger.info(f"Batch translated {len(texts)} texts ({source_lang} -> {target_lang})")
            return translated
            
        except deepl.DeepLException as e:
            logger.error(f"DeepL batch translation error: {e}")
            return texts
        except Exception as e:
            logger.error(f"Unexpected batch translation error: {e}")
            return texts
    
    def detect_language(self, text):
        """
        Detect language of text
        
        Args:
            text: Text to analyze
        
        Returns:
            Language code (EN, PL, etc.) or None if detection fails
        """
        if not self.translator:
            return None
        
        try:
            # Use first 100 characters for detection
            sample = text[:100]
            result = self.translator.translate_text(
                sample,
                target_lang='EN-US'
            )
            detected = result.detected_source_lang
            logger.info(f"Detected language: {detected}")
            return detected
            
        except deepl.DeepLException as e:
            logger.error(f"Language detection error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected detection error: {e}")
            return None
    
    def get_usage(self):
        """
        Get API usage statistics
        
        Returns:
            Dict with character count and limit, or None if unavailable
        """
        if not self.translator:
            return None
        
        try:
            usage = self.translator.get_usage()
            
            if usage.character.limit:
                percentage = (usage.character.count / usage.character.limit * 100)
            else:
                percentage = 0
            
            result = {
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'percentage_used': round(percentage, 2),
                'limit_reached': usage.character.limit_reached if hasattr(usage.character, 'limit_reached') else False
            }
            
            logger.info(f"API Usage: {result['character_count']}/{result['character_limit']} ({result['percentage_used']}%)")
            return result
            
        except deepl.DeepLException as e:
            logger.error(f"Usage check error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected usage check error: {e}")
            return None
    
    def is_available(self):
        """
        Check if translation service is available
        
        Returns:
            Boolean indicating if service is ready
        """
        return self.translator is not None


# Global instance
_translation_service = None


def get_translation_service():
    """
    Get or create translation service instance
    
    Returns:
        TranslationService instance
    """
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service


def translate_text(text, target_lang='PL', source_lang='EN'):
    """
    Convenience function for translating text
    
    Args:
        text: Text to translate
        target_lang: Target language code
        source_lang: Source language code
    
    Returns:
        Translated text
    """
    service = get_translation_service()
    return service.translate(text, source_lang, target_lang)


def translate_blog_post(post):
    """
    Auto-translate blog post to missing language
    
    Args:
        post: BlogPost model instance
    
    Returns:
        Boolean indicating if translation was performed
    """
    service = get_translation_service()
    
    if not service.is_available():
        logger.warning("Translation service not available")
        return False
    
    translated = False
    
    try:
        if post.customer_language == 'en':
            # Customer submitted in English, translate to Polish
            if not post.title_pl or post.title_pl == 'Pending Translation':
                post.title_pl = service.translate(post.title_en, 'EN', 'PL')
                translated = True
            
            if not post.content_pl or 'pending translation' in post.content_pl.lower():
                post.content_pl = service.translate_html(post.content_en, 'EN', 'PL')
                translated = True
            
            if post.excerpt_en and (not post.excerpt_pl or 'pending' in post.excerpt_pl.lower()):
                post.excerpt_pl = service.translate(post.excerpt_en, 'EN', 'PL')
                translated = True
            
            if post.category_en and not post.category_pl:
                post.category_pl = service.translate(post.category_en, 'EN', 'PL')
                translated = True
        
        elif post.customer_language == 'pl':
            # Customer submitted in Polish, translate to English
            if not post.title_en or post.title_en == 'Pending Translation':
                post.title_en = service.translate(post.title_pl, 'PL', 'EN')
                translated = True
            
            if not post.content_en or 'pending translation' in post.content_en.lower():
                post.content_en = service.translate_html(post.content_pl, 'PL', 'EN')
                translated = True
            
            if post.excerpt_pl and (not post.excerpt_en or 'pending' in post.excerpt_en.lower()):
                post.excerpt_en = service.translate(post.excerpt_pl, 'PL', 'EN')
                translated = True
            
            if post.category_pl and not post.category_en:
                post.category_en = service.translate(post.category_pl, 'PL', 'EN')
                translated = True
        
        if translated:
            logger.info(f"Successfully translated blog post: {post.id}")
        
        return translated
        
    except Exception as e:
        logger.error(f"Error translating blog post {post.id}: {e}")
        return False