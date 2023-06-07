from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "sql12.freemysqlhosting.net"
app.config["MYSQL_USER"] = "sql12624048"
app.config["MYSQL_PASSWORD"] = "BDElAiWtYu"
app.config["MYSQL_DB"] = "sql12624048"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}  # https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes

mysql = MySQL(app)

# Server: sql12.freemysqlhosting.net
# Name: sql12624048
# Username: sql12624048
# Password: BDElAiWtYu
# Port number: 3306


@app.route("/add")
def form():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    task = request.form['task']
    task_desc = request.form['task_desc']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `example` (`id`, `title`, `des`) VALUES (NULL, %s, %s)",(task, task_desc))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("show"))

@app.route("/")
@app.route("/display")
def show():
    cur = mysql.connection.cursor()
    data = cur.execute("SELECT * FROM example")
    if data > 0:
        users = cur.fetchall()
        return render_template("home.html",users=users)

@app.route("/update/<todo_id>")
def update(todo_id):
    cur = mysql.connection.cursor()
    sql = f"SELECT * FROM example WHERE `id` = {todo_id}"
    data = cur.execute(sql)
    if data > 0:
        users = cur.fetchall()
        return render_template("update.html", users = users)

@app.route("/update", methods=['POST'])
def updateData():
    task = request.form['task']
    task_desc = request.form['task_desc']
    todo_id = request.form['id']
    cur = mysql.connection.cursor()

    # sql = cur.execute("update example set `title`=%s, `des`=%s where `id`=%s")
    sql = "UPDATE `example` SET `title` = %s, `des` = %s WHERE `example`.`id` = %s"
    val = (task, task_desc, todo_id)
    cur.execute(sql, val)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("show"))


@app.route("/delete/<id>")
def delete(id):
    cur = mysql.connection.cursor()
    sql = f"DELETE FROM `example` WHERE `example`.`id` = {id}"
    cur.execute(sql)
    mysql.connection.commit()
    return redirect(url_for("show"))

if __name__ == "__main__":
    app.run(debug=True)