from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)
process = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        frequency = request.form['frequency']
        file = request.files['file']
        if file and file.filename.endswith('.wav'):
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)
            global process
            if process:
                process.terminate()
            command = ['sudo', './fm_transmitter', '-f', frequency, filepath]
            process = subprocess.Popen(command)
            return redirect(url_for('index'))
    return render_template('index.html', frequency='105.1')

@app.route('/stop', methods=['POST'])
def stop():
    global process
    if process:
        process.terminate()
        process = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=9000)
