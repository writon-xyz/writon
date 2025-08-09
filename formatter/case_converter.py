"""
Case conversion module for Writon CLI
"""

import re


def convert_case(text, style):
    """Convert text to specified case style"""
    if style == "lower":
        return text.lower()
    elif style == "upper":
        return text.upper()
    elif style == "sentence":
        return _capitalize_sentences(text)
    elif style == "title":
        return _to_title_case(text)
    return text


def _capitalize_sentences(text):
    """Capitalize the first letter of each sentence"""
    sentences = re.split(r"([.!?]+\s*)", text)
    result = ""
    capitalize_next = True

    for part in sentences:
        if re.match(r"[.!?]+\s*", part):
            result += part
            capitalize_next = True
        elif part.strip():
            if capitalize_next and part.strip():
                stripped = part.lstrip()
                leading_space = part[: len(part) - len(stripped)]
                if stripped:
                    result += leading_space + stripped[0].upper() + stripped[1:]
                else:
                    result += part
                capitalize_next = False
            else:
                result += part
        else:
            result += part

    # Ensure first character is capitalized
    if result and result[0].islower():
        result = result[0].upper() + result[1:]

    return result


def _to_title_case(text):
    """Convert text to Title Case following standard rules"""
    # Words that stay lowercase (except first/last word)
    small_words = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "if",
        "in",
        "nor",
        "of",
        "on",
        "or",
        "so",
        "the",
        "to",
        "up",
        "yet",
    }

    words = text.lower().split()
    if not words:
        return text

    result = []
    for i, word in enumerate(words):
        # Always capitalize first and last word
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        # Keep small words lowercase unless they're first/last
        elif word in small_words:
            result.append(word)
        else:
            result.append(word.capitalize())

    return " ".join(result)
