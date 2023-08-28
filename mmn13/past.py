words = ["adopt", "bake", "beam", "cook", "time", "grill", "waved", "hire"]


def past_tense_transform(word: str) -> str:
    if word.endswith("ed"):
        return word
    elif word.endswith("e"):
        return word + "d"
    else:
        return word + "ed"


past_tense = [past_tense_transform(word) for word in words]

print(past_tense)
