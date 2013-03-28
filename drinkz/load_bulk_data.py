"""
Module to load in bulk data from text files.
"""
import csv                              

from . import db                        

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)
    x = []
    n = 0
    
    while(1):
        try:
            for (mfg, name, typ) in new_reader:
    	    	amt = typ.split()
       	        n += 1
                db.add_bottle_type(mfg, name, typ)
	    new_reader.next()
	except StopIteration:
	    break
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
    new_reader = data_reader(fp)

    x = []
    n = 0
 
    while(1):
        try:
    	    for (mfg, name, amount) in new_reader:
                n += 1
                db.add_to_inventory(mfg, name, amount)
    	    new_reader.next()
    	except StopIteration:
    	    break
    return n
    
    
def data_reader(fp):
    reader = csv.reader(fp)
  
    for line in reader:
	try:
            if line[0].startswith('#'):
		continue
	    if not line[0].strip():
		continue
	except IndexError:
            pass
	try:
            (mfg,name,value) = line
        except ValueError:
            continue
        yield mfg, name, value
		
			
