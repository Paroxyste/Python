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

@app.route('/addbrand.html', methods=['GET', 'POST'])
def add_brand():
    if (request.method == 'POST'):
        get_brand = request.form.get('brand')
        brand     = Brand(name=get_brand)

        db.session.add(brand)

        flash(f'The brand {get_brand} was added to your database',
              'success')

        db.session.commit()

        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html',
                           title='Add Brand',
                           brands='brands')

# -----------------------------------------------------------------------------
# Brand : delete brand

@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def delete_brand(id):
    get_brand = Brand.query.get_or_404(id)

    if (request.method == 'POST'):
        db.session.delete(get_brand)

        flash(f'The brand {get_brand.name} was deleted from your database',
              'success')

        db.session.commit()

        return redirect(url_for('admin'))

    flash(f'The brand {get_brand.name} can\'t be deleted from your database',
          'warning')

    return redirect(url_for('admin'))

# -----------------------------------------------------------------------------
# Brand : get brand id

@app.route('/brand/<int:id>')
def get_brand(id):
    page      = request.args.get('page', 1, type=int)
    get_brand = Brand.query.filter_by(id=id) \
                           .first_or_404()
    brand     = AddProduct.query.filter_by(brand=get_brand) \
                                .paginate(page=page,
                                          per_page=9)

    return render_template('product/index.html',
                           brand=brand,
                           brands=brands(),
                           categories=categories(),
                           get_brand=get_brand)

# -----------------------------------------------------------------------------
# Brand : update brand

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def update_brand():
    if ('email' not in session):
        flash('Login first please',
              'danger')

        return redirect(url_for('login'))

    update_brand = Brand.query.get_or_404(id)
    get_brand    = request.form.get('brand')

    if (request.method == 'POST') :
        update_brand.name = get_brand

        flash(f'The brand {update_brand.name} was changed to {get_brand}',
              'success')
        
        db.session.commit()

        return redirect(url_for('brands'))
    
    get_brand = update_brand.name

    return render_template('products/addbrand.html',
                           title='Update brand',
                           brands='brands',
                           update_brand=update_brand)
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