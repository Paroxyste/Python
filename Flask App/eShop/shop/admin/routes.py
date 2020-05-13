from flask import flash, redirect, render_template, request, session, url_for

from .forms  import LoginForm, RegistrationForm
from .models import User

from shop  import app, bcrypt, db

from shop.products.models import AddProduct, Brand, Category

# ------------------------------------------------------------------------------
# Admin

@app.route('/admin')
def home():
    products = AddProduct.query.all()

    return render_template('admin/index.html',
                           title    = 'Admin Page',
                           products = products)

# ------------------------------------------------------------------------------
# Brands

@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/brands.html',
                           title = 'Brands',
                           brands = brands)

# ------------------------------------------------------------------------------
# Categories

@app.route('/categories')
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/brands.html',
                           title = 'Categories',
                           categories = categories)

# ------------------------------------------------------------------------------
# Login

# ------------------------------------------------------------------------------
# Register

@app.route('/register')
def register():
    return render_template('admin/register.html', title = 'Register')