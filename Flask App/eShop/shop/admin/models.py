from datetime import datetime
from shop     import db

# -----------------------------------------------------------------------------
# User

class Admin(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)

    firstname = db.Column(db.String(50), 
                          unique=False, 
                          nullable=False)

    lastname = db.Column(db.String(50), 
                         unique=False, 
                         nullable=False)

    username = db.Column(db.String(50), 
                         unique=True, 
                         nullable=False)

    email = db.Column(db.String(100), 
                      unique=True, 
                      nullable=False)

    password = db.Column(db.String(255), 
                         unique=False, 
                         nullable=False)

    profile  = db.Column(db.String(180), 
                         unique=False, 
                         nullable=False, 
                         default='default.jpg')

    def __repr__(self):
        return '<Admin %r>' % self.username

# -----------------------------------------------------------------------------

db.create_all()