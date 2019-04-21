from app import db


class PublishingHouse(db.Model):
    __tablename__ = 'publishing_house'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<PublishingHouse %r>' % self.name


# TODO: make book inherited from magazine?
class Magazine(db.Model):
    __tablename__ = 'magazine'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    publishing_year = db.Column(db.Integer)
    quantity_in_stock = db.Column(db.Integer)
    description = db.Column(db.String(400))
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)
    publishing_house = db.relationship('PublishingHouse', backref=db.backref('magazines', lazy=True))

    # TODO: make using dict
    def __init__(self, title, publishing_year, quantity_in_stock, description, publishing_house_id):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.description = description
        self.publishing_house_id = publishing_house_id

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Magazine %r>' % self.title


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    publishing_year = db.Column(db.Integer, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(400))
    book_authors = db.relationship('BookAuthor', cascade="all, delete-orphan", backref="book")
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)
    publishing_house = db.relationship('PublishingHouse', backref=db.backref('books', lazy=True))

    # TODO: make using dict
    def __init__(self, title, publishing_year, quantity_in_stock, description, publishing_house_id):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.description = description
        self.publishing_house_id = publishing_house_id

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Magazine %r>' % self.title


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    # TODO: make using dict
    def __init__(self, name):
        self.name = name

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Author %r>' % self.name


class BookAuthor(db.Model):
    __tablename__ = "book_author"
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), primary_key=True)

    def __init__(self, item, price=None):
        self.item = item
        self.price = price or item.price

    author = db.relationship(Author, lazy="joined")
