from fill_data_helpers import SaveDataHelper
import json


def fill_db_with_data():
    data = {}
    with open("test_data.json",  "r", encoding="utf8") as read_file:
        data = json.load(read_file)

    for record in data:
        if record == "publishing_houses":
            for pub_house in data[record]:
                SaveDataHelper.new_publising_house(pub_house)
        if record == "authors":
            for author in data[record]:
                SaveDataHelper.new_author(author)
        if record == "magazines":
            for magazine in data[record]:
                SaveDataHelper.new_magazine(magazine)
        if record == "books":
            for book in data[record]:
                SaveDataHelper.new_book(book)
    return data

