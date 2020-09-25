from src.ingredient import Ingredient
import pickle

class Inventory():

	def __init__(self):  
		self._bread = {}   # string = type of ingredient e.g. Sesame Bread
		self._patties = {}
		self._fillings = {}
		self._sides = {}
		self._drinks = {}

	@property
	def bread(self):
		return self._bread

	@property
	def patties(self):
		return self._patties        

	@property
	def fillings(self):
		return self._fillings

	@property
	def sides(self):
		return self._sides

	@property
	def drinks(self):
		return self._drinks

	@property        
	def list_inventory(self, inv):
		attr_list = vars(inv)
		return attr_list
#-----------------------------------------------------
	def delete_ingredient(self, name):  
#-----------------------------------------------------
		if self.get_ingredient(name) == None:
			return f'Ingredient doesnt exist'
		kind = self.get_ingredient(name).kind

		if kind == 'bread':					  
			del self._bread[name] 
		elif kind == 'pattie':
			del self._pattie[name] 
		elif kind == 'filling':
			del self._fillings[name] 
		elif kind == 'side':
			del self._pattie[name] 
		elif kind == 'drink':
			del self._drinks[name] 
		self.update_pickle()

#-----------------------------------------------------
	def update_ingredient(self, ingredient, amount):
#-----------------------------------------------------
		ingredient = self.get_ingredient(ingredient)
		ingredient.update_stock(amount)
		self.update_pickle()
		return ingredient.stock

#-----------------------------------------------------
	def get_ingredient(self, ingredient):
#-----------------------------------------------------

		if self._bread.get(ingredient) is not None:
			return self._bread.get(ingredient)
		elif self._patties.get(ingredient) is not None:
			return self._patties.get(ingredient)
		elif self._fillings.get(ingredient) is not None:
			return self._fillings.get(ingredient)
		elif self._sides.get(ingredient) is not None:
			return self._sides.get(ingredient)
		elif self._drinks.get(ingredient) is not None:
			return self._drinks.get(ingredient)
		else:
			return None
		
#-----------------------------------------------------
	def new_ingredient(self, kind, name, cost, stock):  #inv_type = 'bread', 'pattie', 'fillings' etc
#-----------------------------------------------------
		ingredient = Ingredient(kind, name, stock, cost)
		self.add_ingredient(ingredient)
		self.update_pickle()
		return ingredient

	def add_ingredient(self, ingredient):
		if ingredient.kind == 'bread':
			self._bread[ingredient.name] = ingredient
			return ingredient
		elif ingredient.kind == 'pattie':
			self._patties[ingredient.name] = ingredient
			return ingredient
		elif ingredient.kind == 'filling':
			self._fillings[ingredient.name] = ingredient
			return ingredient
		elif ingredient.kind == 'side':
			self._sides[ingredient.name] = ingredient
			return ingredient
		elif ingredient.kind == 'drink':
			self._drinks[ingredient.name] = ingredient
			return ingredient
		else:
			return None

#-----------------------------------------------------
	def update_cost(self, name, price):
#-----------------------------------------------------
		ingredient = self.get_ingredient(name)

		if self.get_ingredient(name) == None:
			return f'Ingredient doesnt exist'

		try:
			price = int(price)
		except ValueError:
			return f'Invalid Input'

		ingredient.set_cost(price)
		self.update_pickle()

	def update_pickle(self):

		f = open("food.pickle","wb")
		for ingredient in self.bread:
			pickle.dump(self.get_ingredient(ingredient),f)
		for ingredient in self.patties:
			pickle.dump(self.get_ingredient(ingredient),f)
		for ingredient in self.fillings:
			pickle.dump(self.get_ingredient(ingredient),f)
		for ingredient in self.drinks:
			pickle.dump(self.get_ingredient(ingredient),f)
		for ingredient in self.sides:
			pickle.dump(self.get_ingredient(ingredient),f)
		f.close()


#-----------------------------------------------------
	def __str__(self):
#-----------------------------------------------------
		attr = vars(self)
		return str(attr)





