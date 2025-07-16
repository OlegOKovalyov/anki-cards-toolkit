import importlib
import sys
from typing import Any, Dict
from src.config.settings import USER_LOCALE
from src.locales.language_map import LANGUAGE_NAMES

class MessageLoader:
    def __init__(self, default_module: str, translation_module: str = None):
        self.default_messages = self._load_module_dicts(default_module)
        self.translation_messages = self._load_module_dicts(translation_module) if translation_module else {}

    def _load_module_dicts(self, module_path: str) -> Dict[str, Any]:
        if not module_path:
            return {}
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            return {}
        except Exception as e:
            print(f"Warning: Failed to load translation module '{module_path}': {e}")
            return {}
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

def _get_translation_module(locale: str) -> str:
    if locale and locale in LANGUAGE_NAMES and locale != 'en':
        module_path = f"src.locales.{locale}.messages_{locale}"
        try:
            importlib.import_module(module_path)
            return module_path
        except ModuleNotFoundError:
            print(f"Warning: Translation module for locale '{locale}' not found. Falling back to English.")
        except Exception as e:
            print(f"Warning: Error loading translation module for locale '{locale}': {e}. Falling back to English.")
    elif locale and locale not in LANGUAGE_NAMES:
        print(f"Warning: Locale '{locale}' is not supported. Falling back to English.")
    return None

# Singleton/global loader and function
_loader = MessageLoader(
    default_module='docs.messages',
    translation_module=_get_translation_module(USER_LOCALE)
)

def get_message(key: str, **kwargs) -> str:
    # If USER_LOCALE is empty, initialize language configuration
    if not USER_LOCALE:
        from src.config.language_config import initialize_language_if_needed
        initialize_language_if_needed()
        # Re-import settings to get updated USER_LOCALE
        from src.config.settings import USER_LOCALE as updated_locale
        global _loader
        _loader = MessageLoader(
            default_module='docs.messages',
            translation_module=_get_translation_module(updated_locale)
        )
    return _loader.get(key, **kwargs) 