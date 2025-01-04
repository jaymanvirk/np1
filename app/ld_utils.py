from lingua import Language, LanguageDetectorBuilder
import pycld2 as cld2
from ld_manager import LangListManager
import re
import os

LINGUA_LANGUAGES = os.getenv('LINGUA_LANGUAGES').split(',')
LANGUAGES = [getattr(Language, lang.strip().upper()) for lang in LINGUA_LANGUAGES]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

def get_detected_langs(text):
    result = DETECTOR.detect_multiple_languages_of(text)
    langs_lingua = {}
    for r in result:
        langs_lingua.setdefault(r.language.name, []).append((r.start_index, r.end_index))

    _, _, details, _ = cld2.detect(text, bestEffort=True, returnVectors=True)

    langs_cld2 = set(d[0] for d in details if d[0] != 'Unknown')

    llk = set(langs_lingua.keys())
    d = langs_cld2 ^ llk
    s = langs_cld2 & llk

    if d:
        if d & llk:
            d = d & llk
        else:
            d = s
            s = set()

    prev_lang = ''
    word_pos = {}
    linked_list = LangListManager()

    for l in s:
        for st, en in langs_lingua[l]:
            linked_list.insert(l, st, en)

    for l in d:
       for st, en in langs_lingua[l]:
            for match in re.finditer(r'\S+', text[st:en]):
                word = match.group()
                start, end = match.span()
                start += st
                end += st

                lw = DETECTOR.detect_multiple_languages_of(word)
                if lw:
                    lw = lw[0]
                else:
                    break
                lang = lw.language.name
                pos = [start, end]
                if lang in word_pos:
                    word_pos[lang][1] = pos[1]
                else:
                    if prev_lang in word_pos:
                        tmp = word_pos[prev_lang]
                        linked_list.insert(prev_lang, tmp[0], tmp[1])
                        del word_pos[prev_lang]
                    word_pos[lang] = pos
                    prev_lang = lang

    if prev_lang in word_pos:
        tmp = word_pos[prev_lang]
        linked_list.insert(prev_lang, tmp[0], tmp[1])


    return linked_list
