# NOTE:
# You can convert int to string and
#  then use python map function to map the
#  string of digits to list of digits

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


'''
def personal_year(date: str) -> int:
    day, month, year = date.split(".")
    day, month, year = int(day), int(month), int(year)
    result = 0

    result += sum(digits(day))
    result += sum(digits(month))
    result += sum(digits(year))

    return reduce(result, 11)
'''


# Shorter Implementation
def personal_year(date: str) -> int:
    whole_num = int(date.replace('.', ""))
    return reduce(sum(digits(whole_num)), 11)


if __name__ == "__main__":
    # print(personal_year("09.09.1991")) # 11

    while (True):
        date = input("date: ")
        print(f'personal: {personal_year(date)}')
        print("-" * len(date))


#
