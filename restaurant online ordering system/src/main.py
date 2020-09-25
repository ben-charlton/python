from src.ingredient import Ingredient

class Main():

    def __init__(self, bread, fillings, pattie, numBuns, numPatties):
        self._bread = bread
        self._numBuns = numBuns
        self._fillings = fillings
        self._pattie = pattie
        self._numPatties = numPatties

    @property
    def bread(self):
        return self._bread

    def get_bread(self):
        return self._bread

    @property
    def numBuns(self):
        return self._numBuns

    def get_numBuns(self):
        return self._numBuns

    @property
    def fillings(self):
        return self._fillings

    def get_fillings(self):
        return self._fillings

    @property
    def pattie(self):
        return self._pattie

    def get_pattie(self):
        return self._pattie

    @property
    def numPatties(self):
        return self._numPatties

    def get_numPatties(self):
        return self._numPatties

# ------------------------------------------
    def calculate_price(self):
# ------------------------------------------
        price = self.bread.cost * self.numBuns
        for item in self.fillings:
            price += item.cost
        if self.pattie is not None and self.numPatties is not None:
            price += self.pattie.cost * self.numPatties

        return price

# ----------------------------------------------
    def decrease_stock(self):
# ----------------------------------------------
        self.bread.update_stock(-self.numBuns)
        if self.pattie is not None and self.numPatties is not None:
            self.pattie.update_stock(-self.get_numPatties())

        for filling in self.fillings:
            filling.update_stock(-1)

# ------------------------------------------
    def __str__(self):
# ------------------------------------------
        output = ''
        output += f'Main: {self.bread.name} with {self.numPatties} {self.pattie.name} patties and these fillings:'
        for filling in self.fillings:
            output+= f'{filling.name}, '
        output += ''
        return output

 
