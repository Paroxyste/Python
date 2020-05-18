from .forms  import AddProducts
from .models import AddProduct, Brand, Category
from flask   import (flash, current_app, redirect, render_template, request,
                     session, url_for)
from shop    import app, db, photos, search

import os

# -----------------------------------------------------------------------------
# Functions

def brands():
    brands = Brand.query.join(AddProduct, 
                             (Brand.id == AddProduct.brand_id)) \
                        .all()

    return brands

def categories():
    categories = Category.query.join(AddProduct,
                                    (Category.id == AddProduct.category_id)) \
                                .all()

    return categories

# -----------------------------------------------------------------------------
# Brand : add new brand

# -----------------------------------------------------------------------------
# Brand : delete brand

# -----------------------------------------------------------------------------
# Brand : get brand id

# -----------------------------------------------------------------------------
# Brand : update brand

# -----------------------------------------------------------------------------
# Categories : add new category

# -----------------------------------------------------------------------------
# Categories : delete category

# -----------------------------------------------------------------------------
# Categories : update category

# -----------------------------------------------------------------------------
# Product : add new product

# -----------------------------------------------------------------------------
# Product : delete product

# -----------------------------------------------------------------------------
# Product : get product id

# -----------------------------------------------------------------------------
# Product : update product

# -----------------------------------------------------------------------------
# Search results

@app.route('/result')
def result():
    search_word = request.args.get('q')
    products    = AddProduct.query.msearch(search_word, 
                                           fields=['name', 'desc'],
                                           limit=6)

    render_template('products/result.html',
                    products=products,
                    brands=brands(),
                    categories=categories())
# -----------------------------------------------------------------------------
# Root

@app.route('/')
def home():
    page     = request.args.get('page', 1, type=int)
    products = AddProduct.query.filter(AddProduct.stock > 0) \
                               .order_by(AddProduct.id.desc()) \
                               .paginate(page=page, per_page=9)

    return render_template('products/index.html', 
                           products=products,
                           brands=brands(),
                           categories=categories())