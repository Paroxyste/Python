from datetime    import datetime
from flask_login import UserMixin
from shop        import db, login_manager

import json

# -----------------------------------------------------------------------------
# user_loader

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

# -----------------------------------------------------------------------------
# CustomerOrder

class CustomerOrder(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)

    invoice = db.Column(db.String(20),
                        unique=True,
                        nullable=False)

    status = db.Column(db.String(20),
                       default='Pending',
                       nullable=False)

    customer_id = db.Column(db.Integer,
                            unique=False,
                            nullable=False)

    date_created = db.Column(db.DateTime,
                             default=datetime.utcnow,
                             nullable=False)

    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice

# -----------------------------------------------------------------------------
# JsonEncodedDict

class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if (value is None):
            return '{}'
        else :
            return json.dumps(value)

    def process_rsult_value(self, value, dialect):
        if (value is None):
            return {}
        else:
            return json.loads(value)

# -----------------------------------------------------------------------------
# Register

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(50),
                     unique=False)

    username = db.Column(db.String(50),
                         unique=True)

    email = db.Column(db.String(50),
                      unique=True)

    password = db.Column(db.String(255),
                         unique=False)

    country = db.Column(db.String(50),
                        unique=False)

    city = db.Column(db.String(50),
                     unique=False)

    contact = db.Column(db.String(50),
                        unique=False)

    address = db.Column(db.String(50),
                        unique=False)

    zipcode = db.Column(db.String(50),
                        unique=False)

    profile = db.Column(db.String(255),
                        unique=False,
                        default='default.jpg')

    date_created = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

# -----------------------------------------------------------------------------

db.create_all()