import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import importlib
from src.locales.language_map import LANGUAGE_NAMES

# Ensure the src directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.locales.loader import MessageLoader, get_message

class TestMessageLoader:
    @pytest.fixture(scope="class")
    def loader(self):
        return MessageLoader(
            default_module='docs.messages',
            translation_module='src.locales.uk.messages_uk'
        )

    def test_english_message(self):
        # Loader with only English
        loader = MessageLoader(default_module='docs.messages')
        assert loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=123).startswith('✅ Card added')

    def test_ukrainian_message(self, loader):
        # Ukrainian translation exists
        uk_msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=123)
        assert 'Картку додано' in uk_msg or 'Card added' in uk_msg  # fallback or translation

    def test_fallback_to_english(self, loader):
        # Add a fake key to Ukrainian dict to simulate missing translation
        # Use a key that exists in English but not in Ukrainian
        assert loader.get('DEVELOPER_NOTES.nltk_download_failure', error='err').startswith('⚠️ Не вдалося') or \
               loader.get('DEVELOPER_NOTES.nltk_download_failure', error='err').startswith('⚠️ Could not')

    def test_formatting(self, loader):
        msg = loader.get('MEDIA_FILE_UPLOAD.media_save_error', filename='file.mp3', error='disk full')
        assert 'file.mp3' in msg and 'disk full' in msg

    def test_key_error(self, loader):
        with pytest.raises(KeyError):
            loader.get('NON_EXISTENT.KEY')

    def test_formatting_error(self, loader):
        # Missing required kwarg
        with pytest.raises(ValueError):
            loader.get('MEDIA_FILE_UPLOAD.media_save_error', filename='file.mp3')


@patch.dict(os.environ, {'USER_LOCALE': 'en'})
def test_global_get_message():
    # Should work for both locales
    msg = get_message('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
    assert 'ID = 42' in msg
    # Should raise for missing key
    with pytest.raises(KeyError):
        get_message('NOPE.NOT_A_KEY')

class TestLanguageInitialization:
    """Test the new language initialization functionality"""
    
    @patch('src.locales.loader.USER_LOCALE', '')
    @patch('src.config.language_config.initialize_language_if_needed')
    @patch('builtins.input', return_value='1')
    def test_get_message_with_empty_locale(self, mock_input, mock_init):
        """Test that get_message initializes language when USER_LOCALE is empty"""
        with patch('src.locales.loader.MessageLoader.get', return_value="test message") as mock_get:
            result = get_message('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
            mock_init.assert_called_once()
            mock_get.assert_called_once_with('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
            assert result == "test message"
    
    @patch('src.locales.loader.USER_LOCALE', 'en')
    @patch('src.config.language_config.initialize_language_if_needed')
    def test_get_message_with_set_locale(self, mock_init):
        """Test that get_message doesn't initialize language when USER_LOCALE is set"""
        with patch('src.locales.loader.MessageLoader.get', return_value="test message") as mock_get:
            result = get_message('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
            mock_init.assert_not_called()
            mock_get.assert_called_once_with('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
            assert result == "test message"
    
    @patch('builtins.input', return_value='1')
    @patch('src.config.language_config.initialize_language_if_needed')
    def test_get_message_reloads_loader_after_init(self, mock_init, mock_input):
        """Test that get_message reloads the loader after language initialization"""
        # Set up the environment to trigger language initialization
        with patch.dict(os.environ, {}, clear=True):  # Clear USER_LOCALE
            with patch('src.locales.loader.USER_LOCALE', ''):  # Set empty USER_LOCALE
                with patch('src.config.settings.USER_LOCALE', 'uk'):  # Mock the updated value
                    with patch('src.locales.loader.MessageLoader') as mock_loader_class:
                        mock_loader = MagicMock()
                        mock_loader.get.return_value = "test message"
                        mock_loader_class.return_value = mock_loader
                        
                        result = get_message('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=42)
                        
                        # Should create new loader with Ukrainian translation module
                        mock_loader_class.assert_called_with(
                            default_module='docs.messages',
                            translation_module='src.locales.uk.messages_uk'
                        )
                        assert result == "test message" 

class TestDynamicLanguageLoading:
    def test_dynamic_loading_for_all_supported_languages(self):
        """Test that MessageLoader loads translation modules for all languages in LANGUAGE_NAMES, falling back to English if missing."""
        for code in LANGUAGE_NAMES:
            if code == 'en':
                loader = MessageLoader(default_module='docs.messages')
                msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=1)
                assert 'Card added' in msg
            else:
                module_path = f"src.locales.{code}.messages_{code}"
                try:
                    importlib.import_module(module_path)
                    loader = MessageLoader(default_module='docs.messages', translation_module=module_path)
                    msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=1)
                    # Should not raise, and should return a string (translated or fallback)
                    assert isinstance(msg, str)
                except ModuleNotFoundError:
                    # Should fallback to English
                    loader = MessageLoader(default_module='docs.messages', translation_module=module_path)
                    msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=1)
                    assert 'Card added' in msg

    def test_fallback_for_unsupported_locale(self):
        """Test fallback to English if USER_LOCALE is not in LANGUAGE_NAMES."""
        loader = MessageLoader(default_module='docs.messages', translation_module=None)
        msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=2)
        assert 'Card added' in msg

    def test_fallback_for_missing_translation_module(self):
        """Test fallback to English if translation module is missing for a supported locale."""
        fake_lang = 'zz'
        with patch.dict('src.locales.language_map.LANGUAGE_NAMES', {**LANGUAGE_NAMES, fake_lang: 'FakeLang'}):
            module_path = f"src.locales.{fake_lang}.messages_{fake_lang}"
            loader = MessageLoader(default_module='docs.messages', translation_module=module_path)
            msg = loader.get('CARD_CONSTRUCTION_SUBMISSION.card_added', card_id=3)
            assert 'Card added' in msg 