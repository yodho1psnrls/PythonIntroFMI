def is_ice_empty(iceberg: list[str], empty_part="0"):
    for line in iceberg:
        for ice in line:
            if ice != empty_part:
                return False

    return True


def will_ice_melt(iceberg: list[list[str]], x, y, ice="*"):
    if iceberg[x][y] != ice:
        return

    n = 0
    n += iceberg[x + 1][y] == ice
    n += iceberg[x - 1][y] == ice
    n += iceberg[x][y + 1] == ice
    n += iceberg[x][y - 1] == ice

    return n >= 2


if __name__ == "__main__":

    N = int(input())
    iceberg = []

    for i in range(N):
        iceberg.append(str(input()))

    print(N * "=")

    # print(iceberg)
    # for line in iceberg:
    #     print(line)

    ICE = "*"

    hours = 0

    while not is_ice_empty(iceberg):
        temp = iceberg

        for x in range(len(iceberg)):
            for y in range(len(iceberg[x])):
                if will_ice_melt(iceberg, x, y, "*"):
                    temp[x][y] = "0"

        iceberg = temp
        hours += 1

    print(hours)


#
