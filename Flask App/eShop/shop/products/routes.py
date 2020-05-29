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

    return render_template('products/index.html',
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

@app.route('/addcat', methods=['GET', 'POST'])
def add_cat():
    if (request.method == 'POST'):
        get_cat  = request.form.get('category')
        category = Category(name=get_cat)

        db.session.add(category)

        flash(f'The brand {get_cat} was added to your database',
              'success')

        db.session.commit()

        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html',
                           title='Add Category')

# -----------------------------------------------------------------------------
# Categories : delete category

@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def delete_cat(id):
    get_cat = Category.query.get_or_404(id)

    if (request.method == 'POST'):
        db.session.delete(get_cat)

        flash(f'The brand {get_cat.name} was deleted from your database',
              'danger')

        db.session.commit()

        return redirect(url_for('admin'))

    flash(f'The brand {get_cat.name} can\'t be deleted from your database',
          'warning')

    return redirect(url_for('admin'))

# -----------------------------------------------------------------------------
# Categories : update category

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def update_cat(id):
    if ('email' not in session):
        flash('Login first please',
              'danger')
        
        return redirect(url_for('login'))

    update_cat   = Category.query.get_or_404(id)
    get_category = request.form.get('category')

    if (request.method == 'POST'):
        update_cat.name = get_category

        flash(f'The category {update_cat.name} was changed to {get_category}',
              'success')

        db.session.commit()

        return redirect(url_for('categories'))

    get_category = update_cat.name

    return render_template('products/addbrand.html',
                           title='Update Cat',
                           update_cat=update_cat)

# -----------------------------------------------------------------------------
# Product : add new product

@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    form       = AddProducts(request.form)
    brands     = Brand.query.all()
    categories = Category.query.all()

    if (request.method == 'POST' and 'image_1' in request.files):
        name     = form.name.data
        price    = form.price.data
        discount = form.discount.data
        stock    = form.stock.data
        colors   = form.colors.data
        desc     = form.description.data

        get_brand    = request.form.get('brand')
        get_category = request.form.get('category')

        image_1 = photos.save(request.files.get('image_1'),
                              name=os.urandom(10).hex() + '.')
        image_2 = photos.save(request.files.get('image_2'),
                              name=os.urandom(10).hex() + '.')
        image_3 = photos.save(request.files.get('image_3'),
                              name=os.urandom(10).hex() + '.')

        add_product = AddProduct(name=name,
                                 price=price,
                                 discount=discount,
                                 stock=stock,
                                 colors=colors,
                                 desc=desc,
                                 category_id=get_category,
                                 brand_id=get_brand,
                                 image_1=image_1,
                                 image_2=image_2,
                                 image_3=image_3)

        db.session.add(add_product)

        flash(f'The product {name} was added in database',
              'success')
        
        db.session.commit()

        return redirect(url_for('admin'))
    
    return render_template('products/addproduct.html',
                           form=form,
                           title='Add Product',
                           brands=brands,
                           categories=categories)

# -----------------------------------------------------------------------------
# Product : delete product

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def delete_product(id):
    get_product = AddProduct.query.get_or_404(id)

    if (request.method == 'POST'):
        try:
            os.unlink(os.path.join(current_app.root_path,
                                   'static/images' + get_product.image_1))

            os.unlink(os.path.join(current_app.root_path,
                                   'static/images' + get_product.image_2))

            os.unlink(os.path.join(current_app.root_path,
                                   'static/images' + get_product.image_3))

        except Exception as e:
            print(e)

        db.session.delete(get_product)
        db.session.commit()

        flash(f'The product {get_product.name} was delete from your database !',
              'success')

        return redirect(url_for('admin'))

    flash(f'Can\'t delete the product',
          'danger')

    return redirect(url_for('admin'))

# -----------------------------------------------------------------------------
# Product : get product id

@app.route('/product/<int:id>')
def get_product(id):
    get_product = AddProduct.query.get_or_404(id)

    return render_template('products/single_page.html',
                           get_product=get_product,
                           brands=brands(),
                           categories=categories())

# -----------------------------------------------------------------------------
# Product : update product

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    form        = AddProducts(request.form)
    get_product = AddProduct.query.get_or_404(id)
    brands      = Brand.query.all()
    categories  = Category.query.all()

    get_brand    = request.form.get('brand')
    get_category = request.form.get('category')

    if (request.method == 'POST'):
        get_product.name     = form.name.data
        get_product.price    = form.price.data
        get_product.discount = form.discount.data
        get_product.stock    = form.stock.data
        get_product.colors   = form.colors.data
        get_product.dec      = form.description.data

        get_product.category_id = get_category
        get_product.brand_id    = get_brand

        #  Image 1
        if (request.files.get('image_1')):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       'static/images/' + get_product.image_1))

                get_product.image_1 = photos.save(request.files.get('image_1'),
                                                  name=os.urandom(10).hex() + '.')

            except:
                get_product.image_1 = photos.save(request.files.get('image_1'),
                                                  name=os.urandom(10).hex() + '.')

        #  Image 2
        if (request.files.get('image_2')):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       'static/images/' + get_product.image_2))

                get_product.image_2 = photos.save(request.files.get('image_2'),
                                                  name=os.urandom(10).hex() + '.')

            except:
                get_product.image_2 = photos.save(request.files.get('image_2'),
                                                  name=os.urandom(10).hex() + '.')

        #  Image 3
        if (request.files.get('image_3')):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       'static/images/' + get_product.image_3))

                get_product.image_3 = photos.save(request.files.get('image_3'),
                                                  name=os.urandom(10).hex() + '.')

            except:
                get_product.image_3 = photos.save(request.files.get('image_3'),
                                                  name=os.urandom(10).hex() + '.')

        flash('The product was updated !',
              'success')

        db.session.commit()

        return redirect(url_for('admin'))

    form.name.data        = get_product.name
    form.price.data       = get_product.price
    form.discount.data    = get_product.discount
    form.stock.data       = get_product.stock
    form.colors.data      = get_product.colors
    form.description.data = get_product.desc

    get_brand    = get_product.brand.name
    get_category = get_product.category.name

    return render_template('products/addproduct.html',
                           form=form,
                           title='Update Product',
                           get_product=get_product,
                           brands=brands,
                           categories=categories)

# -----------------------------------------------------------------------------
# Products page

@app.route('/')
def products_page():
    page     = request.args.get('page', 1, type=int)
    products = AddProduct.query.filter(AddProduct.stock > 0) \
                               .order_by(AddProduct.id.desc()) \
                               .paginate(page=page, per_page=9)

    return render_template('products/index.html', 
                           products=products,
                           brands=brands(),
                           categories=categories())

# -----------------------------------------------------------------------------
# Search results

@app.route('/result')
def result():
    search_word = request.args.get('q')

    
    if search_word == None:
        return redirect(url_for('products_page'))
    else:
        products    = AddProduct.query.msearch(search_word, 
                                            fields=['name', 'desc'],
                                            limit=6)



    render_template('products/result.html',
                    products=products,
                    brands=brands(),
                    categories=categories())