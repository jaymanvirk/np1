from lingua import Language, LanguageDetectorBuilder

def detect_language(text):

    languages = [Language.ENGLISH, Language.RUSSIAN]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    lingua_result = detector.detect_multiple_languages_of(text)

    return lingua_result 
