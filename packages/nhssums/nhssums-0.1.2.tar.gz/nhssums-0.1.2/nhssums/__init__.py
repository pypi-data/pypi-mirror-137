"""
A package to validate NHS number checksums
"""

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version("nhssums")


def generate_checksum(nhs_number, full_output=False):
    """
    generates a checksum from an input number
    """
    if len(str(nhs_number)) != 9:
        raise ValueError("Supplied number should be 9 digits long")
    split_number = [int(i) for i in str(nhs_number)]
    multipliers = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplied = [a * b for a, b in zip(split_number, multipliers)]
    remainder = sum(multiplied) % 11
    check_digit = 11 - remainder
    if check_digit == 10:
        raise ValueError("Invalid checksum of 10 generated")
    if check_digit == 11:
        check_digit = 0
    if full_output:
        return int(str(nhs_number) + str(check_digit))
    return check_digit


def is_number_valid(nhs_number):
    """
    Checks the validity of a single NHS number
    """
    if not isinstance(nhs_number, int):
        raise TypeError("supplied number should be int")
    if len(str(nhs_number)) != 10:
        raise ValueError("Supplied number should be 10 digits long")
    number_no_checksum = int(str(nhs_number)[0:9])
    supplied_checksum = int(str(nhs_number)[9])
    if supplied_checksum == generate_checksum(number_no_checksum):
        return True
    return False


def is_valid(nhs_numbers):
    """
    Checks the validity of a list of numbers
    """
    if not isinstance(nhs_numbers, list):
        raise TypeError("nhs_numbers should be a list")
    output = []
    for nhs_number in nhs_numbers:
        try:
            output.append(is_number_valid(nhs_number))
        except ValueError:
            output.append(False)
        except TypeError:
            output.append(False)
    return output
