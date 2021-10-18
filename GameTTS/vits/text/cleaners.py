""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
import gruut

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def gruut_cleaner(text):
    # Table for str.translate to fix gruut/TTS phoneme mismatch
    GRUUT_TRANS_TABLE = str.maketrans("g", "ɡ")
    phonemizer_args = {
        "remove_stress": True,
        "ipa_minor_breaks": False,  # don't replace commas/semi-colons with IPA |
        "ipa_major_breaks": False,  # don't replace periods with IPA ‖
    }

    text = lowercase(text)
    ph_list = gruut.text_to_phonemes(
        text,
        lang="de-de",
        return_format="word_phonemes",
        phonemizer_args=phonemizer_args,
    )

    # Join and re-split to break apart dipthongs, suprasegmentals, etc.
    ph_list = ["".join(word_phonemes) for word_phonemes in ph_list]

    clean_text = " ".join(ph_list)

    # Fix a few phonemes
    clean_text = (
        clean_text.translate(GRUUT_TRANS_TABLE)
        .replace(" .", ".")
        .replace(" ?", "?")
        .replace(" !", "!")
        .replace(" ,", ",")
        .replace(" :", ":")
        .replace(" ;", ";")
    )
    clean_text = collapse_whitespace(clean_text)

    return clean_text