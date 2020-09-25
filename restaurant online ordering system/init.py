from src.inventory import Inventory
from src.restaurant_system import RestaurantSystem
from src.order import Order
from src.customer import Customer
from src.ingredient import Ingredient
import pickle

def bootstrap_system():

    obj = None
    inv = Inventory()
    f = open("food.pickle","rb")
    while True:
        try:
            obj = pickle.load(f)
            inv.add_ingredient(obj)
        except EOFError:
            break
    f.close()

    sys = RestaurantSystem(inv)

    order = None
    f = open("order.pickle","rb")
    while True:
        try:
            order = pickle.load(f)
            sys.add_order(order)
            print(order.orderID)
        except EOFError:
            break
    f.close()



    return sys
