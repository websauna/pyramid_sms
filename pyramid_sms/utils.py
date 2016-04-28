def normalize_us_phone_number(number: str) -> str:
    """Clean phone number and convert is raw US phone number in international format.

    :param number: Hand typed US phone number like (555) 123-1234

    :return: Raw phone number like +15551231234
    """
    assert type(number) == str
    digits = "+0123456789"
    number = "".join([digit for digit in number if digit in digits])

    # International 00 prefix
    if number.startswith("00"):
        number = number[2:]

    # Assume US, with area code
    if not number.startswith("+"):
        if not number.startswith("1"):
            number = "1" + number
        number = "+" + number

    return number
