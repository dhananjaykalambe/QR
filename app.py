from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import psycopg2
from utils.qr import generate_qr

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'POST':
        session_id = str(uuid.uuid4())[:8]

        qr_path = generate_qr(session_id, request.host_url)

        cur.execute("INSERT INTO sessions (id) VALUES (%s)", (session_id,))
        conn.commit()

        return render_template('create_session.html', session_id=session_id, qr_path=qr_path)

    return render_template('create_session.html')

@app.route('/mark')
def mark_attendance():
    session_id = request.args.get('session_id')
    name = request.args.get('name', 'Anonymous')

    # Check session exists
    cur.execute("SELECT * FROM sessions WHERE id=%s", (session_id,))
    session = cur.fetchone()

    if session:
        cur.execute(
            "INSERT INTO attendance (session_id, name) VALUES (%s, %s)",
            (session_id, name)
        )
        conn.commit()

        return f"Attendance marked for {name}"

    return "Invalid Session"

@app.route('/view/<session_id>')
def view_attendance(session_id):
    cur.execute("SELECT name FROM attendance WHERE session_id=%s", (session_id,))
    data = cur.fetchall()

    names = [row[0] for row in data]

    return f"Attendance List: {names}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
