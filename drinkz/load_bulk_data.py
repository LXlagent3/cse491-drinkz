"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package


def csv_reader(fp):
    reader = csv.reader(fp)

    for each_line in reader:
        if len(each_line) == 0 or line[0].startswith('#'):
            continue
        yield line

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = csv.reader(fp)

    x = []
    n = 0
    try:
        for mfg, name, typ in reader:
            n+=1
            db.add_bottle_type(mfg, name, typ)
    except ValueError:
        print "Invalid Line."
        pass

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = csv.reader(fp)

    x = []
    n = 0
    try:
        for mfg, name, amount in reader:
            n+=1
            db.add_to_inventory(mfg, name, amount)
    except ValueError:
        print "Invalid Line."
        pass

    return n
