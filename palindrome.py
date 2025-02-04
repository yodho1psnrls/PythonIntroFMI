def is_palindrome(word: str) -> bool:
    n = len(word)
    for i in range(n // 2):
        if word[i] != word[n - i - 1]:
            return False
    return True


if __name__ == "__main__":
    # Example Test

    while True:
        word = str(input())
        print(is_palindrome(word))
