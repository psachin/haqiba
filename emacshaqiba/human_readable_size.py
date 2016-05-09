"""Convert numbers into human readable form.
"""

def hr_size(size):
    """Human-readable file size.
    """
    suffixes = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    for suffix in suffixes:
        if size < 1000:
            return "%s %s" % (size, suffix)
        size = size // 1000
    return "%s %s" % (size, suffix)

# print hr_size(5232)

