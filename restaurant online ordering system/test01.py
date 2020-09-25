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

#class TestInventory():
    # Pickle is now updated whenever the inventory changes

    # def test_sucessful_inventory_setup(self,system,inv):
    #     assert len(inv._bread) == 5
    #     assert len(inv._patties) == 3
    #     assert len(inv._fillings) == 7
    #     assert len(inv._sides) == 2
    #     assert len(inv._drinks) == 3

class TestCreateCustomer():
    
    def test_create_customer(self,system):
        customer_id = system.create_customer()
        system.get_customer(customer_id) 
        assert system.get_customer(customer_id) != None 

    def test_create_ten_customers(self,system):
        customer_ids = []
        for x in range(0,10):
            customer_ids.append(system.create_customer())
            system.get_customer(customer_ids[x]) 
        assert system.get_customer(customer_ids[x]) != None 
        assert len(customer_ids) == 10 


# Epic Story 1 - testing 
# Test Place Online Order

class TestCreateOrder():


# Testing US 1.1 - 1.5 - Create Burger 
#=======================================================================

    def test_sucessful_initiate_first_order(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert len(system._orders) == 1         
        assert len(system.get_customer(customer_id).list_order_ids()) == 1

    def test_unsucessful_create_main(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['wry bread', 1], ['cattle', 1], 'cockroach','dirt')
        assert len(order.mains) == 0

    def test_sucessful_create_main_no_fillings(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['muffin', 1], ['beef', 1], )
        assert len(order.mains) == 1

    def test_unsucessful_create_main_no_buns(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.create_main(system.inventory,['muffin', 0], ['beef', 1], ) == 'Invalid bun number'
        assert len(order.mains) == 0

    def test_unsucessful_create_main_too_many_buns(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.create_main(system.inventory,['muffin', 100], ['beef', 1], ) == 'Invalid bun number'
        assert len(order.mains) == 0

    def test_unsucessful_insufficient_buns(self, system, inv, customer_id):
        stock = inv.get_ingredient('glutenfree').stock
        system.update_inventory('glutenfree', -(stock-1))
        order = system.create_order(system.get_customer(customer_id))
        assert inv.get_ingredient('glutenfree').stock == 1
        fillings = ['tomato', 'lettuce']
        assert order.create_main(system.inventory,['glutenfree', 2], ['beef', 2], fillings) == 'Not enough stock of glutenfree'
        system.update_inventory('glutenfree', 100)    

    def test_unsucessful_create_main_no_patties(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.create_main(system.inventory,['muffin', 1], ['beef', -1], ) == 'Invalid patty number'
        assert len(order.mains) == 0

    def test_sucessful_create_main_too_many_patties(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.create_main(system.inventory,['muffin', 1], ['beef', 100], ) == 'Invalid patty number'
        assert len(order.mains) == 0

    def test_unsucessful_insufficient_patties(self, system, inv, customer_id):
        stock = inv.get_ingredient('beef').stock
        system.update_inventory('beef', -stock)
        order = system.create_order(system.get_customer(customer_id))
        assert inv.get_ingredient('beef').stock == 0
        fillings = ['tomato', 'lettuce']
        assert order.create_main(system.inventory,['glutenfree', 2], ['beef', 2], fillings) == 'Not enough stock of beef'
        system.update_inventory('beef', 150)

    def test_sucessful_create_main_all_availble_fillings(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato', 'swiss cheese', 'cheddar cheese', 'lettuce', 'pineapple', 'beetroot']
        order.create_main(system.inventory,['sesame seed', 2], ['beef', 2], fillings )
        assert len(order.mains[0].fillings) == 6
        assert len(order.mains) == 1

    def test_unsucessful_create_main_no_existing_fillings(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['toothpaste','shampoo'] 
        order.create_main(system.inventory,['sesame seed', 1], ['veggie', 1], fillings )
        assert len(order.mains) == 0

    def test_unsucessful_ingredient_low_stock(self, system, inv, customer_id):
        system.update_inventory('pickles', -10000)
        order = system.create_order(system.get_customer(customer_id))
        assert inv.get_ingredient('pickles').stock == 0
        fillings = ['pickles', 'lettuce']
        assert order.create_main(system.inventory,['sesame seed', 2], ['beef', 2], fillings) == 'Not enough stock of pickles'

    def test_create_multiple_mains(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings1 = ['tomato', 'lettuce']
        fillings2 = ['beetroot', 'pineapple']
        main = order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], fillings1)
        main2 = order.create_main(system.inventory,['muffin', 1], ['beef', 1], fillings2)
        assert len(order.mains) == 2

    def test_sucessfull_delete_order(self,system,customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato', 'lettuce']
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], fillings)
        assert len(system.orders) == 1
        system.delete_order(order.orderID)
        assert len(system.orders) == 0

    def test_sucessful_large_order_multiple_mains_sides_drinks(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings1 = ['pineapple','beetroot']
        fillings2 = ['tomato','lettuce']
        order.create_main(system.inventory,['muffin', 1], ['veggie', 1],fillings1 ) # Cost = 4+4+1+1+3 = 13
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1], fillings2 ) # Cost = 4+4+1+1+3 = 13
        assert order.add_item(system.inventory, 'water') == True
        assert order.add_item(system.inventory, 'coke bottle') == True
        assert order.add_item(system.inventory, 'nuggets') == True
        assert order.add_item(system.inventory, 'chips') == True
        assert len(order.mains) == 2
        assert len(order.drinks) == 2
        assert len(order.sides) == 2

    def test_decrement_stock(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato','lettuce']
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1],fillings )
        order.add_item(system.inventory, 'water')
        stock1 = order.drinks[0][0].stock
        stock2 = order.mains[0].get_bread().stock
        stock3 = order.mains[0].get_pattie().stock
        order.decrease_stock()
        assert order.drinks[0][0].stock == stock1 - 1
        assert order.mains[0].get_bread().stock == stock2 - 1 
        assert order.mains[0].get_pattie().stock == stock3 - 1

    def test_decrement_stock_multiple_patties_and_buns(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato', 'lettuce']
        order.create_main(system.inventory,['sesame seed', 2], ['beef', 2], fillings)
        order.add_item(system.inventory, 'water')
        stock1 = order.drinks[0][0].stock
        stock2 = order.mains[0].get_bread().stock
        stock3 = order.mains[0].get_pattie().stock
        order.decrease_stock()
        assert order.drinks[0][0].stock == stock1 -1
        assert order.mains[0].get_bread().stock == stock2 - 2
        assert order.mains[0].get_pattie().stock == stock3 - 2

# Testing US 1.6 - Selecting Sides
#=======================================================================
    def test_sucessful_add_side(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'chips','Small')
        assert len(order.sides) == 1

    def test_sucessful_add_side_captials(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'CHIPS','Small')
        assert len(order.sides) == 1


    def test_unsucessful_add_side(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.add_item(system.inventory, 'hash browns', 'Large') == 'Item does not exist'
        assert len(order.sides) == 0


    def test_sucessful_add_multiple_sides(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'chips', 'Small')
        assert len(order.sides) == 1
        order.add_item(system.inventory, 'chips', 'Small')
        assert len(order.sides) == 2
        order.add_item(system.inventory, 'chips', 'Small')
        assert len(order.sides) == 3

    def test_sucessful_side_medium_decrement_stock(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'CHIPS','Medium')
        stock = order.sides[0][0].stock
        order.decrease_stock() 
        assert order.sides[0][0].stock == stock - int(order.sides[0][0].size[order.sides[0][1]])
        assert len(order.sides) == 1

    def test_sucessful_side_small_decrement_stock(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'CHIPS','Small')
        stock = order.sides[0][0].stock
        order.decrease_stock() 
        assert order.sides[0][0].stock == stock - int(order.sides[0][0].size[order.sides[0][1]])
        assert len(order.sides) == 1

    def test_sucessful_side_small_price(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'CHIPS','Small')
        assert order.calculate_total() == 3

    def test_sucessful_side_medium_price(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'CHIPS','Medium')
        assert order.calculate_total() == 5

# Testing US 1.7 - Selecting Drinks
#=======================================================================

    def test_sucessful_add_drink(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'water')
        assert len(order.drinks) == 1

    def test_sucessful_add_drink_capitals(self, system, customer_id):
         order = system.create_order(system.get_customer(customer_id))
         order.add_item(system.inventory, 'WATER')
         assert len(order.drinks) == 1

    def test_unsucessful_add_drink(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.add_item(system.inventory, 'wine') == 'Item does not exist'
        assert len(order.drinks) == 0

    def test_unsucessful_add_non_existing_drink(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        assert order.add_item(system.inventory, 'wine') == 'Item does not exist'
        assert len(order.drinks) == 0

    def test_unsucessful_add_drink_no_stock(self, inv, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        system.update_inventory('orange juice', -10000)
        assert inv.get_ingredient('orange juice').stock == 0
        assert order.add_item(system.inventory, 'Orange Juice', 'Large') == 'Not enough stock'
        assert len(order.drinks) == 0

    def test_sucessful_add_many_drinks(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'WATER')
        assert len(order.drinks) == 1
        order.add_item(system.inventory, 'coke can')
        assert len(order.drinks) == 2
        order.add_item(system.inventory, 'coke bottle')
        assert len(order.drinks) == 3


    def test_sucessful_drink_with_size_decrement_stock_small(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'water', 'Small' )
        stock = order.drinks[0][0].stock
        order.decrease_stock()
        assert len(order.drinks) == 1
        assert order.drinks[0][0].stock == stock - 1

    def test_sucessful_drink_with_size_decrements_stock_large(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'water', 'Large' )
        stock = order.drinks[0][0].stock
        order.decrease_stock()
        assert len(order.drinks) == 1
        assert order.drinks[0][0].stock == stock - 3

    def test_sucessful_drink_with_size_cost_small(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'water', 'Small' )
        assert len(order.drinks) == 1
        assert order.calculate_total() == 2

    def test_sucessful_drink_with_size_correct_cost_large(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'water', 'Large' )
        assert len(order.drinks) == 1
        assert order.calculate_total() == 6

# Testing US 1.8 - View Total Price
#=======================================================================
    def test_sucessful_calculate_price(self, system, customer_id):
        # assert if price is correct for meal
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato','lettuce']
        order.create_main(system.inventory,['sesame seed', 1], ['beef', 1],fillings ) 
        order.add_item(system.inventory, 'water')
        assert order.calculate_total() == 12

    def test_sucessful_calculate_price_side(self, system, customer_id):
        # assert if price is correct for meal
        order = system.create_order(system.get_customer(customer_id))
        order.add_item(system.inventory, 'chips', 'Small')
        assert order.calculate_total() == 3

    def test_unsucessful_calculate_price(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        order.create_main(system.inventory,['buttery buns', 1], ['clam', 1],) 
        assert order.calculate_total() == 0

# Testing US 1.9 - Check Out
#=======================================================================

    def test_sucessful_checkout(self, system, customer_id):
        order = system.create_order(system.get_customer(customer_id))
        fillings = ['tomato','lettuce']
        main = order.create_main(system.inventory,['sesame seed', 1], ['beef', 1],fillings )
        system.checkout(order.orderID)
        assert order.status == 0
