from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def note_viewer():
    return render_template('homepage.html', page= 'homepage')

@app.route('/add')
def add_note():
    return render_template('add_note.html', page= 'note add page')


if __name__ == '__main__':
   app.run(debug=True)