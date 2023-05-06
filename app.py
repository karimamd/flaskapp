from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
import psycopg2
import unicodedata

app = Flask(__name__)
app.config['SECRET_KEY'] = "karimamd95"


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def get_db_connection():
   conn = psycopg2.connect(host="note-app.ckkvlyf56ji2.eu-north-1.rds.amazonaws.com", database="postgres", user="karimamd95", password="karimamd95")
   return conn

@app.route('/all')
def show_all():
   # db.create_all()
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM note_items order by note_id;')
   all_notes = cur.fetchall() # list of tuples
   all_notes_reversed=all_notes.copy()
   all_notes_reversed.reverse()
   cur.close()
   conn.close()
   return render_template('show_all.html', notes = all_notes_reversed )


@app.route('/')
def queue():
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM note_items order by note_id asc limit 1;')
   all_notes = cur.fetchall() # list of tuples
   # all_notes=[(1,'t1','b1'), (2,'t2','b2')]
   
   note_one = all_notes[0]
   
   cur.close()
   conn.close()
   return render_template('queue.html', note = jsonify({"note_id": note_one[0],"title": note_one[1],"body": note_one[2]} ))

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note_title=request.form['title']
         note_body=request.form['body'].replace("'", "`")
         conn = get_db_connection()
         cur = conn.cursor()
         cur.execute("insert into note_items(title,body) values('{title}', '{body}'); commit;".format(title=note_title, body=note_body))
         cur.close()
         conn.close()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


@app.route("/get_next_note")
def get_next_note():
    # Get the next note from the database
   current_note_id = request.args.get('id')
   # print(current_note_id)
   conn = get_db_connection()
   cur = conn.cursor()
   update_query="update note_items set last_read_at = current_timestamp where note_id = "+str(current_note_id)
   try:
      cur2 = conn.cursor()
      cur2.execute(update_query)
      conn.commit()
      print('executed')
   except:
      print ("I cant execute the update query for some reason")
   get_note_query= "SELECT note_id, title, body FROM note_items where note_id::INTEGER > {id} order by note_id limit 1;".format(id=current_note_id)
   cur.execute(get_note_query)
   all_notes = cur.fetchall()
   if not all_notes:
      get_note_query= "SELECT note_id, title, body FROM note_items order by note_id asc limit 1;"
      cur.execute(get_note_query)
      all_notes = cur.fetchall()  
   next_note = all_notes[0]

   # Return the next note as JSON
   return jsonify({
      "note_id": next_note[0],
      "title": next_note[1],
      "body": next_note[2]
   })

@app.route("/get_previous_note")
def get_previous_note():
    # Get the previous note from the database
   current_note_id = request.args.get('id')
   conn = get_db_connection()
   cur = conn.cursor()
   update_query="update note_items set last_read_at = current_timestamp where note_id = "+str(current_note_id)
   try:
      cur2 = conn.cursor()
      cur2.execute(update_query)
      conn.commit()
      print('executed')
   except:
      print ("I cant execute the update query for some reason")
   get_note_query= "SELECT note_id, title, body FROM note_items where note_id::INTEGER < {id} order by note_id desc limit 1;".format(id=current_note_id)
   cur.execute(get_note_query)
   all_notes = cur.fetchall()
   # if no note before it then get the last note in the database (end of queue)
   if not all_notes:
      get_note_query= "SELECT note_id, title, body FROM note_items order by note_id desc limit 1;"
      cur.execute(get_note_query)
      all_notes = cur.fetchall()
   next_note = all_notes[0]

   # Return the next note as JSON
   return jsonify({
      "note_id": next_note[0],
      "title": next_note[1],
      "body": next_note[2]
   })
   
@app.route("/get_current_note")
def get_current_note():
    # Get the next note from the database
   conn = get_db_connection()
   cur = conn.cursor()
   query= "SELECT note_id, title, body FROM note_items where last_read_at  = (select max(last_read_at) from note_items ni);"
   cur.execute(query)
   all_notes = cur.fetchall()
   # print(all_notes)
   next_note = all_notes[0]

   # Return the next note as JSON
   return jsonify({
      "note_id": next_note[0],
      "title": next_note[1],
      "body": next_note[2]
   })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)