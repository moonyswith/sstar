from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__, template_folder='templates', static_folder='templates', static_url_path='')
CORS(app)

# Инициализация работы через системный VPN
ytmusic = YTMusic()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_tracks():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    try:
        search_results = ytmusic.search(query, filter='songs', limit=10)
        tracks = []
        for item in search_results:
            tracks.append({
                'id': item.get('videoId'),
                'title': item.get('title'),
                'artist': ', '.join([a['name'] for a in item.get('artists', [])]),
                'album': item.get('album', {}).get('name', 'Single'),
                'duration': item.get('duration'),
                'thumbnail': item.get('thumbnails', [{}])[-1].get('url')
            })
        return jsonify(tracks)
    except Exception as e:
        print("\n!!! ОШИБКА ПОИСКА !!!\n", e, "\n")
        return jsonify({'error': f"Ошибка поиска: {str(e)}"}), 500

@app.route('/api/stream', methods=['GET'])
def get_stream_url():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'Missing video id'}), 400

    # ⚡️ ПОЛНОСТЬЮ ИЗБАВЛЯЕМСЯ ОТ URL-АДРЕСОВ И СЛЭШЕЙ
    # Заставляем yt-dlp искать трек во внутренней базе напрямую по его уникальному ID
    search_query = f"ytsearch1:{video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noconfig': True,  # Сбрасываем любые кривые локальные конфиги системы
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ищем и извлекаем данные по внутреннему поисковому индексу
            info = ydl.extract_info(search_query, download=False)

            # Достаем ссылку на поток из результатов внутреннего поиска
            if 'entries' in info and len(info['entries']) > 0:
                stream_url = info['entries'][0].get('url')
            else:
                stream_url = info.get('url')

            if stream_url:
                return jsonify({'stream_url': stream_url})
            else:
                return jsonify({'error': 'Поток не найден в результатах'}), 404

    except Exception as e:
        print("\n!!! ОШИБКА ИЗВЛЕЧЕНИЯ ПОТОКА !!!\n", e, "\n")
        return jsonify({'error': f"Ошибка стриминга: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__, template_folder='templates', static_folder='templates', static_url_path='')
CORS(app)

# Инициализация работы через системный VPN
ytmusic = YTMusic()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_tracks():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    try:
        search_results = ytmusic.search(query, filter='songs', limit=10)
        tracks = []
        for item in search_results:
            tracks.append({
                'id': item.get('videoId'),
                'title': item.get('title'),
                'artist': ', '.join([a['name'] for a in item.get('artists', [])]),
                'album': item.get('album', {}).get('name', 'Single'),
                'duration': item.get('duration'),
                'thumbnail': item.get('thumbnails', [{}])[-1].get('url')
            })
        return jsonify(tracks)
    except Exception as e:
        print("\n!!! ОШИБКА ПОИСКА !!!\n", e, "\n")
        return jsonify({'error': f"Ошибка поиска: {str(e)}"}), 500

@app.route('/api/stream', methods=['GET'])
def get_stream_url():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'Missing video id'}), 400

    # ⚡️ ПОЛНОСТЬЮ ИЗБАВЛЯЕМСЯ ОТ URL-АДРЕСОВ И СЛЭШЕЙ
    # Заставляем yt-dlp искать трек во внутренней базе напрямую по его уникальному ID
    search_query = f"ytsearch1:{video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noconfig': True,  # Сбрасываем любые кривые локальные конфиги системы
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ищем и извлекаем данные по внутреннему поисковому индексу
            info = ydl.extract_info(search_query, download=False)

            # Достаем ссылку на поток из результатов внутреннего поиска
            if 'entries' in info and len(info['entries']) > 0:
                stream_url = info['entries'][0].get('url')
            else:
                stream_url = info.get('url')

            if stream_url:
                return jsonify({'stream_url': stream_url})
            else:
                return jsonify({'error': 'Поток не найден в результатах'}), 404

    except Exception as e:
        print("\n!!! ОШИБКА ИЗВЛЕЧЕНИЯ ПОТОКА !!!\n", e, "\n")
        return jsonify({'error': f"Ошибка стриминга: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
