def is_ice_empty(iceberg: list[str], ice="*"):
    for row in iceberg:
        for col in row:
            if col == ice:
                return False

    return True


def ice_count(iceberg: list[str], ice="*"):
    count = 0
    for row in iceberg:
        for x in row:
            count += (x == ice)  # branchless version
    return count


def will_ice_melt(iceberg: list[list[str]], x, y, ice="*"):
    if iceberg[x][y] != ice:
        return False

    n = 0
    n += iceberg[x + 1][y] != ice
    n += iceberg[x - 1][y] != ice
    n += iceberg[x][y + 1] != ice
    n += iceberg[x][y - 1] != ice

    return n >= 2


def melted(iceberg: list[str], ice="*"):
    temp = [list(row) for row in iceberg]

    for x in range(len(iceberg)):
        for y in range(len(iceberg[x])):
            if will_ice_melt(iceberg, x, y, ice):
                temp[x][y] = "0"

    return ["".join(row) for row in temp]


ICE = "*"


if __name__ == "__main__":

    # Read from console
    # N = int(input())
    # iceberg = [str(input()) for _ in range(N)]
    # print(N * "=")

    # Read from file
    file = open("iceberg1.txt", "r")
    line = file.readline().strip()
    N = int(line)
    iceberg = [str(line.strip()) for line in file]

    hours = 0
    while not is_ice_empty(iceberg):
        for row in iceberg:
            print(row)
        print(N * "=")
        iceberg = melted(iceberg)
        hours += 1

    print(hours)
    file.close()
#
