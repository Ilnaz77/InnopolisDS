import pandas as pd
import numpy as np
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

df = pd.read_csv('data2.csv', ',')
data = df[df.columns].astype('str')


@app.route('/<string:root>/<string:tag>', methods=['GET'])
def get_all(root, tag):
    if root == 'movie_id':
        try:
            result = list(data['movie'][data['movie_id']==tag])[0]
        except:
            abort(404)
        dic = {'tconst':tag, 'title':result}
        return jsonify(movie=dic)

    result = list(data[data[root] == tag]['movie_id'])
    if len(result) == 0:
        abort(404)
    return jsonify(movies=result)

@app.route('/suggest/<int:topk>', methods=['POST'])
def post_suggest(topk):
    if topk > data.shape[0]:
        abort(404)
        
    req = request.get_json()
    
    for m_id in req['likes']:
        data['ratings'][data['movie_id'] == m_id] = req['likes'][m_id]

    result = np.random.choice(list(data['movie_id'][data['ratings'] == 'None']), topk)
    return jsonify({'ratings':{m_id:abs(round(np.random.rand(),1)) for m_id in result}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

