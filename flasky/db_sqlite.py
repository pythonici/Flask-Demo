import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
apps = Flask(__name__)
# 配置数据库

s_db_basedir = os.path.dirname(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(s_db_basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BookInformation(db.Model):
    __tablename__ = 'book_information'
    title = db.Column(db.String(50), primary_key=True)
    author = db.Column(db.String(20))
    learn = db.Column(db.Boolean)
# if __name__ == "__main__":
#     db.create_all()
#     s_single_data = BookInformation(title="The Left Hand of Darkness", author="Shakespeare", learn=True)
#     db.session.add(s_single)
#     db.session.commit()





