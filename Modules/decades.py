def get_decade(date):
    """
    Returns the decade of a given date.

    Parameters:
        date (datetime): The date to get the decade from.

    Returns:
        str: The decade of the given date.

    """
    year = date.year
    decade = str(year - year%10) + 's'
    return decade