import hashlib
from collections import Counter


def analyse_string(value: str) -> dict:
    if value is None:
        raise ValueError("value is required")
    
    #length
    length = len(value)

    #is_palindrome (which is case insensitive and ignores whitespaces)
    normalized = value.lower()
    is_pal = normalized == normalized[::-1]

    #unique characters
    unique_characters = len(set(value))

    #word count (split by whiteapces)
    word_count = len(value.split())

    # sha256
    sha = hashlib.sha256(value.encode("utf-8")).hexdigest()

    #frequency map
    freq = dict(Counter(value))
    return{
        "length": length,
        "is_palindrome": is_pal,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha,
        "character_frequency_map": freq,

    }