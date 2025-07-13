import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from src.config.language_config import (
    get_language_choice,
    save_language_to_env,
    configure_language,
    should_prompt_for_language,
    initialize_language_if_needed
)

class TestLanguageConfig:
    
    @pytest.fixture
    def temp_env_file(self):
        """Create a temporary .env file for testing"""
        temp_dir = tempfile.mkdtemp()
        env_file = os.path.join(temp_dir, '.env')
        yield env_file
        shutil.rmtree(temp_dir)
    
    @patch('builtins.input')
    def test_get_language_choice_english(self, mock_input):
        """Test language choice for English"""
        mock_input.return_value = '1'
        result = get_language_choice()
        assert result == 'en'
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_get_language_choice_ukrainian(self, mock_input):
        """Test language choice for Ukrainian"""
        mock_input.return_value = '2'
        result = get_language_choice()
        assert result == 'uk'
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_language_choice_invalid_then_valid(self, mock_print, mock_input):
        """Test language choice with invalid input followed by valid input"""
        mock_input.side_effect = ['3', '1']  # Invalid, then valid
        result = get_language_choice()
        assert result == 'en'
        assert mock_input.call_count == 2
        mock_print.assert_called_once()
    
    def test_save_language_to_env_new_file(self, temp_env_file):
        """Test saving language to a new .env file"""
        save_language_to_env('uk', temp_env_file)
        
        # Check that the file was created with correct content
        assert os.path.exists(temp_env_file)
        with open(temp_env_file, 'r') as f:
            content = f.read()
            assert 'USER_LOCALE=uk' in content
    
    def test_save_language_to_env_existing_file(self, temp_env_file):
        """Test saving language to an existing .env file"""
        # Create existing .env file with some content
        with open(temp_env_file, 'w') as f:
            f.write('EXISTING_VAR=value\nUSER_LOCALE=en\nOTHER_VAR=other')
        
        save_language_to_env('uk', temp_env_file)
        
        # Check that USER_LOCALE was updated
        with open(temp_env_file, 'r') as f:
            content = f.read()
            assert 'USER_LOCALE=uk' in content
            assert 'USER_LOCALE=en' not in content
            assert 'EXISTING_VAR=value' in content
            assert 'OTHER_VAR=other' in content
    
    @patch('src.config.language_config.get_language_choice')
    @patch('src.config.language_config.save_language_to_env')
    @patch('builtins.print')
    @patch('subprocess.run')
    def test_configure_language(self, mock_run, mock_print, mock_save, mock_choice):
        """Test configure_language function"""
        mock_choice.return_value = 'uk'
        import pytest
        with pytest.raises(SystemExit):
            configure_language()
        mock_choice.assert_called_once()
        mock_save.assert_called_once_with('uk')  # Uses default .env parameter
        mock_print.assert_any_call("✅ Language set to: Українська")
        mock_print.assert_any_call("🔄 Restarting to apply language change...")
        mock_run.assert_called_once()
    
    @patch.dict(os.environ, {'USER_LOCALE': 'en'})
    def test_should_prompt_for_language_false(self):
        """Test should_prompt_for_language when USER_LOCALE is set"""
        assert not should_prompt_for_language()
    
    @patch.dict(os.environ, {'USER_LOCALE': ''})
    def test_should_prompt_for_language_empty(self):
        """Test should_prompt_for_language when USER_LOCALE is empty"""
        assert should_prompt_for_language()
    
    @patch.dict(os.environ, {'USER_LOCALE': '   '})
    def test_should_prompt_for_language_whitespace(self):
        """Test should_prompt_for_language when USER_LOCALE is whitespace"""
        assert should_prompt_for_language()
    
    @patch.dict(os.environ, {}, clear=True)
    def test_should_prompt_for_language_not_set(self):
        """Test should_prompt_for_language when USER_LOCALE is not set"""
        assert should_prompt_for_language()
    
    @patch('src.config.language_config.should_prompt_for_language')
    @patch('src.config.language_config.configure_language')
    @patch('dotenv.load_dotenv')
    def test_initialize_language_if_needed_prompt(self, mock_load_dotenv, mock_configure, mock_should_prompt):
        """Test initialize_language_if_needed when prompt is needed"""
        mock_should_prompt.return_value = True
        
        initialize_language_if_needed()
        
        mock_configure.assert_called_once()
        mock_load_dotenv.assert_called_once_with(override=True)
    
    @patch('src.config.language_config.should_prompt_for_language')
    @patch('src.config.language_config.configure_language')
    @patch('dotenv.load_dotenv')
    def test_initialize_language_if_needed_no_prompt(self, mock_load_dotenv, mock_configure, mock_should_prompt):
        """Test initialize_language_if_needed when no prompt is needed"""
        mock_should_prompt.return_value = False
        
        initialize_language_if_needed()
        
        mock_configure.assert_not_called()
        mock_load_dotenv.assert_not_called() 