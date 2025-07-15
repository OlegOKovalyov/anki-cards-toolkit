import argparse
import sys
from src.config.language_config import configure_language

def parse_arguments():
    """
    Parse command line arguments.
    Returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Anki Cards Toolkit - Create flashcards with rich content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate_card.py                    # Run normally
  python3 generate_card.py --set-language     # Set/reset language preference
  python3 generate_card.py -l                 # Set/reset language preference (short)
        """,
         allow_abbrev=False  # <---- IMPORTANT: Disallows partial matches
    )
    
    parser.add_argument(
        '--set-language', '-l',
        action='store_true',
        help='Set or reset the language preference (English/Ukrainian)'
    )

    def custom_error(message):
        sys.stderr.write(f'\n❌ {message}\n')
        parser.print_help(sys.stderr)
        sys.exit(2)
    parser.error = custom_error

    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)
    return args

def handle_cli_arguments():
    """
    Handle CLI arguments and perform appropriate actions.
    Returns True if the program should continue, False if it should exit.
    """
    args = parse_arguments()
    
    if args.set_language:
        # Configure language and exit
        configure_language()
        return False
    
    return True 