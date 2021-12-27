import math


class number:
    def __init__(self, number, base):
        self.fract = []
        self.integ = []

        self.hexMapInversed = "0123456789ABCDEF"
        self.bcdMapInversed = ("0000","0001","0010","0011","0100","0101","0110","0111","1000","1001")
        self.bcdMap = dict((self.bcdMapInversed[x], x) for x in range(len(self.bcdMapInversed)))
        self.hexMap = dict((self.hexMapInversed[x], x) for x in range(len(self.hexMapInversed)))
        self.currentBase = base
        parts = number.split(",")
        parts[0] = ((4-len(parts[0])%4)%4)*'0'+parts[0]
        parts[0] = parts[0][::-1]
        if (len(parts)>1):
            parts[1] += ((4-len(parts[1])%4)%4)*'0'

        if base == "BCD":
            for i in range(0,len(parts[0]),4):
                self.integ.append(self.bcdMap[parts[0][i:i+4][::-1]])
            if (len(parts)>1):
                for i in range(0, len(parts[1]), 4):
                    self.fract.append(self.bcdMap[parts[1][i:i + 4]])
            return

        for i in parts[0]:
            self.integ.append(self.hexMap[i])
        if (len(parts) > 1):
            for i in parts[1]:
                self.fract.append(self.hexMap[i])

    def __str__(self):
        str = ""
        # print(self.integ)
        # print(self.fract)

        for i in self.integ:
            str += self.hexMapInversed[i] if self.currentBase != "BCD" else self.bcdMapInversed[i][::-1]
        str = str[::-1]
        str = str.lstrip("0")
        if (len(str)==0):
            str = "0"

        str += ","

        for i in self.fract:
            str += self.hexMapInversed[i] if self.currentBase != "BCD" else self.bcdMapInversed[i]
        str = str.rstrip("0")
        if (len(self.fract) == 0):
            str+="0"
        return str

    def getValue(self):
        print('Перевод в десятичную СС:')
        sum = 0
        degree = 0
        for i in self.integ:
            ds = i * pow(self.currentBase, degree) if (self.currentBase!="BCD") else i * pow(10, degree)
            print(f"+{i} * {pow(self.currentBase, degree) if (self.currentBase!='BCD') else pow(10, degree)}")
            sum += ds
            # print(sum)
            degree += 1
        degree = 0

        for i in self.fract:
            degree -= 1
            ds = i * pow(self.currentBase, degree) if (self.currentBase!="BCD") else i * pow(10, degree)
            print(f"+{i} * {pow(self.currentBase, degree) if (self.currentBase!='BCD') else pow(10, degree)}")
            sum += ds
        print(f"= {sum}")
        return sum

    def toNewBase(self, base, precision):
        if (base=="BCD"):
            self.toNewBase(10, precision)
            self.currentBase = "BCD"
            return

        val = self.getValue()
        self.integ = []
        self.fract = []

        inte = math.floor(val)
        fr = round(val%1, 9)

        print("Перевод целой части:")
        print(' ' * 21 + '^')
        while (inte > 0):
            print('{:>12} % {:>2} ={:>2}|'.format(inte, base, inte % base))
            self.integ.append(inte % base)
            inte = inte // base
        prec_counter = 0

        print("Перевод дробной части:")
        while (fr > 0) and (prec_counter < precision):
            print(('{:>' + str(precision + 8) + '} *{:>2} = {:>9} | {}').format(str(fr), base, round(fr * base,9), int(fr*base)))
            fr *= base
            self.fract.append(math.floor(fr))
            fr = round(fr - math.floor(fr), 9)
            prec_counter += 1
        print(('{:>' + str(precision + 26) + '}').format("˅"))
        self.currentBase = base

while True:
    print("Задайте систему счисления (основание системы счисления или 'BCD'):")
    base = input()
    try:
        base = int(base)
    except:
        pass

    print("Введите число в заданной системе счисления (',' - разделитель целой и дробной частей):")
    num = input()
    h = number(num, base)

    while True:
        print("Задайте новую систему счисления (основание системы счисления или 'BCD'), или нажмите ввод, чтобы задать новое число:")
        base = input()
        try:
            base = int(base)
        except:
            pass
        if base == "":
           break
        h.toNewBase(base, 8)
        print(h)
        print()
