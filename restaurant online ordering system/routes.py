from flask import render_template, request, redirect, url_for, abort, session, Response
from server import app, system
from datetime import datetime
from src.main import Main
from src.customer import Customer
from src.order import Order
from src.ingredient import Ingredient
from src.inventory import Inventory
from src.restaurant_system import RestaurantSystem
from collections import OrderedDict
import copy
from functools import wraps


# -----------------------------------------------------------
'''
Dedicated page for "page not found"
'''
# -----------------------------------------------------------
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):

    return render_template('404.html'), 404

def check_auth(username, password):

    return username == 'admin' and password == 'Lithub'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# -----------------------------------------------------------
'''
Home page, instantiate order 
'''
# -----------------------------------------------------------
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == 'POST':    
        #create customer
        customer_id = system.create_customer()
        customer = system._customers[customer_id]
        #create order for that ID   
        order = system.create_order(customer)
        orderID = order.orderID
        return redirect(url_for('order', orderID=orderID))
    return render_template('home.html')


# -----------------------------------------------------------
'''
Begin order 
'''
# -----------------------------------------------------------
@app.route('/create', methods=["GET", "POST"])
def order():
    
    inventory = system.inventory
    orderID = int(request.args.get('orderID'))
    cost = system.get_order(orderID).calculate_total()


    if request.method == 'POST':
        if request.form["order"] == "Create Custom Burger":
            return redirect(url_for('custom', orderID=orderID))
        if request.form["order"] == "Create Custom Wrap":
            return redirect(url_for('wrap', orderID=orderID))
        elif request.form["order"] == "Choose Base Burger":
            return redirect(url_for('base', orderID=orderID))
        elif request.form["order"] == "Sides":
            return redirect(url_for('sides', orderID=orderID))
        elif request.form["order"] == "Drinks":
            return redirect(url_for('drinks', orderID=orderID))
        elif request.form["order"] == "Proceed to Checkout":
            system.checkout(orderID)
            return redirect(url_for('checkout', orderID=orderID))

    return render_template('order.html', inventory=inventory, cost=cost)





# -----------------------------------------------------------
'''
Create custom burger
'''
# -----------------------------------------------------------
@app.route('/create/customburger', methods=["GET", "POST"])
def custom():
   
    inventory = system.inventory
    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)


    if request.method == 'POST':
        pattie_type = request.form["pattie"]
        numBuns = request.form["numBuns"] 
        if numBuns != "None":
            numBuns = int(numBuns)
        bread_type = request.form["bread"]
        numPatties = request.form["numPatties"]
        if numPatties != "None":
            numPatties = int(numPatties)
        filling_list = request.form.getlist("fillings") 

        if pattie_type == "None" or numBuns == "None"or bread_type == "None" or (numPatties == "None" and pattie_type != "0"):
            select_error = "Please select an option for each field"
            return render_template('custom.html', select_error=select_error, inventory=inventory)

        if pattie_type == "0" and numPatties != "None":
            check_error = "Please don't select number of patties if no pattie type selected"
            return render_template('custom.html', check_error=check_error, inventory=inventory)       

        bread = [bread_type, numBuns]
        if pattie_type != "0":
            pattie = [pattie_type, numPatties]
        else:
            pattie = None

        if filling_list == []:
            filling_list = None

        order.create_main(inventory, bread, pattie, filling_list)

        return redirect(url_for('order', orderID=orderID))

    return render_template('custom.html', inventory=inventory )

# -----------------------------------------------------------
'''
Create custom wrap
'''
# -----------------------------------------------------------
@app.route('/create/customwrap', methods=["GET", "POST"])
def wrap():
   
    inventory = system.inventory
    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)


    if request.method == 'POST':
        pattie_type = request.form["pattie"]        
        bread_type = request.form["bread"]
        filling_list = request.form.getlist("fillings") 

        if pattie_type == "None" or bread_type == "None":
            select_error = "Please select an option for each field"
            return render_template('wrap.html', select_error=select_error, inventory=inventory)

        if filling_list == []:
            filling_list = None
    
        bread = [bread_type, 1]
        pattie = [pattie_type, 1]

        if pattie_type == "0":
            order.create_main(inventory, bread, filling_list)

        else: 
            order.create_main(inventory, bread, pattie, filling_list)
            
        return redirect(url_for('order', orderID=orderID))

    return render_template('wrap.html', inventory=inventory )


