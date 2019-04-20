from app.app import db

#TODO: make book inherited from magazine?
class Magazine(db.Model):
    __tablename__ = 'magazine'
    id = db.Column(db.Integer, primary_key=True)
    # maybe is will be needed to use unicod_convert here
    title = db.Column(db.String(120))
    publishing_year = db.Column(db.Integer)
    quantity_in_stock = db.Column(db.Integer)
    description = db.Column(db.String(400))
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)
    publishing_house = db.relationship('PublishingHouse',
                               backref=db.backref('magazines', lazy=True))

    #TODO: make using dict
    def __init__(self, title, publishing_year, quantity_in_stock, description):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.description = description

    #TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Magazine %r>' % self.title

author_book_association_table = db.Table('author_book_association',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    publishing_year = db.Column(db.Integer)
    quantity_in_stock = db.Column(db.Integer)
    description = db.Column(db.String(400))
    #author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    authors = db.relationship('Author', secondary=author_book_association_table, lazy='subquery', backref=db.backref('books', lazy=True))
    publishing_house_id = db.Column(db.Integer, db.ForeignKey('publishing_house.id'), nullable=False)
    publishing_house = db.relationship('PublishingHouse',
                               backref=db.backref('books', lazy=True))

    #TODO: make using dict
    def __init__(self, title, publishing_year, quantity_in_stock, description):
        self.title = title
        self.publishing_year = publishing_year
        self.quantity_in_stock = quantity_in_stock
        self.description = description

    #TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Magazine %r>' % self.title

class PublishingHouse(db.Model):
    __tablename__ = 'publishing_house'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(400))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    #TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<PublishingHouse %r>' % self.name

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    middle_name = db.Column(db.String(80))

    #TODO: make using dict
    def __init__(self, name, surname, middle_name):
        self.name = name
        self.surname = surname
        self.middle_name = middle_name

    #TODO: remove, just artefact from lesson or rewrite
    def __repr__(self):
        return '<Author %r>' % self.name + ' ' + self.surname + ' ' + self.middle_nam