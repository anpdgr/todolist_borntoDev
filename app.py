from flask import Flask,g,redirect,render_template,request,session,url_for
import db

app = Flask(__name__)

@app.route('/')
def queryTask():
        isFilter = 0
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `alltasks`")
        alltasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE date(dueDate) = CURDATE()")
        todaytasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE isDone = 1")
        donetasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE isDone = 0")
        incomtasks = cur.fetchall()
        return render_template('main.html',isFilter=isFilter, alltasks=alltasks,todaytasks=todaytasks,donetasks=donetasks,incomtasks=incomtasks)


@app.route("/add",methods=['POST'])
def add():
        value=['0','0','0','0','0']
        if request.method=="POST":
                value[0]=request.form['title']
                value[1]=request.form['des']
                value[2]=request.form['prior']
                value[3]=request.form['tags']
                value[4]=request.form['dDate']

                conn = db.get_db()
                with conn.cursor() as cursor:
                        cursor.execute("insert into alltasks(title, description, priority, tag, dueDate) values(%s,%s,%s,%s,%s)",(value[0],value[1],value[2],value[3],value[4]))                       
                        conn.commit() 
                return redirect(url_for('queryTask'))


@app.route("/filter",methods=["POST","GET"])
def filteredTable():
    dDateFilter = ''
    isFilter = 1
    connect = db.get_db()
    cur = connect.cursor()
    if request.method=="POST":
        dDateFilter = request.form['dDateFilter']
        sql = "SELECT * FROM `alltasks` WHERE dueDate = '"+dDateFilter+"'"
        cur.execute(sql)
        filtertasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE date(dueDate) = CURDATE()")
        todaytasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE isDone = 1")
        donetasks = cur.fetchall()
        cur.execute("SELECT * FROM `alltasks` WHERE isDone = 0")
        incomtasks = cur.fetchall()
    connect.commit()
    return render_template('main.html', isFilter=isFilter, dDateFilter=dDateFilter,alltasks=filtertasks,todaytasks=todaytasks,donetasks=donetasks,incomtasks=incomtasks)


@app.route("/changeDone",methods=['POST'])
def changeDone():
        value=['0','0','0','0','0','0','0']
        if request.method=="POST":
                value[0]=request.form['title']
                value[1]=request.form['des']
                value[2]=request.form['prior']
                value[3]=request.form['tags']
                value[4]=request.form['dDate']
                value[5]=request.form['isDoneChange']
                value[6]=request.form['id']

                conn = db.get_db()
                with conn.cursor() as cursor:
                        cursor.execute("update alltasks set title=%s, dueDate=%s, priority=%s, tag=%s, isDone=%s, description=%s where id=%s",(value[0],value[4],value[2],value[3],value[5],value[1],value[6]))
                        #cursor.execute("update alltasks set title=%s, dueDate=%s, priority=%s, tag=%s, description=%s where id=%s",(value[0],value[4],value[2],value[3],value[1],value[6]))
                        conn.commit()

                return redirect(url_for('queryTask'))


@app.route("/remove",methods=['POST'])
def dlt():
        if request.method=="POST":
                id=request.form['id']

                conn = db.get_db()
                with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM alltasks where id=%s",(id))
                        conn.commit()

                return redirect(url_for('queryTask'))


@app.teardown_appcontext
def close_db(error):
    db.close_db()

if __name__ == "__main__":
    app.run(debug=True)