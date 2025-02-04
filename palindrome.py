def is_text_char(ch: str) -> bool:
    ch = ch.lower()
    return ord("a") <= ord(ch) <= ord("z")


def only_alphabetic(word: str) -> str:
    result = ""
    for ch in word:
        if is_text_char(ch):
            result += ch
    return result


def is_palindrome(word: str) -> bool:
    # Leave only alphabetic characters
    word = only_alphabetic(word)
    # Remove spaces
    word = word.replace(" ", "")
    # Make all characters lower case
    word = word.lower()

    n = len(word)
    for i in range(n // 2):
        if word[i] != word[n - i - 1]:
            return False
    return True


if __name__ == "__main__":
    # Example Test

    while True:
        word = str(input())
        # print(is_palindrome(word))
        print(is_palindrome(word))


#
