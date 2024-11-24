from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'saranya'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'school'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM studentdetails")
    studentinfo = cur.fetchall()
    cur.close()
    return render_template('students.html', students=studentinfo)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    if request.method == "POST":
        search_term = request.form['studentid']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM studentdetails WHERE id LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)
        cur.close()
    return render_template('students.html', students=search_results)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        iddata = request.form['studentid']
        name = request.form['name']
        student_class = request.form['class']
        age = request.form['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO studentdetails (id, name, class, age) VALUES (%s, %s, %s, %s)", (iddata, name, student_class, age))
        mysql.connection.commit()
        return redirect(url_for('students'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM studentdetails WHERE id = %s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('students'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    
    if request.method == 'POST':
        id_data = request.form['studentid']
        name = request.form['name']
        student_class = request.form['class']
        age = request.form['age']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE studentdetails SET name = %s, class = %s, age = %s WHERE id = %s", (name, student_class, age, id_data))
        mysql.connection.commit()
        return redirect(url_for('students'))
if __name__==__main__:
    app.run(debug=True)
