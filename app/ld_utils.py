import pycld2 as cld2
from lingua import Language, LanguageDetectorBuilder

def detect_language(text):
    _, _, _, vectors = cld2.detect(text, bestEffort=True, returnVectors=True)

    languages = [Language.ENGLISH, Language.RUSSIAN]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    lingua_result = detector.detect_multiple_languages_of(text)

    return language_bytes[0][1]
