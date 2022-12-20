
def solution():
    array = []
    elf = []
    while True:
        curr = input()
        if curr:
            elf.append(int(curr))
        elif elf:
            array.append(sum(elf))
            elf = []
        else:
            break
    array.sort()
    return array[-1] + array[-2] + array[-3]



if __name__ == "__main__":
    print(solution())