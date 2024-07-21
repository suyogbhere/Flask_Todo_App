from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # date_created=db.Column(Datetime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.title} - {self.desc}"

# @app.route('/')
# def hello_world():
#     return "Hello world"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        print('POST')
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    # todo = Todo(title="First Todo", desc="Start Investing in stock market")
    # db.session.add(todo)
    # db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", AllTodo=alltodo)

@app.route('/show/')
def product():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'This is product page'


@app.route('/delete/<int:SrNo>/')
def todo_delete(SrNo):
        deltodo = Todo.query.filter_by(SrNo=SrNo).first()
        print(deltodo)
        db.session.delete(deltodo)
        db.session.commit()
        return redirect("/")

@app.route('/update/<int:SrNo>/', methods=['GET', 'POST'])
def todo_update(SrNo):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        updatetodo = Todo.query.filter_by(SrNo=SrNo).first()
        updatetodo.title = title
        updatetodo.desc = desc
        db.session.add(updatetodo)
        db.session.commit()
        return redirect("/")
    updatetodo = Todo.query.filter_by(SrNo=SrNo).first()
    return render_template('update.html',todo=updatetodo)
    
if __name__ == "__main__":
    app.run(debug=False)

