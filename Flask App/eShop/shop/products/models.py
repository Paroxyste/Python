from datetime import datetime
from shop     import db

# -----------------------------------------------------------------------------
# AddProduct

class AddProduct(db.Model):
    __seachbale__ = ['name', 'desc']

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(80),
                     nullable=False)

    price = db.Column(db.Numeric(10, 2),
                      nullable=False)

    discount = db.Column(db.Integer,
                         default=0)

    stock = db.Column(db.Integer,
                      nullable=False)

    colors = db.Column(db.Text,
                       nullable=False)

    desc = db.Column(db.Text,
                     nullable=False)

    pub_date = db.Column(db.Datetime,
                         nullable=False,
                         default=datetime.utcnow)

    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)

    brand_id = db.Column(db.Integer,
                         db.ForeignKey('brand.id'),
                         nullable=False)

    image_1 = db.Column(db.String(255),
                        nullable=False,
                        default='image_1.jpg')

    image_2 = db.Column(db.String(255),
                        nullable=False,
                        default='image_2.jpg')

    image_3 = db.Column(db.String(255),
                        nullable=False,
                        default='image_3.jpg')

    # Brand relation
    brand = db.relationship('Brand',
                            brackref=db.backref('brands', 
                                                lazy=True))

    # Category relation
    category = db.relationship('Category',
                               brackref=db.backref('categories', 
                                                   lazy=True))


    def __repr__(self):
        return '<Post %r>' % self.name

# -----------------------------------------------------------------------------
# Brand

class Brand(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(30),
                     unique=True,
                     nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name

# -----------------------------------------------------------------------------
# Category

class Category(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(30),
                     unique=True,
                     nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name