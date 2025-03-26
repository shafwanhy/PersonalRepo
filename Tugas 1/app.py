from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

GHIBLI_API_URL = "https://ghibliapi.vercel.app"

# Fitur 1: Menampilkan semua film
@app.route('/films')
def get_all_films():
    response = requests.get(f"{GHIBLI_API_URL}/films")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Gagal mengambil data"}), 500

# Fitur 2: Menampilkan detail film berdasarkan ID
@app.route('/film/<film_id>')
def get_film_by_id(film_id):
    response = requests.get(f"{GHIBLI_API_URL}/films/{film_id}")
    if response.status_code == 200:
        film = response.json()
        return render_template("film_detail.html", film=film)
    return jsonify({"error": "Film tidak ditemukan"}), 404

# Fitur 3: Menampilkan karakter dari film tertentu (pakai filter ID film)
@app.route('/characters/<film_id>')
def get_characters_by_film(film_id):
    response = requests.get(f"{GHIBLI_API_URL}/people")
    if response.status_code == 200:
        characters = response.json()
        film_url = f"{GHIBLI_API_URL}/films/{film_id}"
        
        # Filter karakter berdasarkan URL film
        film_characters = [char for char in characters if film_url in char.get("films", [])]

        if not film_characters:
            return render_template("characters.html", characters=[])

        return render_template("characters.html", characters=film_characters)

    return render_template("characters.html", characters=[])

# Route untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
