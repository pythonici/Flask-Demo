from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
# 防止中文乱码
app.config['JSON_AS_ASCII'] = False
s_db_basedir = os.path.dirname(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(s_db_basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BookInformation(db.Model):
    __tablename__ = 'book_information'
    title = db.Column(db.String(50), primary_key=True)
    author = db.Column(db.String(20))
    learn = db.Column(db.Boolean)


# 跨域的处理
CORS(app)


# 插入数据前先查询，主键是标题不可重复添加
def judge_data_is_exist(s_title):
    s_single_record = db.session.query(BookInformation).filter_by(title=s_title).first()
    if s_single_record:
        return True
    return False


# 数据库数据全查询
def query_books_info(s_message, s_status=str()):
    d_result_info = {'status': s_status}
    response_object = list()
    l_all_books_info = db.session.query(BookInformation).all()
    # 列表对象转换成字典类型
    for d_books_info in l_all_books_info:
        if hasattr(d_books_info, '_sa_instance_state'):
            d_books_info.__dict__.pop('_sa_instance_state')
        response_object.append(d_books_info.__dict__)
    d_result_info['message'] = s_message
    d_result_info['books'] = response_object

    return d_result_info


@app.route('/all_books', methods=['GET', 'POST'])
def all_books():
    # 第一次进入页面的查询接口
    if request.method == 'GET':
        s_message = str()
        d_result_info = query_books_info(s_message)
        return jsonify(d_result_info)
    # 提交表单
    if request.method == 'POST':
        s_message = str()
        s_status = str()
        d_json_data = request.get_json()
        # 数据存在不提交
        if judge_data_is_exist(d_json_data.get('title')):
            s_message = "Book already exist!"
            s_status = "success"
            d_result_info = query_books_info(s_message, s_status)
            return jsonify(d_result_info)

        s_single_data = BookInformation(title=d_json_data.get('title'), author=d_json_data.get('author'),
                                        learn=d_json_data.get('learn'))
        db.session.add(s_single_data)

        db.session.commit()
        s_message = "Book added!"
        s_status = "success"

        d_result_info = query_books_info(s_message, s_status)
        return jsonify(d_result_info)


@app.route('/update_info/<title>',methods=['PUT','DELETE'])
def update_info(title):
    if request.method == "PUT":
        d_json_data = request.get_json()
        s_primary_key = d_json_data.pop('title')
        db.session.query(BookInformation).filter(BookInformation.title == s_primary_key).update(d_json_data)
        db.session.commit()
        s_message = "Books updated!"
        s_status = "success"
        d_result_info = query_books_info(s_message, s_status)
        return jsonify(d_result_info)
    if request.method == 'DELETE':
        db.session.query(BookInformation).filter_by(title=title).delete()
        db.session.commit()
        s_message = "Book remove!"
        s_status = "success"
        d_result_info = query_books_info(s_message, s_status)
        return jsonify(d_result_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


