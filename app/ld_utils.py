import pycld2 as cld2

def detect_language(text):
    _, _, _, language_bytes = cld2.detect(text, bestEffort=True, returnVectors=True)
    return language_bytes[0][1]
