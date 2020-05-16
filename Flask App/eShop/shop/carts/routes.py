from flask import (current_app, redirect, render_template, request, 
                  session, url_for)
from shop  import app, db

from shop.products.models import AddProduct
from shop.products.routes import brands, categories

import json

def MagerDicts(dict1, dict2):
    if (isinstance(dict1, list) and isinstance(dict2, list)):
        return dict1 + dict2

    if (isinstance(dict1, dict) and isinstance(dict2, dict)):
        return dict(list(dict1.items()) + list(dict2.items()))

# -----------------------------------------------------------------------------
# Add carts

@app.route('/addcart', methods = ['POST'])
def AddCart():
    try:
        product_id =  request.form.get('product_id')
        quantity   = int(request.form.get('quantity'))
        color      = request.form.get('colors')
        product    = AddProduct.query.filter_by(id = product_id).first()

        if (request.method == 'POST'):
            DictItems = {product_id :
                            {'name': product.name,
                             'price': product.price,
                             'discount': product.discount,
                             'colors': colors,
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
                    session['ShoppingCart'] = MagerDicts(
                                                session['ShoppingCart'], 
                                                DictItems
                                            )

                    return redirect(request.referrer)

            else:
                session['ShoppingCart'] = DictItems

                return redirect(request.referrer)

    except Exception as e:
        print(e)

    finally: 
        return redirect(request.referrer)

# -----------------------------------------------------------------------------
# getCart

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
                           tax = tax,
                           grandtotal = grandtotal,
                           brands     = brands(),
                           categories = categories())

# -----------------------------------------------------------------------------