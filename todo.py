from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db  = SQLAlchemy(app)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route('/add', methods=["POST"])
def addTodo():
    title   = request.form.get("title")
    newTodo = Todo(title = title, complate = 0)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update/<string:id>', methods=["GET"])
def updateTodo(id):
    changeTodo = Todo.query.filter_by(id=id).first()
    changeTodo.complate = not changeTodo.complate
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods=["GET"])
def deleteTodo(id):
    deleteTodo = Todo.query.filter_by(id=id).first()
    db.session.delete(deleteTodo)
    db.session.commit()

    return redirect(url_for('index'))

class Todo(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(100))
    complate = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
