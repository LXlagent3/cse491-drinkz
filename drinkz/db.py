"""
Database functionality for drinkz information.
"""

import convert
from cPickle import dump, load

_bottle_types_db = set(tuple())
_inventory_db = {}

_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set(tuple())
    _inventory_db = {}
    _recipe_db = {}

def save_db(filename):

    try:
        os.unlink(filename)
    except OSError:
        pass

    db = sqlite3.connect(filename)

    with db:
        c = db.cursor()

        c.execute("CREATE TABLE BottleTypes(mfg STRING, liquor STRING, typ STRING)")
        c.execute("CREATE TABLE Inventory(mfg STRING, liquor STRING, amount STRING)")
        c.execute("CREATE TABLE Recipes(name STRING, ingredients BUFFER)")


        for (m, l, typ) in _bottle_types_db:
            c.execute("insert into BottleTypes values (?, ?, ?)", (m, l, typ))
        for (m, l) in _inventory_db:
            mfg = m
            liquor = l
            amount = _inventory_db[(mfg, liquor)]
            c.execute("insert into Inventory values (?, ?, ?)", (mfg, liquor, amount))

        for key in _recipe_db:
            templist = _recipe_db[key].ingredients 
            mList = ""
            for item in templist:
                liquor, amt = item
                mList += "{}:{};".format(liquor, amt)
            buflist = buffer(mList[:-1]) 

            c.execute("insert into Recipes values (?, ?)", (key, buflist)) 

        db.commit()
        c.close()

def load_db(filename):

    db = sqlite3.connect(filename)
    db.text_factory = str

    with db:

        c = db.cursor()

        c.execute("SELECT * FROM BottleTypes") 
        rows = c.fetchall()
        for row in rows:
            mfg,liquor,typ = row
            
            _bottle_types_db.add((mfg,liquor,typ))

        c.execute("SELECT * FROM Inventory") 
        rows = c.fetchall()
        for row in rows:
            mfg,liquor,amt = row
            _inventory_db[(mfg, liquor)]=amt

        c.execute("SELECT * FROM Recipes") 
        rows = c.fetchall()
        for row in rows:
            name,ingredients = row
            mList = []
            for t in str(ingredients).split(';'): 
                liq, amt = t.split(':') 
                mList.append((liq, amt)) 
            ing_list = mList            
            r = recipes.Recipe(name,ing_list) 
            add_recipe(r) 

        db.commit()
        c.close()

class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    if check_inventory(mfg, liquor):
	
        new_amount = convert.convert_ml(amount)
        old_amount = get_liquor_amount(mfg, liquor)
        new_total = float(old_amount) + float(new_amount)
        _inventory_db[(mfg, liquor)] = str(new_total)+' ml'


    else:    
        _inventory_db[(mfg, liquor)] =  amount

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
           amounts.append(_inventory_db[key])
            
    total_ml = 0.0

    for i in amounts:
        total_ml += float(convert.convert_ml(i))    

    return total_ml 

def get_liquor_inventory(): 
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]

def add_recipe(r):
    
    if r.name not in _recipe_db:
        _recipe_db[r.name]=r
    else:
        raise DuplicateRecipeName()
    
def get_recipe(name):
        if name not in _recipe_db:
            return None
        return _recipe_db[name]

def get_all_recipes():
    
    return _recipe_db.values()

def get_all_recipe_names():
    return _recipe_db.keys()

