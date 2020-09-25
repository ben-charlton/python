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

@pytest.fixture
def customer_id(system):
    return system.create_customer()

class Testpickle():

    def test_pickle_1(self,system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID) 
        assert len(system.orders) == 1

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)
        assert len(system.orders) == 2

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)
        assert len(system.orders) == 3

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)

        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], 'tomato','lettuce') # Cost = 4+4+1+1+3 = 13
        order.add_item(system.inventory, 'water')
        system.checkout(order.orderID)


        order = None
        orders = []
        f = open("order.pickle","rb")
        while True:
            try:
                order = pickle.load(f)
                orders.append(order)
            except EOFError:
                break
        f.close()

        assert len(orders) == 8




