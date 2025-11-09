from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)
DB_NAME = "songs.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            youtube_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route 1: Add a song (HTML form + POST handler)
@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form.get('title')
        youtube_url = request.form.get('youtube_url')

        if not title or not youtube_url:
            return "Please provide both a song title and YouTube URL.", 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO songs (title, youtube_url) VALUES (?, ?)", (title, youtube_url))
        conn.commit()
        conn.close()

        return redirect('/add_song')

    # HTML form for GET request
    html_form = """
    <html>
    <head>
        <title>Add a Song</title>
    </head>
    <body>
        <h1>Add a New Song</h1>
        <form method="POST" action="/add_song">
            <label for="title">Song Title:</label><br>
            <input type="text" id="title" name="title" required><br><br>

            <label for="youtube_url">YouTube URL:</label><br>
            <input type="url" id="youtube_url" name="youtube_url" required><br><br>

            <input type="submit" value="Add Song">
        </form>
        <br>
    </body>
    </html>
    """
    return html_form


# Route 2: Display all songs in a table
@app.route('/songs', methods=['GET'])
def show_songs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, youtube_url FROM songs")
    songs = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head><title>Song List</title></head>
    <body>
        <h1>All Songs</h1>
        <table border="1" cellpadding="8">
            <tr><th>ID</th><th>Title</th><th>YouTube URL</th></tr>
            {% for id, title, url in songs %}
                <tr>
                    <td>{{ id }}</td>
                    <td>{{ title }}</td>
                    <td><a href="{{ url }}" target="_blank">{{ url }}</a></td>
                </tr>
            {% endfor %}
        </table>
        <br>
        <a href="/add_song">Add Another Song</a>
    </body>
    </html>
    """
    return render_template_string(html, songs=songs)


if __name__ == '__main__':
    app.run(debug=True)
