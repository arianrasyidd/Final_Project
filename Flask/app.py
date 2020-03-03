import pandas as pd
import numpy as np
import json
import requests
from flask import Flask, render_template, url_for, request, abort, redirect, send_from_directory, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rekomendasi',methods=['POST','GET'])
def rekomendasi():
    if request.method == 'POST':
        body = request.form
        favorit = body['judul']

        if favorit not in list(df['track_name']):
            return redirect('/notfound')
        index = df[df['track_name']==favorit].index.values[0]
        # print(stat)
        rekomen_lagu = sorted(list(enumerate(cos_score[index])),key=lambda x:x[1],reverse=True) 
        lagu_fav = df.iloc[index][col]
        # print(poke_fav)
        lagu_lain = []
        for i in rekomen_lagu:
            lagu_x = {}
            if i[0] == index:
                continue
            else:
                artist = df.iloc[i[0]]['artist_name']
                track = df.iloc[i[0]]['track_name']
                mood = df.iloc[i[0]]['mood']
                lagu_x['artist'] = artist
                lagu_x['track'] = track
                lagu_x['mood'] = mood
            lagu_lain.append(lagu_x)
            if len(lagu_lain) == 10:
                break
        # print(lagu_lain)
    return render_template('rekomen.html',rekomen = lagu_lain, favoritku = lagu_fav)


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == "__main__":
    df = pd.read_csv('final_recom.csv')
    col = ['artist_name','track_name','popularity', 'result', 'mood']
    df = df[col]
    df['mood_popular'] = df.apply(lambda i: f"{i['result']},{(i['mood'])}",axis = 1)

    count_vec = CountVectorizer(tokenizer= lambda x: x.split(','))
    mood_extract = count_vec.fit_transform(df['mood_popular'])

    cos_score = cosine_similarity(mood_extract)

    app.run(debug=True)