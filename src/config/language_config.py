import os
import re
import sys
import subprocess
from typing import Optional

def get_language_choice() -> str:
    """
    Prompt user to choose language and return the selected language code.
    Supports any number of languages defined in LANGUAGE_NAMES.
    Returns the selected language code (e.g., 'en', 'uk', 'de', etc.).
    """
    from src.locales.language_map import LANGUAGE_NAMES
    from docs.messages import INITIALIZATION_CONFIGURATION
    
    # Dynamically build the options list
    options = []
    code_list = list(LANGUAGE_NAMES.keys())
    for idx, code in enumerate(code_list, 1):
        options.append(f"[{idx}] {LANGUAGE_NAMES[code]}")
    options_str = "\n".join(options)
    prompt_msg = INITIALIZATION_CONFIGURATION["language_prompt"].format(options=options_str)
    invalid_msg = INITIALIZATION_CONFIGURATION["language_invalid_choice_dynamic"]

    while True:
        choice = input(prompt_msg).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(code_list):
                return code_list[idx]
        print(invalid_msg, end='')

def save_language_to_env(language: str, env_file: str = '.env') -> None:
    """
    Save the selected language to the .env file.
    Creates .env file if it doesn't exist.
    """
    env_content = ""
    
    # Read existing .env file if it exists
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # Check if USER_LOCALE already exists in the file
    if 'USER_LOCALE=' in env_content:
        # Replace existing USER_LOCALE line
        env_content = re.sub(r'USER_LOCALE=.*', f'USER_LOCALE={language}', env_content)
    else:
        # Add USER_LOCALE to the end of the file
        if env_content and not env_content.endswith('\n'):
            env_content += '\n'
        env_content += f'USER_LOCALE={language}\n'
    
    # Write back to .env file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)

def configure_language() -> str:
    """
    Configure language by prompting user and saving the choice.
    Supports any number of languages defined in LANGUAGE_NAMES.
    Returns the selected language code (e.g., 'en', 'uk', 'de', etc.).
    """
    language = get_language_choice()
    save_language_to_env(language)
    
    from src.locales.language_map import LANGUAGE_NAMES
    language_name = LANGUAGE_NAMES.get(language, "Unknown")
    from docs.messages import INITIALIZATION_CONFIGURATION
    set_msg = INITIALIZATION_CONFIGURATION["language_set"].format(language=language_name)
    print(set_msg)
    print("🔄 Restarting to apply language change...")
    subprocess.run([sys.executable, sys.argv[0]])
    sys.exit(0)

def should_prompt_for_language() -> bool:
    """
    Check if we should prompt for language selection.
    Returns True if USER_LOCALE is not set or is empty.
    """
    user_locale = os.getenv('USER_LOCALE', '')
    return not user_locale or user_locale.strip() == ''

def initialize_language_if_needed() -> None:
    """
    Initialize language configuration if USER_LOCALE is not set.
    This function should be called early in the application startup.
    """
    if should_prompt_for_language():
        configure_language()
        # Reload environment variables after saving
        from dotenv import load_dotenv
        load_dotenv(override=True) 