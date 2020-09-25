from src.ingredient import Ingredient
from src.inventory import Inventory
import pickle

f = open("food.pickle","wb")

i = Ingredient('bread','white wrap',100,3)

pickle.dump(i,f)

i = Ingredient('bread','wholegrain wrap',100,3)

pickle.dump(i,f)

i = Ingredient('bread','glutenfree wrap',100,4)

pickle.dump(i,f)

i = Ingredient('bread','wrap',100,3)

pickle.dump(i,f)

i = Ingredient('bread','muffin',100,3)

pickle.dump(i,f)

i = Ingredient('bread','sesame seed',100,4)

pickle.dump(i,f)

i = Ingredient('bread','wholegrain',100,4)

pickle.dump(i,f)

i = Ingredient('bread','glutenfree',1,5)

pickle.dump(i,f)

i = Ingredient('pattie','veggie',100,4)

pickle.dump(i,f)

i = Ingredient('pattie','beef',100,4)

pickle.dump(i,f)

i = Ingredient('pattie','chicken',100,4)

pickle.dump(i,f)

i = Ingredient('filling','lettuce',100,1)

pickle.dump(i,f)

i = Ingredient('filling','tomato',100,1)

pickle.dump(i,f)

i = Ingredient('filling','swiss cheese',100,1)

pickle.dump(i,f)

i = Ingredient('filling','cheddar cheese',100,1)

pickle.dump(i,f)

i = Ingredient('filling','pickles',0,1)

pickle.dump(i,f)

i = Ingredient('filling','beetroot',100,1)

pickle.dump(i,f)

i = Ingredient('filling','pineapple',100,1)

pickle.dump(i,f)

i = Ingredient('side','chips',10000,0.04,{'Small':75, 'Medium':125})

pickle.dump(i,f)

i = Ingredient('side','nuggets',100,1,{'Small':3,'Medium':6})

pickle.dump(i,f)

i = Ingredient('side','chocolate sundae',100,1,{'Small':3,'Medium':5, 'Large':7})

pickle.dump(i,f)

i = Ingredient('side','strawberry sundae',100,1,{'Small':3,'Medium':5, 'Large':7})

pickle.dump(i,f)

i = Ingredient('drink','Coke Can',100,2 ,{'Can':1})

pickle.dump(i,f)

i = Ingredient('drink','Coke Bottle',100,4 ,{'Bottle':1})

pickle.dump(i,f)

i = Ingredient('drink','Sprite Can',100,2 ,{'Can':1})

pickle.dump(i,f)

i = Ingredient('drink','Sprite Bottle',100,4 ,{'Bottle':1})

pickle.dump(i,f)

i = Ingredient('drink','Fanta Can',100,2 ,{'Can':1})

pickle.dump(i,f)

i = Ingredient('drink','Fanta Bottle',100,4 ,{'Bottle':1})

pickle.dump(i,f)

i = Ingredient('drink','orange juice',100,2,{'Small':1,'Medium':2, 'Large':3})

pickle.dump(i,f)

i = Ingredient('drink','apple juice',100,2,{'Small':1,'Medium':2, 'Large':3})

pickle.dump(i,f)

i = Ingredient('drink','water',100,2,{'Small':1,'Medium':2, 'Large':3})

pickle.dump(i,f)

f.close()
with open("food.pickle","rb") as f:
    inv = Inventory()

    while True:

        try:

            obj = pickle.load(f)
            print(obj.kind)
            obj2 = inv.add_ingredient(obj)
            print(obj2.name)
        except EOFError:
            break
f.close()
