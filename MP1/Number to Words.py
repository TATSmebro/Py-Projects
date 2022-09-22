inp = int(input())
num = str(inp)

tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
unit = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
special = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
number = list(range(0,10))

if 0 <= inp <= 100:
    if len(num) == 1:
        print(unit[inp])
    if len(num) == 2:
        if num[0] == '1':
            print(special[int(num[1])])
        elif num[1] == '0':
            print(tens[int(num[0])])
        else:
            print(tens[int(num[0])], unit[int(num[1])])
    if len(num) == 3:
        print('one hundred')
else:
    print('invalid')

