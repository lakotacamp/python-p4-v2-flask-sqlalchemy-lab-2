from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# - a relationship named reviews that establishes a relationship with the Review model.
#   Assign the back_populates parameter to match the property name defined to the reciprocal
#   relationship in Review.
# - Update Customer to add an association proxy named items to get a list of items through 
#   the customer's reviews relationship.
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    serialize_rules = ("-reviews.customer",)
    reviews = db.relationship('Review', back_populates= 'customer')
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj))
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# - a relationship named reviews that establishes a relationship with the Review model. 
#   Assign the back_populates parameter to match the property name defined to the reciprocal
#    relationship in Review.
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    serialize_rules = ("-reviews.item",)
    reviews = db.relationship('Review', back_populates= 'item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# - add a new model class named Review that inherits from db.Model
# - attribute: a string named __tablename__ assigned to the value 'reviews'
# - attribute: a column named id to store an integer that is the primary key
# - attribute: a column named comment to store a string.
# - attribute: a column named customer_id that is a foreign key to the 'customers' table.
# - attribute: a column named item_id that is a foreign key to the 'items' table.
# - a relationship named customer that establishes a relationship with the Customer model. 
#   Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
# - a relationship named item that establishes a relationship with the Item model. Assign the back_populates parameter
#    to match the property name defined to the reciprocal relationship in Item.
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    serialize_rules = ("-customer.reviews", "-item.reviews",)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')