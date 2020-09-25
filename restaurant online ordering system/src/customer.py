class Customer():

    def __init__(self, customer_id, order_ids=[]):
        self._customer_id = customer_id
        self._order_ids = order_ids

    @property
    def customer_id(self):
         return self._customer_id

    def list_order_ids(self):
        return self._order_ids

    def add_order_id(self, order_id):
        self._order_ids.append(order_id)

    def remove_order(self,order_id):
        self._order_ids.remove(order_id)

    
    def __str__(self):
        output = f'Customer: {self.customer_id}'
        if not self._order_ids:
            output += f'\nOrders: {self._order_ids}'
        return output
