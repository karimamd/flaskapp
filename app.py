from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def note_viewer():
    return 'note_view.html'

@app.route('/add')
def add_note():
    return render_template('add_note.html')


if __name__ == '__main__':
   app.run(debug=True)