from __future__ import absolute_import
import pickle
import numpy as np
import json
from io import BytesIO
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask,render_template,url_for,request
import sys
sys.path.insert(0, 'database')
from dbconnect import get_connection

def load_model(path_to_pickle_file):
    """
    Loads models saved in pickle file
    """

    pickle_file = path_to_pickle_file
    with open(pickle_file, 'rb') as pf:
        model = pickle.load(pf)
    return model




rf_classifier = load_model('models/nlp_model.pkl')
cv = load_model('models/transform.pkl')
words = load_model('models/vocabulary.pkl')

conn = get_connection()



app = Flask(__name__)

@app.route('/')
def home():
    """
    Returns a welcome statements
    """
    return "Welcome - This is a Youtube comments classifier. Use a POST request and /predict with the sentence to clasify your sentence"

@app.route('/predict',methods=['POST'])
def predict():
    """
    Returns a prediction for POST and input parameters
    """
    try:
        review = request.data
        data = [review]
        
        countVect = CountVectorizer(vocabulary=words)
        sentence = countVect.transform(data).toarray()
        review_prediction = rf_classifier.predict(sentence)
        prediction = json.dumps({"review_class": review_prediction.tolist()})
        cur = conn.cursor()
        sql = """INSERT INTO Predictions(comments,predictions) VALUES(%s,%s);"""
        cur.execute(sql,(review.decode("utf-8"),prediction))
        conn.commit()     
        cur.close()
        
        return prediction
        
    except (KeyError, json.JSONDecodeError, AssertionError):
        return json.dumps({"error": "CHECK INPUT"}), 400
    except:
        return json.dumps({"error": "PREDICTION FAILED"}), 500


@app.route('/predictions',methods=['GET'])
def get_predictions():
    """
    Get all predictions
    """
    cur = conn.cursor()
    sql = """SELECT * FROM predictions ORDER BY id DESC LIMIT 10;"""
    cur.execute(sql)
    predictions = cur.fetchall()
    conn.commit()     
    cur.close()
    return json.dumps({"top_ten":predictions})


if __name__ == '__main__':
    app.run()