from src.restaurant_system import RestaurantSystem
from src.customer import Customer
from src.order import Order
from src.inventory import Inventory
from src.ingredient import Ingredient
from src.main import Main
import pytest
import pickle

@pytest.fixture 
def inv():
    inv = Inventory()
    f = open("food.pickle","rb")
    while True:
        try:
            obj = pickle.load(f)
            inv.add_ingredient(obj)
        except EOFError:
            break
    f.close()
    return inv

@pytest.fixture 
def system(inv):
    sys = RestaurantSystem(inv)
    return sys

#class TestInventory():

    # def test_sucessful_inventory_setup(self,system,inv):
    #     assert len(inv._bread) == 5
    #     assert len(inv._patties) == 3
    #     assert len(inv._fillings) == 7
    #     assert len(inv._sides) == 2
    #     assert len(inv._drinks) == 3

class TestUpdateInventory():

# Testing US 3.1 - Update Inventory -- plus extra features add new items
#=======================================================================

    def test_sucessful_update_inventory(self, system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', 1)
        assert system.inventory.get_ingredient('tomato').stock == stock + 1
    
    def test_sucessful_decrease_inventory(self, system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', -1)
        assert system.inventory.get_ingredient('tomato').stock == stock - 1 

    def test_sucessful_no_change(self,system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', 0)
        assert system.inventory.get_ingredient('tomato').stock == stock

    def test_unsucessful_update(self, system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', 'test')
        assert system.inventory.get_ingredient('tomato').stock == stock

    def test_sucessful_update_integer_string(self, system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', '1')
        assert system.inventory.get_ingredient('tomato').stock == stock + 1

    def test_sucessful_multiple_updates(self, system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', 1)
        assert system.inventory.get_ingredient('tomato').stock == stock + 1
        system.update_inventory('tomato', 10)
        assert system.inventory.get_ingredient('tomato').stock == stock +1 +10
        system.update_inventory('tomato', -100)
        assert system.inventory.get_ingredient('tomato').stock == stock +1 +10 -100
        
    def test_sucessful_empty_stock(self,system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', -stock)
        assert system.inventory.get_ingredient('tomato').stock == 0

    def test_sucessful_empty_greater_than_stock(self,system):
        stock = system.inventory.get_ingredient('tomato').stock
        system.update_inventory('tomato', -(stock+100))
        assert system.inventory.get_ingredient('tomato').stock == 0 

    def test_sucessful_add_new_item(self, system):
        ingredient = system.inventory.new_ingredient('drink', 'beer', 7, 10)
        assert ingredient.name == 'beer'
        assert ingredient.kind == 'drink'
        assert ingredient.cost == 7
        assert ingredient.stock == 10
        assert system.inventory.get_ingredient('beer') == ingredient
        system.inventory.delete_ingredient('beer')
        assert system.inventory.get_ingredient('beer') == None


    def test_sucessful_delete_item(self, system):
        system.inventory.delete_ingredient('tomato')
        assert system.inventory.get_ingredient('tomato') == None
        ingredient = system.inventory.new_ingredient('filling', 'tomato', 1, 100)

    def test_unsucessful_delete_item(self, system):
        assert system.inventory.delete_ingredient('dog') =='Ingredient doesnt exist'        

    def test_sucessful_update_cost(self, system):
        system.inventory.update_cost('tomato', 4)
        assert system.inventory.get_ingredient('tomato').cost == 4

    def test_unsucessful_update_cost_string(self, system):
        assert system.inventory.update_cost('tomato', 'four dollarydoos') == 'Invalid Input'
        assert system.inventory.update_cost('tictacs', 4) == 'Ingredient doesnt exist'

    def test_sucessful_update_cost_string(self, system):
        system.inventory.update_cost('tomato', '1')
        assert system.inventory.get_ingredient('tomato').cost == 1
        




        






