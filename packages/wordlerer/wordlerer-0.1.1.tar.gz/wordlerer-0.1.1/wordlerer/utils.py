def filter_by_length(words: list[str], length: int) -> list[str]:
    return [word for word in words if len(word) == length]
