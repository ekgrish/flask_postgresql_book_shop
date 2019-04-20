from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request,redirect,render_template, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/book_shop'
#app.debug = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('post_new_magazine.html')

# fork for new and for existed with id
@app.route('/magazine', methods=['POST'])
def magazine_actions():
    magazine = Magazine(request.form['title'],
                        request.form['publishing_year'],
                        request.form['quantity_in_stock'],
                        request.form['description'])
    db.session.add(magazine)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()