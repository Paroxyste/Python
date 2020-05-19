from .forms  import LoginForm, RegisterForm
from .models import User
from flask   import (flash, redirect, render_template, request, session, 
                     url_for)
from shop    import app, bcrypt, db

from shop.products.models import AddProduct, Brand, Category

# ------------------------------------------------------------------------------
# Admin

@app.route('/admin')
def home():
    products = AddProduct.query.all()

    return render_template('admin/index.html',
                           title='Admin Page',
                           products=products)

# ------------------------------------------------------------------------------
# Brands

@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/brands.html',
                           title='Brands',
                           brands=brands)

# ------------------------------------------------------------------------------
# Categories

@app.route('/categories')
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/brands.html',
                           title='Categories',
                           categories=categories)

# ------------------------------------------------------------------------------
# Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()

        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            session['email'] = form.email.data

            flash(f'Welcome {form.email.data} you are connected now',
                  'success')

            return redirect(url_for('admin'))
        else:
            flash('Wrong email and password',
                  'danger')

            return redirect(url_for('login'))
    
    return render_template('admin/login.html',
                           title='Login Page',
                           form=form)

# ------------------------------------------------------------------------------
# Register

@app.route('/register')
def register():
    form = RegisterForm()

    if (form.validate_on_submit()):
        hash_password = bcrypt.generate_password_hash(form.password.data)

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hash_password)

        db.session.add(user)

        flash(f'Welcome {form.name.data} ! Thanks for registering',
              'success')

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('admin/register.html',
                           title='Registration Page',
                           form=form)