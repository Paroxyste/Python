from flask import (current_app, flash, redirect, render_template, request, 
                  session, url_for)
from shop  import app, db

from shop.products.models import AddProduct
from shop.products.routes import brands, categories

import json

# -----------------------------------------------------------------------------
# Functions

def mager_dicts(dict1, dict2):
    if (isinstance(dict1, list) and isinstance(dict2, list)):
        return dict1 + dict2

    if (isinstance(dict1, dict) and isinstance(dict2, dict)):
        return dict(list(dict1.items()) + list(dict2.items()))

# -----------------------------------------------------------------------------
# Cart : add item

@app.route('/addcart', methods=['POST'])
def addCart():
    try:
        product_id = request.form.get('product_id')
        quantity   = int(request.form.get('quantity'))
        color      = request.form.get('colors')
        product    = AddProduct.query.filter_by(id = product_id).first()

        if (request.method == 'POST'):
            dict_items = {product_id :
                            {'name': product.name,
                             'price': product.price,
                             'discount': product.discount,
                             'colors': color,
                             'quantity': quantity,
                             'image': product.image_1,
                             'colors': product.colors}
                        }

            if ('ShoppingCart' in session):
                print(session['ShoppingCart'])

                if (product_id in session['ShoppingCart']):
                    for key, item in session['ShoppingCart'].items():
                        if (int(key) == int(product_id)):
                            session.modified == True
                            item['quantity'] += 1
                else:
                    session['ShoppingCart'] = mager_dicts(
                                                session['ShoppingCart'], 
                                                dict_items
                                            )

                    return redirect(request.referrer)

            else:
                session['ShoppingCart'] = dict_items

                return redirect(request.referrer)

    except Exception as e:
        print(e)

    finally: 
        return redirect(request.referrer)

# -----------------------------------------------------------------------------
# Cart : clear cart

@app.route('/clearcart')
def clearCart():
    try:
        session.pop('ShoppingCart', None)

        return redirect(url_for('home'))

    except Exception as e:
        print(e)

# -----------------------------------------------------------------------------
# Cart : delete item

@app.route('/deleteitem/<int:id>')
def deleteItem(id):
    if ('ShoppingCart' not in session or len(session['ShoppingCart']) <= 0):
        return redirect(url_for('home'))

    try:
        session.modified = True

        for key, item in session['ShoppingCart'].items():
            if (int(key) == id):
                session['ShoppingCart'].pop(key, None)

                return redirect(url_for('getCart'))

    except Exception as e:
        print(e)

        return redirect(url_for('getCart'))

# -----------------------------------------------------------------------------
# Cart : get item

@app.route('/carts')
def getCart():
    if ('ShoppingCart' not in session or len(session['ShoppingCart']) <= 0):
        return redirect(url_for('home'))

    subtotal   = 0
    grandtotal = 0

    for key, product in session['ShoppingCart'].items():
        discount   = (product['discount'] / 100) * float(product['price'])
        subtotal  += float(product['price']) * int(product['quantity'])
        subtotal  -= discount
        tax        = ('%.2f' % (.06 * float(subtotal)))
        grandtotal = float('%.2f' % (1.06 * subtotal))

    return render_template('products/carts.html',
                           tax=tax,
                           grandtotal=grandtotal,
                           brands=brands(),
                           categories=categories())

# -----------------------------------------------------------------------------
# Cart : update cart

@app.route('/updatecart/<int:code>', methods = ['POST'])
def updateCart(code):
    if ('ShoppingCart' not in session or len(session['ShoppingCart']) <= 0):
        return redirect(url_for('home'))

    if (request.method == 'POST'):
        quantity = request.form.get('quantity')
        color    = request.form.get('color')

        try:
            session.modified == True

            for key, item in session['ShoppingCart'].items():
                if (int(key) == code):
                    item['quantity'] = quantity
                    item['color']    = color

                    flash('Item is updated !')

                    return redirect(url_for('getCart'))
        
        except Exception as e:
            print(e)

            return redirect(url_for('getCart'))