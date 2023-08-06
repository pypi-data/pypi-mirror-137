from time import strftime, gmtime


def second_to_strf(seconds: int, str_format: str = "%H:%M:%S") -> str:
    """Format seconds to format

    Args:
        @param seconds: seconds
        @param str_format: format

    Returns:
        str: seconds in string format

    """
    return strftime(str_format, gmtime(seconds))
