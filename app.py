from google import genai
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests
app = Flask(__name__)




data = {
    'genre': ['Hip-Hop', 'Hip-Hop', 'Pop', 'Pop', 'K-Pop', 'K-Pop', 'Alternative/Indie', 'R&B', 'R&B'],
    'niche_artist': [
        'Underground Rapper A', 'Indie Hiphop B',
        'Bedroom Pop C', 'Dream Pop D',
        'Indie Kpop E', 'Kpop Band F',
        'Indie Rock G',
        'Soul R&B H', 'Lo-fi R&B I'
    ]
}
df_niche_artists = pd.DataFrame(data)


genre_to_singers = {
    'Hip-Hop': ['Singer-HH1', 'Singer-HH2', 'Singer-HH3'],
    'Pop': ['Singer-P1', 'Singer-P2', 'Singer-P3'],
    'K-Pop': ['Singer-K1', 'Singer-K2', 'Singer-K3'],
    'Alternative/Indie': ['Singer-A1', 'Singer-A2', 'Singer-A3'],
    'R&B': ['Singer-R1', 'Singer-R2', 'Singer-R3']
}
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        mbti = request.form.get('mbti')
        genre = request.form.get('genre')
        singer = request.form.get('singer')

        return redirect(url_for('result', mbti=mbti, genre=genre, singer=singer))

    return render_template('quiz.html', genre_to_singers=genre_to_singers)


@app.route('/result')
def result():
    # 从 URL 参数获取数据
    mbti = request.args.get('mbti')
    genre = request.args.get('genre')
    singer = request.args.get('singer')
    content = f"Based on your MBTI: {mbti}, Genre: {genre}, Singer: {singer}, recommend me some songs!(just song names) and give a comment on how what type of songs i would like(2sentensces)"
    client = genai.Client(api_key="AIzaSyBP1BPnpQtA60YJ1dbVYC7RGfQv2_LmPz8")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    gemini_comment = response.text

    print( gemini_comment)


    niche_subset = df_niche_artists[df_niche_artists['genre'] == genre]
    if not niche_subset.empty:
        niche_artist = niche_subset.sample(1).iloc[0]['niche_artist']
    else:
        niche_artist = "暂无小众歌手推荐"

    return render_template('result.html',
                           mbti=mbti,
                           genre=genre,
                           singer=singer,
                           gemini_comment=gemini_comment,
                           niche_artist=niche_artist)


if __name__ == '__main__':

    app.run(debug=True)




