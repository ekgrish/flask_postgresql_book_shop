from models import PublishingHouse, Product, Author, Type, User
from app import db


class SaveDataHelper:
    def new_product(product_dict):
        publishing_house = PublishingHouse.query.filter_by(name=product_dict['publishing_house_name']).first()
        if publishing_house is None:
            publishing_house = PublishingHouse(product_dict['publishing_house_name'])
            publishing_house.save_data()
            publishing_house_id = PublishingHouse.query.filter_by(name=product_dict['publishing_house_name']).first().id
        else:
            publishing_house_id = publishing_house.id

        product_type = Type.query.filter_by(product_type=product_dict['type']).first()
        if product_type is None:
            product_type = Type(product_dict['type'])
            product_type.save_data()
            product_type_id = Type.query.filter_by(product_type=product_dict['type']).first().id
        else:
            product_type_id = product_type.id

        product = Product(product_dict['title'],
                          product_dict['publishing_year'],
                          product_dict['quantity_in_stock'],
                          publishing_house_id,
                          product_type_id)
        if product_type.product_type == "книга":
            for author_name in product_dict['authors']:
                author = Author.query.filter_by(name=author_name).first()
                if author is None:
                    author = Author(author_name)
                    db.session.add(author)
                    db.session.commit()
                    product.authors.append(author)
                else:
                    product.authors.append(author)
        db.session.add(product)
        db.session.commit()

    def new_author(author_dict):
        author = Author(author_dict['name'])
        db.session.add(author)
        db.session.commit()

    def new_publising_house(publising_house_dict):
        publising_house = PublishingHouse(publising_house_dict['name'])
        db.session.add(publising_house)
        db.session.commit()

    def new_type(type_dict):
        product_type = Type(type_dict['name'])
        db.session.add(product_type)
        db.session.commit()

    def new_user(user_dict):
        user = User(user_dict['username'])
        db.session.add(user)
        db.session.commit()
