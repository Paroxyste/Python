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