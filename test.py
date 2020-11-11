from flask import Flask, request, render_template,redirect,url_for
from threading import Timer
import psycopg2
import  webbrowser
connection1=None
try:
      connection1=psycopg2.connect(
      port=12312,
      host="localhost",
      database="TEST",
      user="postgres",
      password="qwe123@")
except:
      print("not connected")
      print("---------------------------------------------")


cursor1=connection1.cursor()
cursor1.execute("""CREATE TABLE  IF NOT EXISTS TODOLIST
                (ID           SERIAL    NOT NULL,
                 TASK           TEXT  NOT NULL,
                 NOTES        TEXT  NOT NULL,
                 COMPLETE     BOOLEAN);""")
connection1.commit()

app = Flask(__name__)
@app.route('/')
def home():
      cursor1.execute('''SELECT *  FROM TODOLIST;''')
      cur=cursor1.fetchall()
      return render_template("lost.html",value=cur)
      

@app.route('/add', methods =["GET", "POST"]) 
def add(): 
    if (request.method == "POST"):  
       Task=request.form.get("task")
       Notes=request.form.get("notes")
       Complete=False;
       cursor1.execute('''INSERT INTO TODOLIST(TASK,NOTES,COMPLETE)  VALUES (%s,%s,%s)''',
                      (Task,Notes,Complete));
       connection1.commit()
       return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
      string=str(todo_id)
      cursor1.execute('''SELECT * FROM TODOLIST WHERE ID=%s;''',(todo_id,))
      cur =cursor1.fetchone()
      cur1=list(cur)
      a=True
      b=False
      if (cur1[3]==True):
            cursor1.execute('''UPDATE TODOLIST SET COMPLETE=%s WHERE ID=%s;''',(b,todo_id,))
      else:
            cursor1.execute('''UPDATE TODOLIST SET COMPLETE=%s WHERE ID=%s;''',(a,todo_id,))      
      connection1.commit()
      return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
      cursor1.execute('''DELETE FROM TODOLIST  WHERE ID=%s''',(todo_id,))
      connection1.commit()
      return redirect(url_for("home"))

def open_browser():
      webbrowser.open_new('http://127.0.0.1:2000/')


if __name__ == "__main__":
      Timer(1,open_browser).start();
      app.run(port=2000,debug=True)

       
