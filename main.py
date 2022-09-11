import json
import base64

from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from migrations import total_migrations, unrun_migrations
from wtforms import Form, SelectField, SubmitField, validators, RadioField,StringField
from wtforms.widgets import PasswordInput


from app_database import AppDataBase

class LoginForm(Form):
    username = StringField("Username:")
    password = StringField("Password:", widget=PasswordInput(hide_value=False))
    submit = SubmitField("Log In")


class User():

    def __init__(self,rowid, username, name, is_active=0, is_authenticated=0, is_anonymous=0):
        self.id = rowid
        self.name=name
        self.is_active=is_active
        self.username=username
        self.is_anonymous=is_anonymous 
        self.is_authenticated=is_authenticated
        
    def get_id(self):
        return str(self.id)
        


def create_jwt(user_id, username, password="", token=""):
    # to_b64_encode = [user_id, username, password, token]
    to_b64_encode = [user_id, username]
    res = []
    [res.append(base64.b64encode(bytes(str(item),"UTF-8"))) for item in to_b64_encode]
    new_res = [str(res[i].decode("UTF-8")) for i in range(len(res))]
    jwt_str = ".".join(new_res)
    return jwt_str


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"

login_manager = LoginManager(app)
login_manager.init_app(app)

adb = AppDataBase("garden-tracker.db")
# adb.migrate()


@app.route("/")
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    user = adb.cur.execute(f"SELECT rowid, username, name, is_active, is_authenticated, is_anonymous FROM users WHERE rowid={user_id}").fetchone()
    return User(user[0],user[1],user[2],user[3],user[4],user[5])


@app.route('/api/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")

#TODO Add ability to create user, on creation generate random token string for user (this needs to refresh every so often)
# @app.route('/create/', methods=['GET', 'POST'])
# def create_page():
#     #this is where you will make a user 
#     return render_template("create.html",create_form=create_form)


@app.route('/api/login/', methods=['GET', 'POST'])
def login_page():
    # TODO add jwt
    username = request.args.get("username", None)
    password = request.args.get("password", None)
    print(username, password)
    if username is None or password is None:
        return jsonify({"status": 500})
    if request.method == "POST":
        #TODO add pass encryption probably
        query = adb.cur.execute(f"SELECT rowid, username, name, is_active, is_authenticated, is_anonymous FROM users WHERE username='{username}' AND password='{password}'").fetchone()
        print(query)
        if query is not None:
            instance = User(query[0],query[1],query[2],query[3],query[4],query[5])
        if instance is not None:
            print(instance)
            login_user(instance)
            return jsonify({"status": 200})
            # return redirect("/home/")
        else:
            return jsonify({"status": 500})
            # return render_template("login.html",login_form=login_form)
    else:
        return jsonify({"status": 500})
        # return render_template("login.html",login_form=login_form)


   
##########################################################################
#################     NEW CALLS     ######################################
##########################################################################


@app.route("/api/harvest/", methods=["POST"])
def api_harvest():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        for item in decoded_json["harvested"]:
            # TODO fix sql injectsion
            adb.cur.execute(f"INSERT into harvests (user_id, plant_id, date, quantity, pound, ounce, notes) VALUES ({decoded_json['user_id']},{item['plant_id']},'{decoded_json['date']}',{item['pound']},{item['quantity'] if item['quantity'] is not None else 'null' },{item['ounce']},'{item['notes']}')")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Harvest Successfully!"})


@app.route("/api/plant/new", methods=["POST"])
def api_new_plant():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"INSERT into plants (name, description, info_url) VALUES ('{decoded_json['name']}','{decoded_json['description']}','{decoded_json['info_url']}')")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@app.route("/api/variety/new", methods=["POST"])
def api_new_variety():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"INSERT into varietys (plant_id, name, description, info_url) VALUES ({decoded_json['plant_id']},'{decoded_json['name']}','{decoded_json['description']}','{decoded_json['info_url']}')")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@app.route("/api/garden/new", methods=["POST"])
def api_new_garden():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        #TODO metadata wont work for now, need to fix the sql injection or quote problems 
        adb.cur.execute(f"INSERT into user_gardens (user_id, created_at, updated_at, name, description, layout) VALUES ({decoded_json['user_id']},'{decoded_json['date']}','{decoded_json['date']}','{decoded_json['name']}','{decoded_json['description']}','{decoded_json['layout']}')")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Garden Successfully!"})


