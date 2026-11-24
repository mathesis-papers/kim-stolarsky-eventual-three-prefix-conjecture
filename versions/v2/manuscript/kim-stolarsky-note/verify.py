import json
from fractions import Fraction


def polynomial(values):
    result = tuple(Fraction(value) for value in values)
    while len(result) > 1 and result[-1] == 0:
        result = result[:-1]
    return result


def add(*arguments):
    length = max(map(len, arguments))
    return polynomial(sum(argument[index] if index < len(argument) else 0
                          for argument in arguments) for index in range(length))


def scale(argument, factor):
    return polynomial(value * factor for value in argument)


def multiply(*arguments):
    result = polynomial([1])
    for argument in arguments:
        values = [Fraction(0)] * (len(result) + len(argument) - 1)
        for left_index, left_value in enumerate(result):
            for right_index, right_value in enumerate(argument):
                values[left_index + right_index] += left_value * right_value
        result = polynomial(values)
    return result


def power(argument, exponent):
    return multiply(*([argument] * exponent))


def evaluate(argument, value):
    result = Fraction(0)
    for coefficient in reversed(argument):
        result = result * value + coefficient
    return result


def continued_fraction(value):
    digits = []
    while True:
        digit = value.numerator // value.denominator
        digits.append(digit)
        remainder = value - digit
        if not remainder:
            return digits
        value = 1 / remainder


def reconstruct(digits):
    value = Fraction(digits[-1])
    for digit in reversed(digits[:-1]):
        value = digit + 1 / value
    return value


def left_polynomial(parameter, delta):
    squared = Fraction(parameter**2 * (parameter + 1)**2, 4)
    return ((squared + 1) * delta**3 + (6 * squared + 12) * delta**2
            + (12 * squared + 48) * delta
            - (4 * parameter**3 + 9 * parameter**2 + 6 * parameter - 63))


def third_polynomial(parameter, delta):
    coefficient = Fraction(parameter**2 + parameter + 2, 2)
    return left_polynomial(parameter, delta) + (parameter - 3 - coefficient * delta)**2


def left_delta(parameter, tail):
    return Fraction(4 * (16 * tail + 13),
                    48 * parameter * tail + 39 * parameter + 20 * tail + 16)


def third_delta(parameter, tail):
    return Fraction(4 * (3 * tail + 1), 9 * parameter * tail + 3 * parameter + 4 * tail)


def polynomial_certificates():
    parameter = polynomial([0, 1])
    squared_four = multiply(power(parameter, 2), power(polynomial([1, 1]), 2))
    constant = polynomial([-63, 6, 9, 4])
    coefficient = scale(polynomial([2, 1, 1]), Fraction(1, 2))

    def scaled_left(numerator, denominator):
        return add(multiply(add(squared_four, (4,)), power(numerator, 3)),
                   multiply(add(scale(squared_four, 6), (48,)),
                            power(numerator, 2), denominator),
                   multiply(add(scale(squared_four, 12), (192,)),
                            numerator, power(denominator, 2)),
                   scale(multiply(constant, power(denominator, 3)), -4))

    first = polynomial([37000394928, 153160798296, 216415841355,
                        111108436490, 9740981349, 304726968, 3171150])
    second = polynomial([-753289137476, -3039824512752, -4118482794221,
                         -1910502470606, -50623742159, -335894760, 133974])
    assert scaled_left((945, 36), (289, 720, 27)) == first
    assert scaled_left((2561, 36), (794, 1932, 27)) == scale(second, -1)
    threshold = 10**6
    assert all(value > 0 for value in first)
    assert sum(abs(second[index]) / Fraction(threshold**(6 - index))
               for index in range(6)) < 336

    quadratic = polynomial([-432, -1134, -719, 35])
    linear = polynomial([-120, -548, -512, 6, -6])
    constant_third = polynomial([-8, -54, -89, -1, -2])

    def transformed_third(tail):
        return add(multiply(quadratic, power(tail, 2)),
                   multiply(linear, tail), constant_third)

    lower = scale(polynomial([128, 6]), Fraction(1, 35))
    upper = scale(polynomial([129, 6]), Fraction(1, 35))
    assert scale(transformed_third(lower), 1225) == polynomial(
        [-7625288, -21789398, -16055337, -653633, -194])
    assert scale(transformed_third(upper), 1225) == scale(polynomial(
        [-483782, -1381575, -1016978, -40816, 1]), 16)
    assert (Fraction(40816, threshold) + Fraction(1016978, threshold**2)
            + Fraction(1381575, threshold**3) + Fraction(483782, threshold**4)
            < Fraction(41, 1000))
    for tail_value in range(4):
        numerator = polynomial([4 * (3 * tail_value + 1)])
        denominator = polynomial([4 * tail_value, 9 * tail_value + 3])
        square_part = add(multiply((-3, 1), denominator),
                          scale(multiply(coefficient, numerator), -1))
        actual = add(scaled_left(numerator, denominator),
                     scale(multiply(power(square_part, 2), denominator), 4))
        expected = scale(multiply((7 * tail_value + 1, 9 * tail_value + 3),
                                  transformed_third((tail_value,))), -32)
        assert actual == expected
    shifted = polynomial([4164, 3336, 609, 42, 1])
    assert add(*(scale(power((12, 1), index), coefficient)
                 for index, coefficient in enumerate((-12, -48, -39, -6, 1)))) == shifted
    return {'left_endpoint_identities': 2, 'third_endpoint_identities': 2,
            'third_transform_identity': 'degree-three identity in the tail; four coefficient-polynomial comparisons',
            'sign_bound_threshold': threshold, 'status': 'pass'}


