from math import tan
from math import sqrt
from decimal import Decimal


def hcf_finder(num1, num2):
    num1_factors = []
    num2_factors = []
    common_factors = []
    for i in range(num1 + 1):
        if i != 0 and num1 % i == 0:
            num1_factors.append(i)
    for i in range(num2 + 1):
        if i != 0 and num2 % i == 0:
            num2_factors.append(i)
    for i in range(len(num1_factors)):
        for n in range(len(num2_factors)):
            if num1_factors[i] == num2_factors[n]:
                common_factors.append(num2_factors[n])
    common_factors.reverse()
    return common_factors[0]


def hcf_finder_fast(num1, num2):
    while num2:
        num1, num2 = num2, num1 % num2
    return num1


def lcm_finder(num1, num2):
    x = num1
    y = num2
    while y:
        x, y = y, x % y
    hcf = x
    lcm = (num1 * num2) // hcf
    return lcm


def factor_finder(number):
    output = []
    for i in range(number + 1):
        if i != 0 and number % i == 0:
            output.append(i)
    return output


def prime_check(n):
    factors = []
    for i in range(n + 1):
        if i != 0 and n % i == 0:
            factors.append(i)
    if len(factors) == 2:
        return True
    else:
        return False


def odd_even_checker(number):
    if number % 2 == 0:
        return "even"
    elif number % 2 == 1:
        return "odd"
    else:
        return "Invalid number"


def square(number):
    return number * number


def cube(number):
    return pow(number, 3)


def find_distance_2_coor(x1, x2, y1, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def pythagoras(base_square, perpendicular_square):
    hypotenusesq = base_square + perpendicular_square
    hypotenuse = sqrt(hypotenusesq)
    return hypotenuse


def fibonacci(n):
    thelist = [1, 1]
    while len(thelist) != n:
        thelist.append(thelist[-1] + thelist[-2])
    return thelist


def cuberoot(x):  # Only Compatible with perfect cubes
    for ans in range(0, abs(x) + 1):
        if ans ** 3 == abs(x):
            break
    if ans ** 3 != abs(x):
        return 'Not a perfect cube'
    else:
        if x < 0:
            ans = -ans
    return ans


def to_the_power_anything_root(to_the_power_of_what, number):
    for ans in range(0, abs(number) + 1):
        if ans ** to_the_power_of_what == abs(number):
            break
    if ans ** to_the_power_of_what != abs(number):
        return 'Not perfect'
    else:
        if number < 0:
            ans = -ans
    return ans


def decimal_to_binary(n):
    return bin(n).replace("0b", "")


def binary_to_decimal(n):
    stingn = str(n)
    for character in stingn:
        if character == '.':
            return 'Invalid'
        if character != 0 and character != 1:
            return 'Invalid'
    num = n
    dec_value = 0

    base = 1

    temp = num
    while temp:
        last_digit = temp % 10
        temp = int(temp / 10)

        dec_value += last_digit * base
        base = base * 2
    return dec_value


def deciamal_to_octadecimal(n):
    return oct(n)


def octadecimal_to_decimal(n):
    decimal_value = 0
    base = 1

    while (n):
        last_digit = n % 10
        n = int(n / 10)
        decimal_value += last_digit * base
        base = base * 8
    return decimal_value


def decimal_to_hexadecimal(n):
    return hex(n)


def profit_percent_calculator(investment, output):
    profit_or_loss_amount = output - investment
    if profit_or_loss_amount >= 0:
        profit_or_loss = 'profit'
    elif profit_or_loss_amount < 0:
        profit_or_loss = 'loss'
    else:
        return 'Invalid Inputs'
    if profit_or_loss == 'profit':
        return str((profit_or_loss_amount / investment * 100)) + '% Profit'
    elif profit_or_loss == 'loss':
        return str((abs(profit_or_loss_amount) / investment * 100)) + '% Loss'


def average(listofvalues):
    return sum(listofvalues) / len(listofvalues)


def average2(*args):
    listofvalues = []
    for item in args:
        listofvalues.append(item)
    return sum(listofvalues) / len(listofvalues)


def a_plus_b_wholesquare(a, b):
    return pow(a + b, 2)


def a_minus_b_wholesquare(a, b):
    return pow(a - b, 2)


def a_square_plus_b_square(a, b):
    return pow(a, 2) + pow(b, 2)


def square_area(length):
    return length * length


def rectange_area(length, breadth):
    return length * breadth


def triange_area(base, height):
    return 0.5 * base * height


def regular_polygon_apothem(number_of_sides, lenght_of_each_side):
    return lenght_of_each_side / (2 * (tan(180 / number_of_sides)))


def regular_polygon_area(number_of_sides, length_of_each_side):
    apothem = length_of_each_side / (2 * (tan(180 / number_of_sides)))
    return (number_of_sides * length_of_each_side * apothem) / 2


def tow(base, mod):
    """Example: tow(10, 4) will return 10 to the power 10 to the power 10 to the power 10"""
    output = base
    for i in range(mod - 1):
        output = pow(output, base)
    return output


def is_decimal(n):
    x = type(n)
    x = str(x)
    if x == "<class 'float'>":
        return True
    else:
        return False


def is_square(n):
    num = sqrt(n)
    num = str(num)
    if num.endswith('.0'):
        return True
    return False


def add(*args):
    sum(args)


def subtract(*args):
    output = args[0]
    for num in args:
        output -= num


def multiply(*args):
    output = args[0]
    for num in args:
        output *= num


def divide(*args):
    output = args[0]
    for num in args:
        output /= num
