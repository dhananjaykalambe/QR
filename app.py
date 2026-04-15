from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from utils.qr import generate_qr

app = Flask(__name__)

# In-memory storage (for demo)
attendance_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'POST':
        session_id = str(uuid.uuid4())[:8]

        # Generate QR
        qr_path = generate_qr(session_id, request.host_url)

        # Store session
        attendance_data[session_id] = []

        return render_template('create_session.html', session_id=session_id, qr_path=qr_path)

    return render_template('create_session.html')

@app.route('/mark')
def mark_attendance():
    session_id = request.args.get('session_id')
    name = request.args.get('name', 'Anonymous')

    if session_id in attendance_data:
        attendance_data[session_id].append(name)
        return f"Attendance marked for {name}"

    return "Invalid Session"

@app.route('/view/<session_id>')
def view_attendance(session_id):
    data = attendance_data.get(session_id, [])
    return f"Attendance List: {data}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
