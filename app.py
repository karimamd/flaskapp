from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.sqlite3'
app.config['SECRET_KEY'] = "Kareem"

db = SQLAlchemy(app)

class notes(db.Model):
      id = db.Column('note_id', db.Integer, primary_key = True)
      title = db.Column(db.String(100))
      body = db.Column(db.String(5000)) 
      
def __init__(self, title, body):
   self.title = title
   self.body = body

@app.route('/')
def show_all():
   db.create_all()
   return render_template('show_all.html', notes = notes.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note = notes(title=request.form['title'], body=request.form['body'])
         db.session.add(note)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)