# -----------------------------------------------------------
'''
Base burger
'''
# -----------------------------------------------------------
@app.route('/create/baseburger', methods=["GET", "POST"])
def base():
   
    inventory = system.inventory
    select_error = None
    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)

    if request.method == 'POST':
    
        choices = request.form
        for item in choices:
            fillings = ['tomato','lettuce', 'cheddar cheese']
            if item == 'beefBurger':
                order.create_main(inventory, ['sesame seed', 2], ['beef', 1], fillings)
            if item == 'chickenBurger':
                order.create_main(inventory, ['sesame seed', 2], ['chicken', 1], fillings)
            if item == 'veggieBurger':
                order.create_main(inventory, ['sesame seed', 2], ['veggie', 1], fillings)
            if item == 'beefWrap':
                order.create_main(inventory, ['white wrap', 1], ['beef', 1], fillings)
            if item == 'chickenWrap':
                order.create_main(inventory, ['white wrap', 1], ['chicken', 1], fillings)
            if item == 'veggieWrap':
                order.create_main(inventory, ['white wrap', 1], ['veggie', 1], fillings)

        return redirect(url_for('order', orderID=orderID))

    return render_template('base_burger.html', inventory=inventory)





# -----------------------------------------------------------
'''
Sides
'''
# -----------------------------------------------------------
@app.route('/create/sides', methods=["GET", "POST"])
def sides():
    
    inventory = system.inventory 
    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)

    if request.method == 'POST':
        side_list = request.form.getlist('side') 
        size_list = request.form.getlist('size')
        quantity_list = request.form.getlist('quantity')

        for side in side_list:
            i = 0
            for side_name, s in inventory.sides.items():
                if side_name.lower() == side.lower():
                    index = i
                i += 1
            if size_list[index] == None or size_list[index] == 'None':
                select_error = "Please select a size"
                return render_template('sides.html', select_error=select_error, inventory=inventory)

            if int(quantity_list[index]) < 1 or int(quantity_list[index]) > 10:
                select_error = "Please enter a valid quantity (max 10)"
                return render_template('sides.html', select_error=select_error, inventory=inventory)
            for x in range(int(quantity_list[index])):
                order.add_item(system.inventory, side, size_list[index])
                
        return redirect(url_for('order', orderID=orderID))
        
    return render_template('sides.html', inventory=inventory)




# -----------------------------------------------------------
'''
Drinks
'''
# -----------------------------------------------------------
@app.route('/create/drinks', methods=["GET", "POST"])
def drinks():
    
    inventory = system.inventory 
    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)

    if request.method == 'POST':

        drink_list = request.form.getlist('drink') 
        if len(drink_list) == 0:
            select_error = "Please select a drink"
            return render_template('drinks.html', select_error=select_error, inventory=inventory)
        size_list = request.form.getlist('size')
        quantity_list = request.form.getlist('quantity')
    
        drinks = []

        for drink in system.inventory.drinks:
            drink = system.inventory.get_ingredient(drink)
            if len(drink.size) == 1 and drink.stock > 10:
                drinks.append(drink.name)
            elif drink.stock > 10:
                drinks.append(drink.name)

        for drink in drink_list:
            index = drinks.index(drink)
            if size_list[index] == None or size_list[index] == 'None':
                select_error = "Please select a size"
                return render_template('drinks.html', select_error=select_error, inventory=inventory)
            if int(quantity_list[index]) < 1 or int(quantity_list[index]) > 10:
                select_error = "Please enter a valid quantity (max 10)"
                return render_template('drinks.html', select_error=select_error, inventory=inventory)
            for x in range(int(quantity_list[index])):
                if size_list[index] == 'N/A':
                    order.add_item(system.inventory, drink)
                else:
                    order.add_item(system.inventory, drink, size_list[index])  
        return redirect(url_for('order', orderID=orderID))
        
    return render_template('drinks.html', inventory=inventory)



# -----------------------------------------------------------
'''
Checkout order
'''
# -----------------------------------------------------------
@app.route('/checkout', methods=["GET", "POST"])
def checkout():

    orderID = int(request.args.get('orderID'))
    order = system.get_order(orderID)
    cost = system.get_order(orderID).calculate_total()

    return render_template('checkout.html', order=order, cost = cost)

# -----------------------------------------------------------
'''
Cancel order
'''
# -----------------------------------------------------------
@app.route('/cancel', methods=["GET", "POST"])
def cancel():

    print('cancelling order')

    # pop most recent item off order dict (i.e. the current order)
    ood = OrderedDict(system._orders)
    if ood:
        ood.popitem()
        system._orders = ood
    # clear customer id for this order
    cod = OrderedDict(system._customers)
    if cod:
        cod.popitem()  
        system._customers = cod

    return redirect(url_for('index'))


