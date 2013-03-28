import os
from drinkz import db, recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

db._reset_db()

drinkz.db.load_db("bin/test_database")


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

