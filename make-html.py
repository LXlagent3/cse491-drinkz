import os
from drinkz import db, recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

db._reset_db()

db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')
db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')
db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
db.add_recipe(r)
r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'), ('vermouth', '1.5 oz')])
db.add_recipe(r)
r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
db.add_recipe(r)


fp = open('html/index.html', 'w')
print >>fp, """
<p><a href='index.html'>Index!</a></p>
<p><a href='recipes.html'>Recipes!</a></p>
<p><a href='inventory.html'>Inventory!</a></p>
<p><a href='liquor_types.html'>Liquor types!</a></p>
<h1>HW3--Task4!(Index)</h1>
"""




fp.close()


fp = open('html/recipes.html', 'w')

print >>fp, """
<p><a href='index.html'>Index!</a></p>
<p><a href='recipes.html'>Recipes!</a></p>
<p><a href='inventory.html'>Inventory!</a></p>
<p><a href='liquor_types.html'>Liquor types!</a></p>
<h1>Recipes</h1>
<ul>
"""
for receipes in db.get_all_recipes():
  print >>fp, "<li>"
  print >>fp, receipes.name
  if receipes.need_ingredients() == []:
    print >>fp, ", Have all ingredients."
  else:
    print >>fp, ", Need extra ingredients."

  print >>fp, "</li>"
print >>fp, "</ul>"


fp.close()


fp = open('html/inventory.html', 'w')

print >>fp, """
<p><a href='index.html'>Index!</a></p>
<p><a href='recipes.html'>Recipes!</a></p>
<p><a href='inventory.html'>Inventory!</a></p>
<p><a href='liquor_types.html'>Liquor types!</a></p>
<h1>Inventory</h1>
<ul>
"""

for m,l in db.get_liquor_inventory():
  print >>fp, "<li>"
  print >>fp, m
  print >>fp, ", "
  print >>fp, db.get_liquor_amount(m, l)
  print >>fp, " ml"
  print >>fp, "</li>"

print >>fp, "</ul>"

fp.close()


fp = open('html/liquor_types.html', 'w')

print >>fp, """
<p><a href='index.html'>Index!</a></p>
<p><a href='recipes.html'>Recipes!</a></p>
<p><a href='inventory.html'>Inventory!</a></p>
<p><a href='liquor_types.html'>Liquor types!</a></p>
<h1>Liquor Types</h1>
<ul>
"""

for mfg, liquor in db.get_liquor_inventory():
    print >>fp, "<p> </p>"
    print >>fp, '<li> %s, %s' % (mfg, liquor)

print >>fp, "</ul>"

fp.close()

