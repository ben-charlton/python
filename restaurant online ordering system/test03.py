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

@pytest.fixture
def order1(system,customer_id):
	# order 1 
    order = system.create_order(system.get_customer(customer_id))
    order.add_item(system.inventory, 'Chips', 'Small')
    system.checkout(order.orderID)
    return order.orderID

@pytest.fixture
def order2(system,customer_id):
    # order 2
    order = system.create_order(system.get_customer(customer_id))
    order.add_item(system.inventory, 'water')
    system.checkout(order.orderID)
    return order.orderID

@pytest.fixture
def order3(system,customer_id):
    # order 3
    order = system.create_order(system.get_customer(customer_id))
    order.add_item(system.inventory, 'Nuggets', 'Medium')
    system.checkout(order.orderID)
    return order.orderID

class TestServiceOrders():
# Testing US 2.1/2 - Epic Story - Staff can service oders - view current orders and update status
#=======================================================================

    def test_sucessful_check_status(self,system,order1):
        assert system.check_order_status(order1) == 0

    def test_sucessful_update_status_avaliable(self,system,order2):
        assert system.check_order_status(order2) == 0
        assert system.update_order_status(order2,1) == 'Status updated successfully. Order ready!'
        assert system.check_order_status(order2) == 1

    def test_sucessful_update_status_unavaliable(self,system,order3):
        assert system.check_order_status(order3) == 0
        assert system.update_order_status(order3,0) == 'Status updated successfully. Order not ready.'
        assert system.check_order_status(order3) == 0

    def test_sucessful_reupdate_status_unavaliable(self,system,order2):
        assert system.check_order_status(order2) == 0
        assert system.update_order_status(order2,1) == 'Status updated successfully. Order ready!'
        assert system.check_order_status(order2) == 1
        assert system.update_order_status(order2,0) == 'Status updated successfully. Order not ready.'
        assert system.check_order_status(order2) == 0

    def test_unsucessful_update_status_text(self,system,order1):
        assert system.check_order_status(order1) == 0
        assert system.update_order_status(order1,'whoops') == 'Invalid'
        assert system.check_order_status(order1) == 0

    def test_unsucessful_update_status_number(self,system,order1):
        assert system.check_order_status(order1) == 0
        assert system.update_order_status(order1,4) == 'Invalid'
        assert system.check_order_status(order1) == 0

    def test_current_orders(self,system,order1,order2,order3):
        assert order1 == 1
        assert order2 == 2
        assert order3 == 3
        assert len(system._orders) == 3
        assert len(system.view_current_orders()) == 3

    def test_current_orders_all_unavaliable(self,system,order1,order2,order3):
        # assert order1 == 1
        # assert order2 == 2
        # assert order3 == 3
        assert len(system._orders) == 3
        system.update_order_status(order1,1)
        system.update_order_status(order2,1)
        system.update_order_status(order3,1)
        assert len(system.view_current_orders()) == 0

class TestCheckOrderStatus():
    # Testing US 1.10 - check status of order
#=======================================================================

    def test_sucessful_check_status(self, system, order1):
        assert system.check_order_status(order1) == 0

    def test_unsucessful_check_status(self, system, order2):
        assert system.check_order_status("test") == "Invalid input"

    def test_sucessful_check_status_int(self, system, order1):
        assert system.check_order_status(1) == 0

    def test_sucessful_check_status_string(self, system, order1):
        assert system.check_order_status('1') == 0

    def test_sucessful_check_wrong_order(self, system, order1):
        assert system.check_order_status(10) == "Order doesn't exist"