"""Template Filters."""
from itertools import zip_longest

from pprint import pprint as pp

def to_table(value):
    """Convert the results of groupby to a table."""
    header = []
    nodes = []

    for group, items in value:
        header.append(group)
        nodes.append(items)

    retval = [header]

    for row in zip_longest(*nodes):
        retval.append(row)

    return retval
