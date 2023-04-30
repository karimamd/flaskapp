from flask import Flask, request, flash, url_for, redirect, render_template
import psycopg2
import unicodedata

app = Flask(__name__)
app.config['SECRET_KEY'] = "karimamd95"


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def get_db_connection():
   conn = psycopg2.connect(host="note-app.ckkvlyf56ji2.eu-north-1.rds.amazonaws.com", database="postgres", user="karimamd95", password="karimamd95")
   return conn

@app.route('/')
def show_all():
   # db.create_all()
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM note_items;')
   all_notes = cur.fetchall() # list of tuples
   # print(all_notes)
   all_notes_reversed=all_notes.copy()
   all_notes_reversed.reverse()
   # print(all_notes_reversed)
   cur.close()
   conn.close()
   return render_template('show_all.html', notes = all_notes_reversed )


@app.route('/queue')
def queue():
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM note_items order by note_id asc limit 10;')
   all_notes = cur.fetchall() # list of tuples
   
   my_array = all_notes

   my_list = []
   for item in my_array:
      my_dict = {'title': remove_control_characters(str(item[1])), 'body': remove_control_characters(str(item[2]))}
      my_list.append(my_dict)

   #print(my_list)
   
   cur.close()
   conn.close()
   return render_template('queue.html', my_array = my_list )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note_title=request.form['title']
         note_body=request.form['body']
         # print('printing')
         # print(note_title, note_body)
         conn = get_db_connection()
         cur = conn.cursor()
         cur.execute("insert into note_items(title,body) values('{title}', '{body}'); commit;".format(title=note_title, body=note_body))
         cur.close()
         conn.close()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)