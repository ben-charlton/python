from src.customer import Customer
from src.order import Order
from src.inventory import Inventory
from src.main import Main
import random 
import pickle

class RestaurantSystem():

    def __init__(self,inventory):
        self._customers = {}
        self._orders = {}
        self._inventory = inventory

    def get_customer(self, customer_id):
        return self._customers.get(customer_id)

    def get_order(self, order_id):
        return self._orders.get(order_id)

    def inventory(self): 
        return self._inventory

    '''-----------------------------------------------
        CREATE
    -----------------------------------------------'''

    def create_customer(self):
        customer_id = random.randint(10000,99999)
        while self.get_customer(customer_id) is not None:
            customer_id = random.randint(10000,99999)

        customer = Customer(customer_id)
        self._customers[customer_id] = customer  
        return customer_id

    def create_order(self,customer):
        if self._orders == {}:
            order_id = 1 
        else:
            order_id = max(k for k, v in self._orders.items() if v != 0)+1
        
        order = Order(order_id)
        self._orders[order_id] = order
        customer.add_order_id(order_id)
        
        return order 



    '''-----------------------------------------------
        SERVICE
    -----------------------------------------------'''

    def check_order_status(self, order_id):
        try:
            order_id = int(order_id)
        except ValueError:
            return "Invalid input"

        if self.get_order(order_id) is None:
            return f'Order doesn\'t exist'

        return self.get_order(order_id).status

    def update_order_status(self, order_id, status):
        r = self.get_order(order_id).update_status(status)
        self.update_pickle()
        return r
 
    def view_current_orders(self):
        orders_list = []
        for x in self._orders:
            if self._orders[x].status is 0:
                orders_list.append(x)
        return orders_list

    def view_all_orders(self):
        orders_list = []
        for x in self._orders:
            if self._orders[x].status is not -1:
                orders_list.append(x)
        return orders_list

    def view_archive_orders(self):
        orders_list = []
        for x in self._orders:
            if self._orders[x].status is 2:
                orders_list.append(x)
        return orders_list

    def update_inventory(self, ingredientname, update):
        try:
            update = int(update)
        except ValueError:
            return None
        self.inventory.update_ingredient(ingredientname,update)
        return self.inventory.get_ingredient(ingredientname).stock
        

    def delete_order(self, order_id):
        self._orders.pop(order_id)
        #self.get_customer(customer_id).remove_order(order_id)
        self.update_pickle()

    def checkout(self,order_id):
        order = self.get_order(order_id)
        if order is not None:
            order.decrease_stock()
        else:
            return None
        self.update_order_status(order_id,0)
        self.update_pickle()

    '''-----------------------------------------------------------------
        Properties 
    -----------------------------------------------------------------'''
    @property
    def orders(self):
        return self._orders

    @property
    def customers(self):
        return self._customers

    @property
    def inventory(self):
        return self._inventory

    def update_pickle(self):
        f = open("order.pickle","wb")
        for orderID in self._orders:
            pickle.dump(self.get_order(orderID),f)
        f.close()

    def add_order(self, order):
        self._orders[order.orderID] = order
