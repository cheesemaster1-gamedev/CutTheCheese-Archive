# LANGUAGES/language_module.py

from PySide6.QtWidgets import QLabel as _QLabel, QPushButton as _QPushButton, QLineEdit as _QLineEdit
from Global import GlobalVariables as GVars
#from RESOURCES.Autocorrect import QLineEdit as _QLineEdit
import json, logging
import os, difflib
from wordfreq import top_n_list, zipf_frequency
import RESOURCES.Autocorrect as AC

# --- Load Translations ---

def load_translations(language_code: str):
    """Load translations for the given language code."""
    if language_code != 'EN':
        path = f'LANGUAGES/{language_code}.json'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None

# --- Translator ---

_lang_cache = None
_last_lang = None
GAME_WORDS = ['Chest', 'Apple Juice', 'Craft', 'Slipper']
tGAME_WORDS = []

def get_lang():
    """Reload translations if language changed."""
    global _lang_cache, _last_lang
    if _last_lang != GVars.selectedLang:
        _lang_cache = load_translations(GVars.selectedLang)
        _last_lang = GVars.selectedLang
    return _lang_cache

def translate(text: str) -> str:
    """Return translated text or fallback to original."""
    if not text:
        return text
    lang = get_lang()
    if lang and text in lang:
        return lang[text]
    return text

for word in GAME_WORDS:
    translated = translate(word)
    tGAME_WORDS.append(translated)
GAME_WORDS = tGAME_WORDS

# --- Redefined Widgets ---

class QLabel(_QLabel):
    """QLabel that auto-translates its text."""
    def __init__(self, text='', *args, **kwargs):
        if GVars.selectedLang != 'EN':
            super().__init__(translate(text), *args, **kwargs)
        else:
            super().__init__(text, *args, **kwargs)

class QPushButton(_QPushButton):
    """QPushButton that auto-translates its text."""
    def __init__(self, text='', *args, **kwargs):
        if GVars.selectedLang != 'EN':
            super().__init__(translate(text), *args, **kwargs)
        else:
            super().__init__(text, *args, **kwargs)

class QLineEdit(_QLineEdit):
    def __init__(self, text='', *args, **kwargs):
        if GVars.selectedLang != 'EN':
            super().__init__(translate(text), *args, **kwargs)
        else:
            super().__init__(text, *args, **kwargs)

    def autocorrect(self, input_word):
        if not input_word.strip():
            return None

        input_word = input_word.lower()
        words = GAME_WORDS + top_n_list(GVars.selectedLang, 10000)

        # 1. exact match first
        for word in words:
            if word.lower() == input_word:
                return word

        # 2. best match search
        best_word = None
        best_score = float('inf')

        for word in words:
            score = AC.levenshtein_distance(input_word, word.lower())

            if score < best_score:
                best_score = score
                best_word = word

        return best_word

    '''
    def autocorrect(self, word) -> str:
        word = word.lower().strip()
        words = top_n_list(GVars.selectedLang.lower(), 50000)  # top 50k English words
        matches = difflib.get_close_matches(word, words, n=1, cutoff=0.8)
        return matches[0] if matches else word
    '''

    def text(self) -> str:
        input_text = super().text()
        text = self.autocorrect(input_text)
        lang = get_lang()
        if lang:
            for key, translated in lang.items():
                if text == translated:
                    return key
        return text
