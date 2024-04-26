class Color:
    """
    These colors are used to print text colors in command line.

    Example:
    import Color
    print(f'{ Color.CYAN }{ svg }{ Color.END }: file extension is not svg.')
    """

    PURPLE = '\x1b[35m'
    CYAN = '\x1b[36m'
    GRAY = '\x1b[90m'
    RED = '\x1b[91m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    BLUE = '\x1b[94m'
    END = '\x1b[0m'
