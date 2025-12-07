from flask import render_template
from flask_login import current_user

from app import create_app
from app.forms import CreateToDoForm, DeleteToDoForm, DoneToDoForm, LoginForm
from app.models import db, get_user_todo_list, get_user

# Flask app
app = create_app()
# Database
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def index() -> str:

    login_form = LoginForm()

    context = {
        'login_form': login_form,
    }

    # If the user is logged in
    if not current_user.is_anonymous:
        username = current_user.id
        create_todo_form = CreateToDoForm()
        done_todo_form = DoneToDoForm()
        delete_todo_form = DeleteToDoForm()

        # Get the user todo list
        user = current_user.id
        user_db = get_user(user)
        todo_list = get_user_todo_list(id_user=user_db.id)

        context = {
            "username": username,
            "create_todo_form": create_todo_form,
            "done_todo_form": done_todo_form,
            "delete_todo_form": delete_todo_form,
            "todo_list": todo_list
        }

        return render_template("index.html", **context)

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(port=5000,
            debug=True)
