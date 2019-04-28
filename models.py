from flask_login._compat import unicode
from sqlalchemy.orm import relationship
from app import db, serializer
from flask_login import UserMixin


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(10), nullable=False)

    def __init__(self, product_type):
        self.product_type = product_type

    def to_json(self):
        return {"id": self.id,
                "type": self.type}

    # TODO: think, is that correct?
    def save_data(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return {"error": "{}".format(e)}
        else:
            product_type = Type.query.filter_by(product_type=self.product_type).first()
            return product_type.to_json(self)

    def get_id_by_name(self, name):
        return self.query.filter_by(name=name)

    def __repr__(self):
        return '<Type %r>' % self.product_type


class PublishingHouse(db.Model):
    __tablename__ = 'publishing_house'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {"id": self.id,
                "name": self.name}

    # TODO: think, is that correct?
    def save_data(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return {"error": "{}".format(e)}
        else:
            publishing_house = PublishingHouse.query.filter_by(name=self.name).first()
            return publishing_house.to_json(self)

    def get_id_by_name(self, name):
        return self.query.filter_by(name=name)

    def __repr__(self):
        return '<PublishingHouse %r>' % self.name


book_author_association = db.Table('book_author_association', db.Model.metadata,
                                   db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                                   db.Column('book_id', db.Integer, db.ForeignKey('product.id'))
                                   )


# TODO: make book and magazine inherited from maybe
# one Table, but with two "handlers"
# just think about it someday, yeah?)
# now using only one model to simplify
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    publishing_year = db.Column(db.Integer)
    quantity_in_stock = db.Column(db.Integer)
    # TODO make table for types
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)
    authors = relationship('Author', secondary=book_author_association, back_populates="books")

    def __init__(self, title, publishing_year, quantity_in_stock, publishing_house_id, type_id):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.publishing_house_id = publishing_house_id
        self.type_id = type_id

    def to_json(self):
        product_type = Type.query.filter_by(id=self.type_id).first()
        if product_type is None:
            return {"error": "something goes wrong with type"}
        publishing_house = PublishingHouse.query.filter_by(id=self.publishing_house_id).first()
        if publishing_house is None:
            return {"error": "something goes wrong with publishing house"}
        result = {"id": self.id,
                  "type": product_type.product_type,
                  "title": self.title,
                  "publishing_year": self.publishing_year,
                  "quantity_in_stock": self.quantity_in_stock,
                  "publishing_house": publishing_house.name,
                  }
        if product_type.product_type == "книга":
            authors = [author.name for author in Author.query.filter(Author.books.any(Product.id == self.id)).all()]
            if authors is None:
                return {"error": "something goes wrong with publishing house"}
            else:
                result["authors"] = authors
        return result

    def __repr__(self):
        return '<Product %r>' % self.title


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    books = relationship(
        "Product",
        secondary=book_author_association,
        back_populates="authors")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    session_token = db.Column(db.String(100), unique=True)

    def __init__(self, username):
        self.username = username
        self.session_token = serializer.dumps([username])

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return unicode(self.session_token)
