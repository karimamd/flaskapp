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

def query_db(query, is_fetchable=False, needs_commit=False):
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute(query)
   all_records = []
   if is_fetchable:
      all_records = cur.fetchall()
   if needs_commit:
      conn.commit()
   cur.close()
   conn.close()
   return all_records
   
@app.route('/')
def queue():
   select_last_read = 'SELECT * FROM note_items_unarchived order by last_read_at desc limit 1;'
   last_read_notes = query_db(select_last_read, True) # list of tuples
   # all_notes=[(1,'t1','b1'), (2,'t2','b2')] 
   note_one = last_read_notes[0]
   return render_template('queue.html')

@app.route('/all')
def show_all():
   select_all = 'SELECT * FROM note_items_unarchived order by note_id;'
   all_notes = query_db(select_all, True) # list of tuples
   all_notes_reversed=all_notes.copy()
   all_notes_reversed.reverse()
   return render_template('show_all.html', notes = all_notes_reversed )


@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note_title=request.form['title']
         note_body=request.form['body'].replace("'", "`")

         insert_query = "insert into note_items(title,body) values('{title}', '{body}'); commit;".format(title=note_title, body=note_body)
         query_db(insert_query, is_fetchable=False, needs_commit=False)
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route("/get_note_by_id")
def get_note_by_id():
   current_note_id = request.args.get('id')
   print('current note id:')
   print(current_note_id)
   get_note_query= "SELECT note_id, title, body FROM note_items_unarchived where note_id::INTEGER = {id} limit 1;".format(id=current_note_id)
   all_notes = query_db(get_note_query, True)
   if not all_notes:
      get_note_query= "SELECT 0 as note_id, 'none found' as title, 'none found' as body FROM note_items_unarchived order by note_id asc limit 1;"
      all_notes = query_db(get_note_query, True)
   backend_note = all_notes[0]
   # Return the note as JSON
   return jsonify({
      "note_id": backend_note[0],
      "title": backend_note[1],
      "body": backend_note[2]
   })
   
@app.route('/edit', methods = ['GET', 'POST'])
def edit():
   # next: want to send parameter to edit page of which id to show
   # current_note_id = request.args.get('id')
   if request.method == 'POST':
      if not request.form['title'] or not request.form['body']:
         flash('Please enter all the fields', 'error')
      else:
         note_title=request.form['title']
         note_body=request.form['body'].replace("'", "`")

         insert_query = "insert into note_items(title,body) values('{title}', '{body}'); commit;".format(title=note_title, body=note_body)
         query_db(insert_query, is_fetchable=False, needs_commit=False)
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('edit.html')

      


@app.route("/get_next_note")
def get_next_note():
    # Get the next note from the database
   current_note_id = request.args.get('id')
   # print(current_note_id)
   update_query="update note_items set last_read_at = current_timestamp where note_id = "+str(current_note_id)
   try:
      query_db(update_query, is_fetchable=False, needs_commit=True)
      print('executed')
   except:
      print ("I cant execute the update query for some reason")
      
   get_note_query= "SELECT note_id, title, body FROM note_items_unarchived where note_id::INTEGER > {id} order by note_id limit 1;".format(id=current_note_id)
   
   all_notes = query_db(get_note_query, is_fetchable=True)
   if not all_notes:
      get_note_query= "SELECT note_id, title, body FROM note_items_unarchived order by note_id asc limit 1;"
      all_notes = all_notes = query_db(get_note_query, is_fetchable=True)
   next_note = all_notes[0]

   # Return the next note as JSON
   return jsonify({
      "note_id": next_note[0],
      "title": next_note[1],
      "body": next_note[2]
   })
   
   
@app.route("/delete")
def archive_note():
    # Get the next note from the database
   current_note_id = request.args.get('id')
   # print(current_note_id)
   archive_query="update note_items set is_archived = true where note_id = "+str(current_note_id)
   try:
      query_db(archive_query, is_fetchable=False, needs_commit=True)
      print('executed')
   except:
      print ("I cant execute the update query for some reason")
   get_note_query= "SELECT note_id, title, body FROM note_items_unarchived where note_id::INTEGER > {id} order by note_id limit 1;".format(id=current_note_id)
   all_notes = query_db(get_note_query, True)
   if not all_notes:
      get_note_query= "SELECT note_id, title, body FROM note_items_unarchived order by note_id asc limit 1;"
      all_notes = query_db(get_note_query, True)
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
   update_query="update note_items set last_read_at = current_timestamp where note_id = "+str(current_note_id)
   try:
      query_db(update_query, False, needs_commit=True)
      print('executed')
   except:
      print ("I cant execute the update query for some reason")
   get_note_query= "SELECT note_id, title, body FROM note_items_unarchived where note_id::INTEGER < {id} order by note_id desc limit 1;".format(id=current_note_id)
   all_notes = query_db(get_note_query, is_fetchable=True)
   # if no note before it then get the last note in the database (end of queue)
   if not all_notes:
      get_note_query= "SELECT note_id, title, body FROM note_items_unarchived order by note_id desc limit 1;"
      all_notes = query_db(get_note_query, is_fetchable=True)
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
   query= "SELECT note_id, title, body FROM note_items_unarchived where last_read_at  = (select max(last_read_at) from note_items_unarchived ni);"
   all_notes = query_db(query, is_fetchable=True, needs_commit=False)
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