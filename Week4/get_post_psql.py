from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ilnazindira1997@localhost/InnoDS"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Text)
    movie = db.Column(db.Text)
    year = db.Column(db.Text)
    ratings = db.Column(db.Text)

    def __repr__(self):
        return '%r' % self.movie_id 

@app.route('/<string:root>/<string:tag>', methods=['GET'])
def get_all(root, tag):
    try:
        if root == 'movie_id':
            result = Test.query.filter_by(movie_id=tag).first()
            dic = {'tconst':tag, 'title':result.movie}
            return jsonify(movie=dic)
        elif root == 'year':
            result = Test.query.filter_by(year=tag).all()
            list_object = list([i.movie_id for i in result])
            return jsonify(movies=list_object)
        elif root == 'movie':
            result = Test.query.filter_by(movie=tag).all()
            list_object = list([i.movie_id for i in result])
            return jsonify(movies=list_object)
    except:
        abort(404)

@app.route('/suggest/<int:topk>', methods=['POST'])
def post_suggest(topk):
    req = request.get_json()

    for m_id in req['likes']:
        Test.query.filter_by(movie_id=m_id).update({'ratings':req['likes'][m_id]})
    db.session.commit()

    
    obj = Test.query.filter(Test.ratings.endswith('None')).all()
    result = np.random.choice(obj, topk)

    return jsonify({'ratings':{m_id.movie_id:abs(round(np.random.rand(),1)) for m_id in result}})
 
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # print(Test.query.filter_by(year='1894').first())