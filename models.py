from sqlalchemy.orm import relationship
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

    # TODO: make using dict
    def __init__(self, title, publishing_year, quantity_in_stock, description, publishing_house_id):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.description = description
        self.publishing_house_id = publishing_house_id

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "publishing_year":  self.publishing_year,
            "quantity_in_stock": self.quantity_in_stock,
            "description": self.description,
            "publishing_house": PublishingHouse.query.filter_by(id=self.publishing_house_id).first().name
        }

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Magazine %r>' % self.title


book_author_association = db.Table('book_author_association', db.Model.metadata,
                                   db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                                   db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                                   )


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    publishing_year = db.Column(db.Integer, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(400))
    authors = relationship('Author', secondary=book_author_association, back_populates="books")
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)


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

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "publishing_year":  self.publishing_year,
            "quantity_in_stock": self.quantity_in_stock,
            "description": self.description,
            "publishing_house": PublishingHouse.query.filter_by(id=self.publishing_house_id).first().name,
            "authors": [author.name for author in Author.query.filter(Author.books.any(Book.id == self.id)).all()]
        }


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    books = relationship(
        "Book",
        secondary=book_author_association,
        back_populates="authors")

    # TODO: make using dict
    def __init__(self, name):
        self.name = name

    # TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Author %r>' % self.name
