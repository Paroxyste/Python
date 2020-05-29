from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms        import (FloatField, Form, IntegerField, StringField,
                            TextAreaField)

from wtforms.validators import DataRequired, Length

class AddProducts(Form):
    name = StringField('Name',
                       validators=[DataRequired(), 
                                   Length(min=3, max=80)])

    price = StringField('Price',
                        validators=[DataRequired()])

    discount = IntegerField('Discount',
                            default=0)

    stock = IntegerField('Stock',
                         validators=[DataRequired(),
                                     Length(min=1)])

    colors = StringField('Colors',
                         validators=[DataRequired(),
                                     Length(min=3)])

    description = TextAreaField('Description',
                                validators=[DataRequired(),
                                            Length(min=3)])

    image_1 = FileField('Image 1',
                        validators=[FileRequired(),
                                    FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                'Image only please')])

    image_2 = FileField('Image 2',
                        validators=[FileRequired(),
                                    FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                'Image only please')])

    image_3 = FileField('Image 3',
                        validators=[FileRequired(),
                                    FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                'Image only please')])
