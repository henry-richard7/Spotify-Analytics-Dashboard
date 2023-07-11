def get(millis):
    """
    Calculate the time duration in days, hours, minutes, and seconds based on the given milliseconds.

    Parameters:
        millis (int): The number of milliseconds to calculate the duration from.

    Returns:
        str: The time duration in days, hours, minutes, and seconds formatted as a string.
    """
    seconds, milliseconds = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    time_strings = [f"{value} {unit}" for value, unit in [(days, 'day'), (hours, 'hour'), (minutes, 'minute'), (seconds, 'second')] if value]

    result = ', '.join(time_strings[:-1]) + (' and ' if len(time_strings) > 1 else '') + time_strings[-1]
    return result