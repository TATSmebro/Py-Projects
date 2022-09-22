word = input()

for row in range(2*len(word)-1):
    for col in range(2*len(word)-1):
        if col == len(word)-1-row or col == len(word)-1+row or col == row-(len(word)-1) or (row >= len(word)-1 and col == row + (len(word)-1) - 2*(row-(len(word)-1))):
            if row < len(word):
                print(word[row], end='')
            else:
                print(word[(2*len(word)-2)-row], end='')
        else:
            print(' ', end='')
    print()