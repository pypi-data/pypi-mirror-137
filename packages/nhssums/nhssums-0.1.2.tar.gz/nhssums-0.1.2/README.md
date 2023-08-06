# nhssums

<!-- badges: start -->
[![lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html)
<!-- badges: end -->

The nhssums package provides functions for working with NHS number checksums.

## NHS Number Overview

NHS numbers are issued to patients of the NHS in the UK.

The number consists of 9 digits and a single digit checksum.

For more information, please see the
[NHS number Wikipedia article](https://en.wikipedia.org/wiki/NHS_number)
on the subject.



## Instalation

To install the [published version](https://pypi.org/project/nhssums)  of the
package from PyPI:

```
python3 -m pip install nhssums
```

## Usage

Use `is_valid()` to iterate over a list of numbers:

``` python
>>> nhssums = [1234567881, 1234567806, 123456876, 1234512343]
>>> nhssums.is_valid(nhs_numbers)
[True, True, False, True]
```

To check if the checksum is valid for a single number, use `is_number_valid()`:

``` python
>>> import nhssums
>>> nhssums.is_number_valid(1234567881)
True
>>> nhssums.is_number_valid(1234567882)
False
```

Finally, `generate_checksum()` will return a valid checksum, for a given input
number. It can also return the full number (input + checksum) if required:

``` python
>>> nhssums.generate_checksum(123451234)
3
>>> nhssums.generate_checksum(123451234, full_output = True)
1234512343
```

## License

This package is released under an MIT license.

