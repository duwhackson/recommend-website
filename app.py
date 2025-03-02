from google import genai
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


def load_music_data():
    try:
        encodings = ['cp1252', 'latin1', 'iso-8859-1', 'gbk', 'gb2312', 'utf-8']

        for encoding in encodings:
            try:
                
                print(f"try {encoding} files...")
                df = pd.read_csv('web.csv', encoding=encoding)

               
                valid_columns = []
                for col in df.columns:
                    if col and not col.startswith('Unnamed'):
                        valid_columns.append(col)

             
                if 'GENRE' not in df.columns or 'Popular Artist' not in df.columns:
                    print(f"using {encoding} find genre and popular artist")
                    continue

    
                for col in df.columns:
                    if df[col].dtype == 'object':  
                        df[col] = df[col].str.strip()

                print(f"successfully using {encoding} reading files")

                return df
            except UnicodeDecodeError as e:
                print(f"{encoding} not suit to: {e}")
                continue
            except Exception as e:
                print(f"mistakes happens when encoding with {encoding} : {e}")
                continue

        df = pd.read_csv('web.csv', encoding='latin1', errors='replace')
        return df
    except Exception as e:
        print(f"mistake happens: {e}")
        return pd.DataFrame()



def create_genre_to_singers_map(df):
    if df.empty:
        return {}

    genre_to_singers = {}
    for genre in df['GENRE'].unique():
        if pd.isna(genre):
            continue

        genre_artists = df[df['GENRE'] == genre]['Popular Artist'].dropna().tolist()
        genre_to_singers[genre] = list(set(genre_artists))

    print(f"build the connection: {genre_to_singers}")
    return genre_to_singers



music_data = load_music_data()
genre_to_singers = create_genre_to_singers_map(music_data)


if not genre_to_singers or 'Kpop' not in genre_to_singers:
    default_data = {
        'Hip-Hop': ['Kendrick Lamar', 'Eminem', 'Megan Thee Stallion', 'Nicki Minaj'],
        'Pop': ['Taylor Swift', 'Sabrina Carpenter', 'One Direction', 'Justin Bieber'],
        'Kpop': ['BTS', 'IU', 'EXO', 'New Jeans'],
        'Alternative/Indie': ['Phoebe Bridgers', 'Mitski', 'Melanie Martinez', 'Arctic Monkeys'],
        'R&B': ['Usher', 'Frank Ocean', 'Michael Jackson', 'Kehlani']
    }


    for genre, artists in default_data.items():
        if genre not in genre_to_singers:
            genre_to_singers[genre] = artists


if music_data.empty:
    sample_data = []
    for genre, artists in genre_to_singers.items():
        for artist in artists:
            sample_data.append({
                'GENRE': genre,
                'Popular Artist': artist,
                'Small Artist': f'Unknown {genre} Artist',
                'Instagram': '#',
                'Spotify': '#',
                'Popular Song': 'Sample Song',
                'Song Link': '#'
            })
    music_data = pd.DataFrame(sample_data)


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

    mbti = request.args.get('mbti')
    genre = request.args.get('genre')
    singer = request.args.get('singer')


    content = f"Based on your MBTI: {mbti}, Genre: {genre}, Singer: {singer}, recommend me some songs!(just song names) and give a comment on how what type of songs i would like(2sentensces)"


    client = genai.Client(api_key="AIzaSyBP1BPnpQtA60YJ1dbVYC7RGfQv2_LmPz8")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=content
        )
        gemini_comment = response.text
    except Exception as e:
        print(f"Gemini API 调用出错: {e}")
        gemini_comment = f"Based on your preference for {genre} music and artists like {singer}, you might enjoy energetic tracks with meaningful lyrics. Your MBTI type {mbti} suggests you appreciate music that resonates with your emotional depth."

    print(gemini_comment)


    genre_matches = music_data[music_data['GENRE'].str.lower() == genre.lower()]


    if genre_matches.empty:
        for g in music_data['GENRE'].unique():
            if pd.notna(g) and (genre.lower() in g.lower() or g.lower() in genre.lower()):
                genre_matches = music_data[music_data['GENRE'] == g]
                break

    if not genre_matches.empty:

        niche_artist_row = genre_matches.sample(1).iloc[0]
        niche_artist = {
            'name': niche_artist_row['Small Artist'],
            'instagram': niche_artist_row['Instagram'],
            'spotify': niche_artist_row['Spotify'],
            'popular_song': niche_artist_row['Popular Song'],
            'song_link': niche_artist_row['Song Link'],
            'genre': niche_artist_row['GENRE'],
            'album_image': niche_artist_row['Album Image'],
            'artist_image':niche_artist_row['Artist Image']
        }
    else:
        niche_artist = {
            'name': "sorry for blanket",
            'instagram': "#",
            'spotify': "#",
            'popular_song': "",
            'song_link': "#",
            'genre': genre,
            'album_image' : "#",
            'artist_image' : "#"
        }

    return render_template('result.html',
                           mbti=mbti,
                           genre=genre,
                           singer=singer,
                           gemini_comment=gemini_comment,
                           niche_artist=niche_artist)


if __name__ == '__main__':
    app.run(debug=True)
