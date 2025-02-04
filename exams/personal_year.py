# Given an integer number it returns its digits
def digits(num: int) -> list[int]:
    result = []
    while num >= 10:
        result.append(num % 10)
        num //= 10
    result.append(num)
    return list(reversed(result))


# Sums the digits until single digit or special number
def reduce(num: int, *specials) -> int:
    while num >= 10 and num not in specials:
        num = sum(digits(num))
    return num


def personal_year(year: str) -> int:
    day, month, year = year.split(".")
    day, month, year = int(day), int(month), int(year)
    result = 0

    result += sum(digits(day))
    result += sum(digits(month))
    result += sum(digits(year))

    return reduce(result, 11)


if __name__ == "__main__":
    year = input()
    print(personal_year(year))
    # print(personal_year("09.09.1991")) # 11


#