# -----------------------------------------------------------
'''
Staff view current orders
'''
# -----------------------------------------------------------
@app.route('/staff/stafforders', methods=["GET", "POST"])
def staff_view_orders():

    orderIDs = system.view_all_orders()
    orders = []
    for orderID in orderIDs:
        orders.append(system.get_order(orderID))

    if request.method == "POST" and 'confirm' in request.form: 
        if request.form["update"] != "None":
            orderID = int(request.form["key"])
            order = system.get_order(orderID)
            system.update_order_status(orderID,int(request.form["update"]))
            return render_template('staff_orders.html', orders=orders)

    if request.method == "POST" and 'collected' in request.form: 
        orderID = int(request.form["key"])
        order = system.get_order(orderID)
        system.update_order_status(orderID,int(2))
        return render_template('staff_orders.html', orders=orders)

    if request.method == "POST" and 'archive_orders' in request.form: 
        return redirect(url_for('archive_orders'))

    return render_template('staff_orders.html', orders=orders)

# -----------------------------------------------------------
'''
Staff view archived orders
'''
# -----------------------------------------------------------
@app.route('/staff/stafforders/archive', methods=["GET", "POST"])
def archive_orders():


    if request.method == "POST" and 'delete' in request.form: 
        orderID = int(request.form["key"]) 
        system.delete_order(orderID)
        orderIDs = system.view_archive_orders()
        orders = []
        for order in orderIDs:
            orders.append(system.get_order(order))
        return render_template('archive.html', orders=orders)

    if request.method == "POST" and 'delete_all' in request.form: 
        orderIDs = system.view_archive_orders()
        orders = []
        for orderID in orderIDs:
            system.delete_order(orderID)
        return render_template('archive.html', orders=[])
    
    orderIDs = system.view_archive_orders()
    orders = []
    for orderID in orderIDs:
        orders.append(system.get_order(orderID))

    return render_template('archive.html', orders=orders)

# -----------------------------------------------------------
'''
Staff update inventory 
'''
# -----------------------------------------------------------
@app.route('/staff/staffinventory', methods=["GET", "POST"])
def staff_update_inventory():

    inventory = system.inventory


    if request.method == 'POST':
        try:
            button = request.form['button']
            if button == 'Choose':
                name = request.form["Ingredient"] 
                ingredient = system.inventory.get_ingredient(name) 
                if ingredient == None:
                    return render_template('staff_inventory.html', inventory=inventory, button= 'Choose', error = 'Ingredient doesnt exist')
                else:
                    stock = system.inventory.get_ingredient(name).stock
                    return render_template('staff_inventory.html', inventory=inventory, button= 'Set', ingredient=name, stock = stock)
            elif button == 'Set':
                name = request.form["Ingredient"] 
                stock = system.inventory.get_ingredient(name).stock
                ingredient = system.inventory.get_ingredient(name) 
                amount = int(request.form["amount"])
                new_stock = system.update_inventory(name, amount) 
                return render_template('staff_inventory.html', inventory=inventory, button= 'Confirm', ingredient=name, stock = stock, new_stock = new_stock, amount = amount)
            elif button == 'Confirm':
                print('confirm')
        except:
            return render_template('staff_inventory.html', inventory=inventory, button= 'Choose')


     
    return render_template('staff_inventory.html', inventory=inventory, button= 'Choose')

# -----------------------------------------------------------
'''
Customer check order status
'''
# -----------------------------------------------------------
@app.route('/checkorder', methods=["GET", "POST"])
def customer_check_order():

    if request.method == 'POST':
        order_id = request.form['order_id']
        order = system.get_order(order_id)
        status = system.check_order_status(order_id)
        if status == 0:
            return render_template('order_status.html', status = 'unavaliable', order_id = order_id, order = order)
        elif status == 1:
            return render_template('order_status.html', status = 'avaliable',order_id = order_id, order = order)
        elif status == -1:
            return render_template('order_status.html', status = 'not confirmed', order_id = order_id, order = order)
        elif status == 2:
            return render_template('order_status.html', status = 'Archived', order_id = order_id, order = order)
        else:
            return render_template('order_status.html', error = status)

    return render_template('order_status.html')


# -----------------------------------------------------------
'''
List orders
'''
# -----------------------------------------------------------

@app.route('/listorders', methods=["GET", "POST"])
def list_orders():

    return render_template("list.html", orders = system.orders)



@app.route('/staff', methods=["GET", "POST"])
@requires_auth
def staff():
    return render_template("staff.html")