@app.route("/api/userplant/new", methods=["POST"])
def api_new_user_plant():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        #TODO add metadata to insert/ fix inject/ quote problems
        adb.cur.execute(f"INSERT into user_plants (user_id, plant_id, variety_id, garden_id, created_at, updated_at, name, description) VALUES ({decoded_json['user_id']},{decoded_json['plant_id']},{decoded_json['variety_id']},{decoded_json['garden_id']},'{decoded_json['date']}','{decoded_json['date']}','{decoded_json['name']}','{decoded_json['description']}')")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


##########################################################################
#################    UPDATE CALLS   ######################################
##########################################################################


@app.route("/api/plant/update", methods=["POST"])
def api_update_plant():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"UPDATE plants SET name = {decoded_json['name']}, description = {decoded_json['description']}, info_url = {decoded_json['info_url']}) WHERE rowid = {decoded_json['plant_id']}")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@app.route("/api/variety/update", methods=["POST"])
def api_update_variety():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"UPDATE varietys SET plant_id = {decoded_json['plant_id']}, name = {decoded_json['name']}, description = {decoded_json['description']}, info_url = {decoded_json['info_url']}) WHERE rowid = {decoded_json['variety_id']}")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@app.route("/api/garden/update", methods=["POST"])
#TODO add user jwt auth 
def api_update_garden():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"UPDATE user_gardens SET plant_id = {decoded_json['plant_id']}, updated_at = '{decoded_json['date']}',name = {decoded_json['name']}, description = {decoded_json['description']}, layout = '{decoded_json['layout']}') WHERE rowid = {decoded_json['garden_id']}")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Garden Successfully!"})


@app.route("/api/userplant/update", methods=["POST"])
def api_update_user_plant():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        #TODO add user JWT auth
        adb.cur.execute(f"UPDATE user_plants SET plant_id = {decoded_json['plant_id']}, variety_id = {decoded_json['plant_id']}, garden_id = {decoded_json['plant_id']}, name = '{decoded_json['name']}', updated_at = '{decoded_json['date']}', description = '{decoded_json['description']}', info_url = {decoded_json['info_url']}) WHERE rowid = {decoded_json['userplant_id']}")
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


##########################################################################
#################    SERIALIZERS   #######################################
##########################################################################


@app.route("/api/user/", methods=["GET"])
def api_user_serializer():
    #TODO add jwt auth
    serialized = {}
    user_id = request.args.get("user_id", None)
    if user_id is None:
        return jsonify({"status": 500, "message": "No user supplied"})
    else:
        user_fields = adb.cur.execute(f"select name,username from users where rowid={user_id}").fetchone()
        garden_fields = adb.cur.execute(f"select rowid ,name, description, layout, metadata from user_gardens where user_id={user_id}").fetchall()
        userplant_fields = adb.cur.execute(f"select rowid, plant_id, variety_id, garden_id, name, description, metadata from user_plants where user_id={user_id}").fetchall()

        garden_titles = ["garden_id" ,"name", "description", "layout", "metadata"]
        userplant_titles = ["userplant_id", "plant_id", "variety_id", "garden_id", "name", "description", "metadata"]
        
        serialized["user_id"] = user_id
        serialized["name"] = user_fields[0]
        serialized["username"] = user_fields[1]
        serialized["gardens"] = [{garden_titles[i] : item[i] for i in range(len(garden_titles))} for item in garden_fields]
        serialized["user_plants"] = [{userplant_titles[i] : item[i] for i in range(len(userplant_titles))} for item in userplant_fields]
    return jsonify(serialized)


@app.route("/api/plants/", methods=["GET"])
def api_plant_serializer():
    serialized = {}
    plant_titles = ["plant_id", "name", "description", "info_url"]
    query_plants = adb.cur.execute("SELECT rowid, name, description, info_url from plants").fetchall()
    serialized["plants"] = [{plant_titles[i] : plant[i] for i in range(len(plant_titles))} for plant in query_plants]
    return jsonify(serialized)


@app.route("/api/varietys/", methods=["GET"])
def api_variety_serializer():
    plant_id = request.args.get("plant_id", None)
    if plant_id is None:
        return jsonify({"status": 500, "message": "No plant id supplied"})
    else:
        serialized = {}
        serialized["plant_id"] = plant_id
        variety_titles = ["variety_id", "name", "description", "info_url"]
        query_varietys = adb.cur.execute(f"SELECT rowid, name, description, info_url from varietys WHERE plant_id={plant_id}").fetchall()
        serialized["varietys"] = [{variety_titles[i] : variety[i] for i in range(len(variety_titles))} for variety in query_varietys]
        return jsonify(serialized)

    
if __name__ == "__main__":
    app.run()
