# Given an integer number it returns its digits
def digits(num: int) -> list[int]:
    result = []
    num = abs(num)
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


def personal_year(date: str) -> int:
    day, month, year = date.split(".")
    # int = date.replace('.', "")
    day, month, year = int(day), int(month), int(year)
    result = 0

    result += sum(digits(day))
    result += sum(digits(month))
    result += sum(digits(year))

    return reduce(result, 11)


if __name__ == "__main__":
    # print(personal_year("09.09.1991")) # 11

    while (True):
        date = input("date: ")
        print(f'personal: {personal_year(date)}')
        print("----------------")


#
