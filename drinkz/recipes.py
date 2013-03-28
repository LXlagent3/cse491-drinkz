import db, convert
#class for recipes

class Recipe(object):

    def __init__(self, name = "", ingredients = []):
	self.name = name
	self.ingredients = ingredients

    def need_ingredients(self):

        missing_list = []

        bottle_type_list = []
        
	for i in self.ingredients:
	    for item in db._bottle_types_db:
		if  i[0] == item[2]:
		    bottle_type_list.append(item)


        amounts_list = []

	for i in bottle_type_list:
	    if db.check_inventory(i[0], i[1]):
		amount = (i[0], i[2], db.get_liquor_amount(i[0], i[1]))
		amounts_list.append(amount)        
                
        for i in self.ingredients:
            amount = 0.0
            for item in amounts_list: 
                if i[0]==item[1]:
                    if amount < float(item[2]): 
                        amount = float(item[2])
            ing_amount = convert.convert_ml(i[1])            
            if float(amount) < float(ing_amount):
                needed = float(ing_amount)-float(amount)
                needed_tup = (i[0], needed)
                missing_list.append(needed_tup)


	return missing_list
