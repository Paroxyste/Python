from flask import (current_app, flash, make_response, redirect, 
                   render_template, request, session, url_for)

from flask_login import current_user, login_required, login_user, logout_user
from shop        import app, bcrypt, db, login_manager, photos, search

from .forms import CustomerLoginFrom, CustomerRegisterForm
from .model import CustomerOrder, Register

import json
import os
import pdfkit

# -----------------------------------------------------------------------------
# Customer : login

@app.route('/customer/login', methods = ['GET', 'POST'])
def customerLogin():
    form = CustomerLoginFrom()

    if (form.validate_on_submit()):
        user = Register.query.filter_by(email = form.email.data).first()

        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)

            flash('You are login now !',
                  'success')
            
            next = request.args.get('next')

            return redirect(next or url_for('home'))
        
        flash('Incorrect email and password',
              'danger')

        return redirect(url_for('customerLogin'))
    
    return render_template('customer/login.html',
                           form = form)

# -----------------------------------------------------------------------------
# Customer : logout

@app.route('/customer/logout')
def customerLogout():
    logout_user()

    return redirect(url_for('home'))

# -----------------------------------------------------------------------------
# Customer : register

@app.route('/customer/register', methods = ['GET', 'POST'])
def customerRegister():
    form = CustomerRegisterForm()

    if (form.validate_on_submit()):
        hash_password = bcrypt.generate_password_hash(form.password.data)

        register = Register(name     = form.name.data,
                            username = form.username.data,
                            email    = form.email.data,
                            password = hash_password,
                            country  = form.country.data,
                            city     = form.city.data,
                            contact  = form.contact.data,
                            address  = form.adress.data,
                            zipcode  = form.zipcode.data)
        
        db.session.add(register)

        flash(f'Welcome { form.name.data } ! Thank You for registering',
              'success')

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('customer/register.html',
                           form = form)

# -----------------------------------------------------------------------------
# Order : get order

@app.route('/getorder')
@login_required
def getOrder():
    if (current_user.is_authenticated):
        customer_id = current_user.id
        invoice     = os.urandom(10).hex()

        try:
            order = CustomerOrder(invoice     = invoice,
                                  customer_id = customer_id,
                                  orders      = session['ShoppingCart'])

            db.session.add(order)
            db.session.commit()

            session.pop('ShoppingCart')

            flash('Your order has been sent successfully',
                  'success')

            return redirect(url_for('orders', 
                                    invoice = invoice))

        except Exception as e:
            print(e)

            flash('Something went wrong while get order',
                  'danger')

            return redirect(url_for('getCart'))

# -----------------------------------------------------------------------------
# Order : create order

@app.route('orders/<invoice>')
@login_required
def orders(invoice):
    if (current_user.is_authenticated):
        grandTotal  = 0
        subTotal    = 0
        customer_id = current_user.id
        customer    = Register.query.filter_by(id = customer_id).first()
        orders      = CustomerOrder.query.filter_by(customer_id = customer_id,
                                                    invoice = invoice) \
                                         .order_by(CustomerOrder.id.desc()) \
                                         .first()

        for _key, product in orders.orders.items():
            discount   = (product['discount'] / 100) * float(product['price'])
            subTotal  += float(product['price']) * int(product['quantity'])
            subTotal  -= discount
            tax        = ('%.2f' % (.06 * float(subTotal)))
            grandTotal = float('%.2f' % (1.06 * subTotal))
    
    else:
        return redirect(url_for(customerLogin))

    return render_template('customer/order.html',
                           invoice    = invoice,
                           tax        = tax,
                           subTotal   = subTotal,
                           grandTotal = grandTotal,
                           customer   = customer,
                           orders     = orders)

# -----------------------------------------------------------------------------
# Order : make pdf order