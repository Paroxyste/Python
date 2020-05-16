from flask import (current_app, flash, make_response, redirect, 
                   render_template, request, session, url_for)

from flask_login import current_user, login_required, login_user, logout_user
from shop        import app, bcrypt, db, login_manager, photos, search

from .forms import CustomerLoginFrom, CustomerRegisterForm
from .model import CustomerOrder, Register

import json
import os
import pdfkit
import secrets

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

