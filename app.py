from flask import Flask
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    desc = db.Column(db.String(200), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
  

    def __repr__(self):
        return f'{self.sno}-{self.title}'

with app.app_context():
    db.create_all() 

@app.route('/', methods = ['GET', 'POST'])
def hello_world():

    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

   

    all_todo = Todo.query.all()
    print(all_todo)
    return render_template('index.html', all_todo = all_todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno= sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>')
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    # print(todo)
    db.session.delete(todo)
    db.session.commit()
    return render_template('update.html',todo = todo)


if __name__=='__main__':
    app.run(debug= True)