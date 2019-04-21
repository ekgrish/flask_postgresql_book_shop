from models import *
from flask import request, redirect, render_template, url_for
from app import app
from app import db


@app.route('/')
def index():
    render_template('routs.html')

    return redirect(url_for('new_magazine'))


@app.route('/new_magazine')
def new_magazine():
    return render_template('new_magazine.html')


# fork for new and for existed with id
@app.route('/magazine', methods=['POST'])
def magazine_actions():
    publising_house_name = request.form['publishing_house']
    publising_house = PublishingHouse.query.filter_by(name=publising_house_name).first()
    if publising_house is None:
        publising_house = PublishingHouse(publising_house_name)
        db.session.add(publising_house)
        db.session.commit()
        publising_house_id = PublishingHouse.query.filter_by(name=publising_house_name).first().id
    else:
        publising_house_id = publising_house.id
    magazine = Magazine(request.form['title'],
                        request.form['publishing_year'],
                        request.form['quantity_in_stock'],
                        request.form['description'],
                        publising_house_id)
    db.session.add(magazine)
    db.session.commit()
    return redirect(url_for('index'))
