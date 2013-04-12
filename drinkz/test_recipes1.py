import sys
sys.path.insert(0, 'bin/') 
import os

from . import db, load_bulk_data
from cStringIO import StringIO
import imp


def test_script_load_liquor_recipes():
    db._reset_db()

    scriptpath = 'bin/load-liquor-recipes'
    module = imp.load_source('llt', scriptpath)

    exit_code = module.main([scriptpath, 'test-data/recipe-test.txt'])
    assert 'Recipe1' in db.get_all_recipe_names()
