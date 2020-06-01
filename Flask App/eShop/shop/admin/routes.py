from .forms  import LoginForm, RegisterForm
from .models import Admin
from flask   import (flash, redirect, render_template, request, session, 
                     url_for)
from shop    import app, bcrypt, db

from shop.products.models import AddProduct, Brand, Category

# ------------------------------------------------------------------------------
# Admin

@app.route('/admin')
def admin():
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
def admin_login():
    form = LoginForm()

    if (form.validate_on_submit()):
        admin = Admin.query.filter_by(email=form.email.data).first()

        if (admin and bcrypt.check_password_hash(admin.password, form.password.data)):
            session['email'] = form.email.data

            flash(f'Welcome {form.email.data} you are connected now',
                  'success')

            return redirect(url_for('admin'))
        else:
            flash('Wrong email and password',
                  'danger')

            return redirect(url_for('admin_login'))
    
    return render_template('admin/login.html',
                           title='Login Page',
                           form=form)

# ------------------------------------------------------------------------------
# Register

@app.route('/register')
def admin_register():
    form = RegisterForm()

    if (form.validate_on_submit()):
        hash_password = bcrypt.generate_password_hash(form.password.data)

        admin = Admin(firstname=form.firstname.data,
                      lastname=form.lastname.data,
                      username=form.username.data,
                      email=form.email.data,
                      password=hash_password)

        db.session.add(admin)

        flash(f'Welcome {form.name.data} ! Thanks for registering',
              'success')

        db.session.commit()

        return redirect(url_for('admin_login'))

    return render_template('admin/register.html',
                           title='Registration Page',
                           form=form)