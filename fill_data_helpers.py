from models import *
from app import db


class SaveDataHelper:
    def new_book(book_dict):
        publising_house = PublishingHouse.query.filter_by(name=book_dict['publishing_house_name']).first()
        if publising_house is None:
            publising_house = PublishingHouse(book_dict['publishing_house_name'])
            db.session.add(publising_house)
            db.session.commit()
            publising_house_id = PublishingHouse.query.filter_by(name=book_dict['publishing_house_name']).first().id
        else:
            publising_house_id = publising_house.id

        book = Book(book_dict['title'],
                    book_dict['publishing_year'],
                    book_dict['quantity_in_stock'],
                    book_dict['description'],
                    publising_house_id)
        autors = Author.query.filter_by(name=book_dict['author']).all()
        if autors is None:
            autors = Author(book_dict['author'])
            db.session.add(autors)
            db.session.commit()
        #book.book_authors.extend(autors)
        book.book_authors.append(autors)
        db.session.add(book)
        db.session.commit()

    def new_magazine(magazine_dict):
        publising_house = PublishingHouse.query.filter_by(name=magazine_dict['publishing_house_name']).first()
        if publising_house is None:
            publising_house = PublishingHouse(magazine_dict['publishing_house_name'])
            db.session.add(publising_house)
            db.session.commit()
            publising_house_id = PublishingHouse.query.filter_by(name=magazine_dict['publishing_house_name']).first().id
        else:
            publising_house_id = publising_house.id
        magazine = Magazine(magazine_dict['title'],
                            magazine_dict['publishing_year'],
                            magazine_dict['quantity_in_stock'],
                            magazine_dict['description'],
                            publising_house_id)
        db.session.add(magazine)
        db.session.commit()

    def new_author(author_dict):
        author = Author(author_dict['name'])
        db.session.add(author)
        db.session.commit()

    def new_publising_house(publising_house_dict):
        publising_house = PublishingHouse(publising_house_dict['name'])
        db.session.add(publising_house)
        db.session.commit()

