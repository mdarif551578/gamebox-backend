from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.String(127))
    zone_id = db.Column(db.String(127))
    transaction_code = db.Column(db.String(127))
    selected_package_text = db.Column(db.String(255))

with app.app_context():
    db.create_all()



# public endpoint
###########################################
@app.route("/add/", methods=["POST"])
def add():
    data = request.get_json()

    print(data)

    user_id = data.get('user_id')
    zone_id = data.get('zone_id')
    transaction_code = data.get('transaction_code')
    selected_package_text = data.get('selected_package_text')

    new_todo = Todo(complete=False,user_id=user_id,zone_id=zone_id,transaction_code=transaction_code,selected_package_text=selected_package_text)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"status": "ok", "msg": "Order Submitted Successfully."})
    # try:
    #     data = request.get_json()

    #     print(data)

    #     user_id = data.get('user_id')
    #     zone_id = data.get('zone_id')
    #     transaction_code = data.get('transaction_code')
    #     selected_package_text = data.get('selected_package_text')

    #     new_todo = Todo(complete=False,user_id=user_id,zone_id=zone_id,transaction_code=transaction_code,selected_package_text=selected_package_text)
    #     db.session.add(new_todo)
    #     db.session.commit()

    #     return jsonify({"status": "ok", "msg": "Order Submitted Successfully."})
    # except:
    #     return jsonify({"status": "failed", "msg": "Order Submittion Failed."})
###########################################


msky = "hi"


# private endpoints
@app.get(f"/{msky}/")
def home():
    todo_list = db.session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)

@app.get(f"/{msky}/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get(f"/{msky}/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)