def run_checks():
    certificates = polynomial_certificates()
    odd_failures = []
    third_failures = []
    for index in range(61):
        parameter = 10**(4 * index + 2)
        quotient = parameter // 7
        first = parameter // 2 + 2
        odd = Fraction(4 * parameter**2 + 6 * parameter + 2,
                       parameter**2 + parameter + 2)
        predicted_odd = {0: [4, first, quotient - 1, 1, 6],
                         1: [4, first, quotient - 1, 1, 2, 2],
                         2: [4, first, quotient, 7]}[index % 3]
        assert continued_fraction(odd) == predicted_odd
        assert reconstruct(predicted_odd) == odd
        if predicted_odd[2] != quotient - 1:
            odd_failures.append(index)
        even = Fraction(4 * parameter**2 + 2 * parameter,
                        parameter**2 + parameter + 2)
        quotient_even = parameter // 28
        even_first = parameter // 2 - 3
        predicted_even = {
            0: [3, 1, even_first, 1, 1, quotient_even, 4, 1, 2],
            1: [3, 1, even_first, 1, 1, quotient_even - 1, 1, 13],
            2: [3, 1, even_first, 1, 1, quotient_even - 1, 1, 3, 1, 2],
        }[index % 3]
        assert continued_fraction(even) == predicted_even
        assert reconstruct(predicted_even) == even
        if index >= 1:
            left_digit = Fraction(9 * parameter - 92, 404)
            assert left_digit.denominator == 1
            assert left_polynomial(parameter, left_delta(parameter, left_digit)) > 0
            assert left_polynomial(parameter, left_delta(parameter, left_digit + 1)) < 0
            third_digit = (6 * parameter + 128) // 35
            assert third_polynomial(parameter, third_delta(parameter, third_digit)) > 0
            assert third_polynomial(parameter, third_delta(parameter, third_digit + 1)) < 0
            source_digit = (6 * parameter + 134) // 35
            assert third_digit == source_digit - (index % 3 == 2)
            if third_digit != source_digit:
                third_failures.append(index)
    assert odd_failures == list(range(2, 61, 3)) == third_failures
    for parameter in range(12, 10001, 2):
        odd = Fraction(4 * parameter**2 + 6 * parameter + 2,
                       parameter**2 + parameter + 2)
        assert continued_fraction(odd)[:3] == [4, parameter // 2 + 2, (parameter - 3) // 7]
        if parameter >= 40:
            even = Fraction(4 * parameter**2 + 2 * parameter,
                            parameter**2 + parameter + 2)
            assert continued_fraction(even)[:6] == [3, 1, parameter // 2 - 3,
                                                    1, 1, (parameter - 10) // 28]
    for parameter in range(2, 31):
        for value in [-5, -4, 0, 1]:
            source_left = (sum((2 * position - 1)**3 for position in range(1, parameter + 2))
                           + value**3
                           + sum((2 * position - 2 + (position - 1) * value)**3
                                 for position in range(2, parameter + 2)))
            source_third = (value * sum((4 * position + 1 + position * value)
                                        * ((position + 1) * (position - 2) + position**2 * value)
                                        for position in range(parameter + 1))
                            - value**2 + value**3)
            assert source_left == -left_polynomial(parameter, -4 - value)
            assert source_third == -third_polynomial(parameter, -4 - value)
    for distance in range(1, 21):
        for parameter in range(31):
            summation = sum((distance + 1 - 2 * position)
                            * (distance + 1 - 2 * (distance + 1) * position + 2 * position**2)
                            for position in range(1, parameter + 1))
            assert summation == -parameter**2 * (parameter - distance)**2
    return {
        'status': 'pass',
        'arithmetic': 'exact Python integers and fractions.Fraction',
        'polynomial_certificates': certificates,
        'odd_and_even_full_expansion_indices': {'minimum': 0, 'maximum': 60, 'count': 61},
        'cubic_branch_prefix_indices': {'minimum': 1, 'maximum': 60, 'count': 60},
        'source_R_and_Q_failure_indices': odd_failures,
        'general_squared_odd_even_parameters': {'minimum': 12, 'maximum': 10000, 'step': 2},
        'general_squared_even_prefix_parameters': {'minimum': 40, 'maximum': 10000, 'step': 2},
        'source_polynomial_controls': {'parameters': '2..30', 'arguments': [-5, -4, 0, 1]},
        'double_zero_family_controls': {'distances': '1..20', 'parameters': '0..30'},
        'coverage': 'Polynomial identities and sign bounds; rational full expansions; cubic-root prefix brackets; finite source-sum and double-zero-family controls.',
    }


if __name__ == '__main__':
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
