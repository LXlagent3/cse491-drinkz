import db

class Recipe:
    def __init__(self, name, ingredient):
        self.name = name
        self.ingredients = ingredient

    def need_ingredients(self):
        MissingList =[]
    
        KeyList=[]
        TypeList=[]
        for (Type, amount) in self.ingredients:
            for mfg, liquor in db.check_inventory_type(Type):
                KeyList.append((mfg, liquor))
            TypeList.append((Type, KeyList))
            KeyList = []

        TotalInv = 0.0
        AmountList=[]
        for (Type, key) in TypeList:
            for (mfg, liquor) in key:
                if (mfg, liquor) in db._inventory_db or TypeList[1] == []:
                    if db._inventory_db[(mfg, liquor)] > TotalInv:
                        TotalInv = db._inventory_db[(mfg, liquor)]
            AmountList.append((Type, TotalInv))
            TotalInv = 0

        TotalNeed = 0.0
        for (Type, amount) in self.ingredients:
            for (Type1, amount1) in AmountList:
                if Type == Type1:
                    TotalNeed = float(db.convert_ml(amount)) - float(amount1)
                    if TotalNeed > 0.0:
                        MissingList.append((Type1, TotalNeed))
        return MissingList
