import importlib
import sys
from typing import Any, Dict
from src.config.settings import USER_LOCALE

class MessageLoader:
    def __init__(self, default_module: str, translation_module: str = None):
        self.default_messages = self._load_module_dicts(default_module)
        self.translation_messages = self._load_module_dicts(translation_module) if translation_module else {}

    def _load_module_dicts(self, module_path: str) -> Dict[str, Any]:
        if not module_path:
            return {}
        module = importlib.import_module(module_path)
        # Only load ALL_CAPS dicts
        return {k: v for k, v in vars(module).items() if k.isupper() and isinstance(v, dict)}

    def get(self, key: str, **kwargs) -> str:
        parts = key.split('.')
        # Try translation first
        msg = self._get_from_dict(self.translation_messages, parts)
        if msg is None:
            msg = self._get_from_dict(self.default_messages, parts)
        if msg is None:
            raise KeyError(f"Message key not found: {key}")
        if kwargs:
            try:
                return msg.format(**kwargs)
            except Exception as e:
                raise ValueError(f"Error formatting message '{key}': {e}")
        return msg

    def _get_from_dict(self, d: Dict[str, Any], parts):
        current = d
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

# Determine translation module based on USER_LOCALE
# If USER_LOCALE is empty, we'll handle it in the get_message function
if USER_LOCALE == 'uk':
    translation_module = 'src.locales.uk.messages_uk'
elif USER_LOCALE == 'en':
    translation_module = None
else:
    translation_module = None  # Default/fallback for unknown locales

# Singleton/global loader and function
_loader = MessageLoader(
    default_module='docs.messages',
    translation_module=translation_module
)

def get_message(key: str, **kwargs) -> str:
    # If USER_LOCALE is empty, initialize language configuration
    if not USER_LOCALE:
        from src.config.language_config import initialize_language_if_needed
        initialize_language_if_needed()
        # Re-import settings to get updated USER_LOCALE
        from src.config.settings import USER_LOCALE as updated_locale
        # Update the global loader with the correct translation module
        global _loader
        if updated_locale == 'uk':
            translation_module = 'src.locales.uk.messages_uk'
        else:
            translation_module = None
        _loader = MessageLoader(
            default_module='docs.messages',
            translation_module=translation_module
        )
    
    return _loader.get(key, **kwargs) 