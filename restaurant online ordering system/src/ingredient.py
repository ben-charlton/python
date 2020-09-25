
class Ingredient():

	def __init__(self, kind, name, stock, cost, size = {}):

		self._kind = kind.lower()
		self._name = name.lower()
		self._stock = stock
		self._cost = cost
		self._size = size

# PROPERTIES
	@property 
	def kind(self):
		return self._kind

	@property 
	def name(self):
		return self._name

	@property 
	def stock(self):
		return self._stock

	@property
	def stock(self):
		return self._stock

	@property 
	def cost(self):
		return self._cost

	@property
	def size(self):
		return self._size
	

# UPDATE PROPERTIES
	def update_stock(self, amount):
		self._stock += amount
		if self.stock < 0:
			self._stock = 0

	def set_cost(self, amount):
		self._cost = amount


	def __str__(self):

		return f'Ingredient: {self.name}, Stock: {self.stock}, Cost {self.cost}'
	

