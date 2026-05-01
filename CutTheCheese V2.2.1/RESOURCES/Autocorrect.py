from PySide6.QtWidgets import (
    QLineEdit as _QLineEdit
)
from Global import GlobalVariables as GVars
import json
import os, logging
from wordfreq import top_n_list, zipf_frequency
import difflib

GAME_WORDS = ['Chest', 'Apple Juice', 'Craft', 'Slipper']

class QLineEdit(_QLineEdit):
    def __init__(self, text='', *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    def text(self) -> str:
        input_text = super().text()
        output = self.autocorrect(input_text)
        return output

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
            score = levenshtein_distance(input_word, word.lower())

            if score < best_score:
                best_score = score
                best_word = word

        return best_word
    

def levenshtein_distance(a, b):
    a = a.lower()
    b = b.lower()

    if a == b:
        return 0

    if len(a) == 0:
        return len(b)

    if len(b) == 0:
        return len(a)

    # build matrix
    prev_row = list(range(len(b) + 1))

    for i, ca in enumerate(a, start=1):
        current_row = [i]

        for j, cb in enumerate(b, start=1):
            insert_cost = current_row[j - 1] + 1
            delete_cost = prev_row[j] + 1
            replace_cost = prev_row[j - 1] + (ca != cb)

            current_row.append(min(insert_cost, delete_cost, replace_cost))

        prev_row = current_row

    return prev_row[-1]
