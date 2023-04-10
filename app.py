from flask import Flask, request, flash, url_for, redirect, render_template
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = "karimamd95"

def get_db_connection():
   conn = psycopg2.connect(host="note-app.ckkvlyf56ji2.eu-north-1.rds.amazonaws.com", database="postgres", user="karimamd95", password="karimamd95")
   return conn

@app.route('/')
def show_all():
   # db.create_all()
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM note_items;')
   all_notes = cur.fetchall()
   cur.close()
   conn.close()
   return render_template('show_all.html', notes = all_notes )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note_title=request.form['title']
         note_body=request.form['body']
         print('printing')
         print(note_title, note_body)
         conn = get_db_connection()
         cur = conn.cursor()
         cur.execute("insert into note_items(title,body) values('{title}', '{body}'); commit;".format(title=note_title, body=note_body))
         cur.close()
         conn.close()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)