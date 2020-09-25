from src.ingredient import Ingredient
from src.inventory import Inventory
from src.main import Main

class Order():

    def __init__(self, ID, status=-1):
        self._mains = []
        self._sides = []
        self._drinks = []
        self._status = status
        self._orderID = ID

    @property
    def mains(self):
    	return self._mains
		
    @property
    def sides(self):
    	return self._sides

    @property
    def drinks(self):
    	return self._drinks

    @property
    def status(self):
    	return self._status

    @property
    def orderID(self):
    	return self._orderID

# ----------------------------------------------
    def update_status(self, value):
# ----------------------------------------------
        # 1 is ready, 0 is not ready, -1 hasn't been checkout, 2 archived
        if value == 0 or value == 1:
            self._status = value
            if value == 1:
                return f'Status updated successfully. Order ready!'
            elif value == 0:
                return f'Status updated successfully. Order not ready.'
        elif value == 2:
            self._status = value
            return f'Order has been archived'
        else:
            return f'Invalid'    

# ----------------------------------------------
    def list_items(self):
# ----------------------------------------------
        print('~~~ listing all mains ~~~')
        for main in self.mains:
            print(main.__str__())
        print('')

        print('~~~ listing all sides ~~~')
        for side in self.sides:
            print(side.name)
        print('')

        print('~~~ listing all drinks ~~~')
        for drink in self.drinks:
            print(drink.name)
        
# ----------------------------------------------
    def add_item(self, inv, ingredient, size=None):
# ----------------------------------------------
        item = inv.get_ingredient(ingredient.lower())

        if item is None:
            return f'Item does not exist'
        elif item.stock < 1:
            return f'Not enough stock'

        if item.kind == 'side':
            self._sides.append([item,size])
            return True
        elif item.kind == 'drink':
            self._drinks.append([item,size])
            return True
        else:
            print('Invalid input')

# ----------------------------------------------
    def create_main(self, inv,*args):
# ----------------------------------------------
        fillings=[]
        pattie = None
        numPatties = None
        for item in args:
            if type(item) is list and (len(item) > 1) and isinstance(item[1], int):
                item[0] = inv.get_ingredient(item[0])
                if item[0] is None:
                    return f'Invalid item chosen'
                if item[0].kind == 'bread':
                    if item[0].stock < item[1]:         
                        return f'Not enough stock of {item[0].name}'
                    bread = item[0]
                    if item[1] > 0 and item[1] < 4:
                        numBuns = item[1]
                    else:
                        return f'Invalid bun number'
                elif item[0].kind == 'pattie':
                    if item[0].stock < item[1]:       
                        return f'Not enough stock of {item[0].name}'
                    pattie = item[0]
                    if item[1] > 0 and item[1] < 4:
                        numPatties = item[1]
                    else:
                        return f'Invalid patty number'
            elif type(item) is list and item is not None:
                for list_item in item:
                    filling = inv.get_ingredient(list_item)
                    if filling is None:
                        return f'Invalid item chosen'
                    if filling.kind == 'filling':
                        if filling.stock < 1:         
                            return f'Not enough stock of {filling.name}'
                        fillings.append(filling)

        
        new_main = Main(bread,fillings,pattie,numBuns, numPatties)

        self._mains.append(new_main)

        return new_main

# ----------------------------------------------
    def calculate_total(self):
# ----------------------------------------------
        price = 0

        for main in self.mains:
            price += main.calculate_price()
        for side in self.sides:
            price += side[0].cost*side[0].size[side[1]]      
        for drink in self.drinks:
            if drink[1] == None:
                price += drink[0].cost
            else:
                price += drink[0].cost*drink[0].size[drink[1]]
        return price

# ----------------------------------------------
    def decrease_stock(self):       # Called when payment complete 
# ----------------------------------------------
        for main in self.mains:
            main.decrease_stock()

        for drink in self.drinks:
            if drink[1] == None:
                drink[0].update_stock(-1)
            else:
                drink[0].update_stock(-drink[0].size[drink[1]])

        for side in self.sides:
            side[0].update_stock(-side[0].size[side[1]])
    
# ----------------------------------------------
    def __str__(self):
# ----------------------------------------------
        text = f"Order ID: {self.orderID}|\n"
        text += f'Mains:'
        for main in self.mains:
            text += f"\t{main.__str__()}\n"
        text+= f'\n \tDrinks:'
        for drink in self.drinks:
            text += f'{drink[0].name}'
        text+= f'\n \tSides:'
        for side in self.sides:
            text += f'{side[0].name}'

        return text
