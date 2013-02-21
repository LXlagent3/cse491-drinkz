"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()
# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
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

    Total = convert_ml(amount)
    
    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += Total
    else:
        _inventory_db[(mfg, liquor)] = Total

def convert_ml(amount):
    Total = []
    Total = amount.split(" ")
    TotalAmount = 0.0
    if Total[1].lower() == "ml":
        TotalAmount += float(Total[0])
    elif Total[1].lower() == "oz":
        TotalAmount += float(Total[0]) * 29.5735
    elif Total[1].lower() == "gallon":
        TotalAmount += float(Total[0]) * 3785.41
    elif Total[1].lower() == "liter":
        TotalAmount += float(Total[0]) * 1000
    return TotalAmount

def check_inventory(mfg, liquor):
    if (mfg, liquor) in _inventory_db:
        return True
    return False

def check_inventory_type(Type):
    for (m, l) in _inventory_db:
        if (m, l, Type) in _bottle_types_db:
            yield (m, l)
    
def get_liquor_amount(mfg, liquor):
    AmountList = []
    TotalAmount = 0.0
    for each in _inventory_db:
        m = each[0]
        l = each[1]
        temp = _inventory_db[each]
        if mfg == m and liquor == l:
            AmountList.append(temp)
    for amount in AmountList:
        TotalAmount += float(amount)
    return TotalAmount

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for k,v in _inventory_db.iteritems():
        m = k[0]
        l = k[1]
        yield m, l

def add_recipe(inputreceipe):
    for receipes in _recipes_db:
        if receipes.name == inputreceipe.name:
            err = "Duplicate Recipes: %s", inputreceipe.name
            raise DuplicateRecipeName(err)
    _recipes_db.add(inputreceipe)
        
def get_recipe(name):
    for receipes in _recipes_db:
        if receipes.name == name:
            return receipes
        
def get_all_recipes():
    tempset = set()
    for receipes in _recipes_db:
        tempset.add(receipes)
    return tempset
