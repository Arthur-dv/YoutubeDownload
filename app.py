from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Criar pasta de downloads se não existir
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o download
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json  # Recebe os dados do AJAX
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Nenhum link foi fornecido"}), 400

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return jsonify({"message": "Download concluído!"})

    except Exception as e:
        return jsonify({"error": f"Erro ao baixar o vídeo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
