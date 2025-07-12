import pytest
import sys
from unittest.mock import patch, MagicMock
from src.cli.args import parse_arguments, handle_cli_arguments

class TestCLIArgs:
    
    @patch('sys.argv', ['generate_card.py'])
    def test_parse_arguments_no_args(self):
        """Test parsing arguments with no command line arguments"""
        args = parse_arguments()
        assert not args.set_language
    
    @patch('sys.argv', ['generate_card.py', '--set-language'])
    def test_parse_arguments_set_language(self):
        """Test parsing arguments with --set-language flag"""
        args = parse_arguments()
        assert args.set_language
    
    @patch('sys.argv', ['generate_card.py', '--help'])
    def test_parse_arguments_help(self):
        """Test that help argument is handled correctly"""
        # Help should raise SystemExit
        with pytest.raises(SystemExit):
            parse_arguments()
    
    @patch('src.cli.args.configure_language')
    def test_handle_cli_arguments_set_language(self, mock_configure):
        """Test handle_cli_arguments with --set-language flag"""
        # Mock parse_arguments to return args with set_language=True
        with patch('src.cli.args.parse_arguments') as mock_parse:
            mock_args = MagicMock()
            mock_args.set_language = True
            mock_parse.return_value = mock_args
            
            result = handle_cli_arguments()
            
            assert result is False  # Should return False to exit
            mock_configure.assert_called_once()
    
    def test_handle_cli_arguments_normal(self):
        """Test handle_cli_arguments without --set-language flag"""
        # Mock parse_arguments to return args with set_language=False
        with patch('src.cli.args.parse_arguments') as mock_parse:
            mock_args = MagicMock()
            mock_args.set_language = False
            mock_parse.return_value = mock_args
            
            result = handle_cli_arguments()
            
            assert result is True  # Should return True to continue 