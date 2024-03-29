import json
import base64
import csv
import hashlib
import hmac

from flask import Flask, render_template, url_for, request, redirect, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from migrations import total_migrations, unrun_migrations
from wtforms import Form, SelectField, SubmitField, validators, RadioField,StringField
from wtforms.widgets import PasswordInput
from config import bSECRET, LOCKOUT, LOCKOUT_LIMIT, ADMIN_EMAIL
from openpyxl import Workbook

from app_database import AppDataBase




def encrypt(data):
    # turn off for now till get front end working
    return data
    # message = base64.b64encode(bytes(data, 'utf-8'));
    # hash = hmac.new(bSECRET, message, hashlib.sha256);
    # hash =  base64.b64encode(hash.digest());
    # hash = hash.decode("utf-8");
    # print(hash)
    # return hash



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
    # TODO make a real jwt
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

adb = AppDataBase("/var/www/garden-tracker/garden-tracker.db")

def app_migrate(adb=adb):
    adb.migrate()


@login_manager.user_loader
def load_user(user_id):
    user = adb.cur.execute(f"SELECT rowid, username, name, is_active, is_authenticated, is_anonymous FROM users WHERE rowid=?",(user_id,)).fetchone()
    return User(user[0],user[1],user[2],user[3],user[4],user[5])


@app.route('/api/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"status": 200, "message": "Successful logout"})

@app.route('/api/who-am-i/', methods=['GET'])
def whoami():
    try:
        if current_user:
            if current_user.is_anonymous == True:
                return jsonify({"status": 500, "message": "Not Authorized"})
            else:
                return jsonify({"status": 200, "message": "logged in"})
        else:
            return jsonify({"status": 500, "message": "Not Logged in"})
    except:
        return jsonify({"status": 500, "message": "Not Logged in"})

#TODO Add ability to create user, on creation generate random token string for user (this needs to refresh every so often)
@app.route('/api/create-user/', methods=['POST'])
def create_user():
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    username_taken = adb.cur.execute("SELECT EXISTS(SELECT * FROM users WHERE username=?)",(decoded_json["username"],)).fetchone()
    if username_taken[0] != 0:
        return jsonify({"status": 500, "message": "Username already exsists"})
    else:
        # try:
        if True:
            adb.cur.execute("INSERT INTO users (username, password) VALUES (?,?)",(decoded_json["username"],encrypt(decoded_json["password"])))
            adb.con.commit()
        # except:
        #     return jsonify({"status": 500, "message": "Error adding user"})
        return jsonify({"status": 200, "message": "User Created"})
        


@app.route('/api/login/', methods=['GET', 'POST'])
def login_page():
    # TODO add jwt
    username = request.args.get("username", None)
    password = request.args.get("password", None)
    print(username, password)
    
    if username is None or password is None:
        return jsonify({"status": 500})

    if request.method == "POST":
        if LOCKOUT == True:
            user_failed_attempts = adb.cur.execute("SELECT failed_attempts FROM users WHERE username=?",(username,)).fetchone()[0]
            print(user_failed_attempts)
            if user_failed_attempts is not None and user_failed_attempts < LOCKOUT_LIMIT:
                query = adb.cur.execute("SELECT rowid, username, name, is_active, is_authenticated, is_anonymous FROM users WHERE username=? AND password=?",(username,password)).fetchone()
                print(query)
                if query is not None:
                    print("making instance")
                    instance = User(query[0],query[1],query[2],query[3],query[4],query[5])
                    if instance is not None:
                        print(instance)
                        login_user(instance)
                        return jsonify({"status": 200, "auth": f""})
                adb.cur.execute("UPDATE users SET failed_attempts=? WHERE username=?", ((user_failed_attempts + 1),username))
                adb.con.commit()
                return jsonify({"status": 500, "message": "Something has gone wrong"})
            return jsonify({"status": 500, "message": f"Your account is locked please email {ADMIN_EMAIL} for assistance."})
        else:
            query = adb.cur.execute("SELECT rowid, username, name, is_active, is_authenticated, is_anonymous FROM users WHERE username=? AND password=?",(username,password)).fetchone()
            print(query)
            if query is not None:
                instance = User(query[0],query[1],query[2],query[3],query[4],query[5])
                if instance is not None:
                    print(instance)
                    login_user(instance)
                    return jsonify({"status": 200, "auth": f""})
            return jsonify({"status": 500,"message": "Something has gone wrong" })
            

   
##########################################################################
#################     NEW CALLS     ######################################
##########################################################################

@login_required
@app.route("/api/harvest/", methods=["POST"])
def api_harvest():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    # try:
    if True:
        for item in decoded_json["harvested"]:
            if item['userplant_id'] != 0:
                item['plant_id'] = 0
                # item['plant_id'] = adb.cur.execute("SELECT plant_id FROM user_plants WHERE rowid=?",(item['userplant_id'],)).fetchone()[0]
            
            adb.cur.execute("INSERT into harvests (user_id, plant_id, userplant_id, garden_id, harvested_at, quantity, pound, ounce, notes, metadata) VALUES (?,?,?,?,?,?,?,?,?,?)",(decoded_json['user_id'],item['plant_id'],item['userplant_id'],item['garden_id'],decoded_json['date'],item['pound'],(item['quantity'] if item['quantity'] is not None else 'null'),item['ounce'],item['notes'],str(item['metadata'])))
        adb.con.commit()

    # except:
        # return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Harvest Successfully!"})


@app.route("/api/plant/new", methods=["POST"])
def api_new_plant():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    if True:
        adb.cur.execute(f"INSERT into plants (name, description, info_url, foot_size) VALUES (?,?,?,?)",(decoded_json['name'],decoded_json['description'],decoded_json['info_url'],decoded_json['foot_size']))

        adb.con.commit()
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})

@app.route("/api/amend/new", methods=["POST"])
def api_new_amend():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    if True:
        adb.cur.execute(f"INSERT into amends (name, description, info_url) VALUES (?,?,?)",(decoded_json['name'],decoded_json['description'],decoded_json['info_url']))

        adb.con.commit()
    return jsonify({"status": 200, "message": "Saved Amend Successfully!"})

@app.route("/api/amendment/new", methods=["POST"])
def api_new_amendment():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    if True:
        adb.cur.execute(f"INSERT into amendments (user_id, amend_id, garden_id, amended_at, quantity, pound, ounce, notes) VALUES (?,?,?)",(decoded_json['user_id'],decoded_json['amend_id'],decoded_json['garden_id'],decoded_json['amended_at'],decoded_json['quantity'],decoded_json['pound'],decoded_json['ounce'],decoded_json['notes']))

        adb.con.commit()
    return jsonify({"status": 200, "message": "Saved Amendment Successfully!"})


@app.route("/api/variety/new", methods=["POST"])
def api_new_variety():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"INSERT into varietys (plant_id, name, description, info_url) VALUES (?,?,?,?)",(decoded_json['plant_id'],decoded_json['name'],decoded_json['description'],decoded_json['info_url']))
        adb.con.commit()

    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@login_required
@app.route("/api/garden/new", methods=["POST"])
def api_new_garden():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute("INSERT into user_gardens (user_id, created_at, updated_at, name, description, layout, metadata) VALUES (?,?,?,?,?,?,?)" ,(decoded_json['user_id'],decoded_json['date'],decoded_json['date'],decoded_json['name'],decoded_json['description'],decoded_json['layout'], decoded_json['metadata']))
        adb.con.commit()

    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Garden Successfully!"})


@login_required
@app.route("/api/userplant/new", methods=["POST"])
def api_new_user_plant():
    # TODO add jwt auth
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    if True:
        adb.cur.execute("INSERT into user_plants (user_id, plant_id, variety_id, garden_id, created_at, updated_at, name, description, foot_size ,metadata) VALUES (?,?,?,?,?,?,?,?,?,?)",(decoded_json['user_id'],decoded_json['plant_id'],decoded_json['variety_id'],decoded_json['garden_id'],decoded_json['date'],decoded_json['date'],decoded_json['name'],decoded_json['description'],str(decoded_json['metadata']),str(decoded_json['foot_size'])))
        adb.con.commit()
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


##########################################################################
#################    UPDATE CALLS   ######################################
##########################################################################


@app.route("/api/plant/update", methods=["POST"])
def api_update_plant():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"UPDATE plants SET name = ?, description = ?, info_url = ? WHERE rowid = ?", (decoded_json['name'],decoded_json['description'], decoded_json['info_url'], decoded_json['plant_id']))
        adb.con.commit()

    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@app.route("/api/variety/update", methods=["POST"])
def api_update_variety():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute("UPDATE varietys SET name = ?, description = ?, info_url = ? WHERE rowid = ?", (decoded_json['name'], decoded_json['description'], decoded_json['info_url'], decoded_json['variety_id']))
        adb.con.commit()

    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


@login_required
@app.route("/api/garden/update", methods=["POST"])
def api_update_garden():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute("UPDATE user_gardens SET updated_at = ? ,name=? ,description = ?, layout = ? WHERE rowid = ?", (decoded_json['date'],decoded_json['name'], decoded_json['description'], decoded_json['layout'], decoded_json['garden_id']))
        adb.con.commit()
    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Garden Successfully!"})

@login_required
@app.route("/api/userplant/update", methods=["POST"])
def api_update_user_plant():
    return_json = {}
    decoded_json = json.loads(request.get_data().decode("UTF-8"))
    try:
        adb.cur.execute(f"UPDATE user_plants SET plant_id = ?, variety_id = ?, garden_id = ?, name = ?, updated_at = ?, description = ? WHERE rowid = ?", (decoded_json['plant_id'],decoded_json['variety_id'], decoded_json['garden_id'], decoded_json['name'], decoded_json['date'], decoded_json['description'], decoded_json['userplant_id']))
        adb.con.commit()

    except:
        return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    return jsonify({"status": 200, "message": "Saved Plant Successfully!"})


##########################################################################
#################    SERIALIZERS   #######################################
##########################################################################

@login_required
@app.route("/api/user/", methods=["GET"])
def api_user_serializer():
    #TODO add jwt auth
    # fornow using current_user, will use that with frontend jwt
    if current_user.is_anonymous == True:
        return jsonify({"status": 500, "message": "Not Authorized"})

    serialized = {}
    user_id = current_user.id

    if user_id is None:
        return jsonify({"status": 500, "message": "No user supplied"})
    else:
        user_fields = adb.cur.execute("select name,username from users where rowid=?",(user_id,)).fetchone()
        garden_fields = adb.cur.execute("select rowid ,name, description, layout, metadata from user_gardens where user_id=?",(user_id,)).fetchall()
        userplant_fields = adb.cur.execute("select rowid, plant_id, variety_id, garden_id, name, description, foot_size, metadata from user_plants where user_id=?",(user_id,)).fetchall()

        garden_titles = ["value" ,"label", "description", "layout", "metadata"]
        userplant_titles = ["value", "plant_id", "variety_id", "garden_id", "label", "description", "metadata", "foot_size"]
        
        serialized["user_id"] = user_id
        serialized["name"] = user_fields[0]
        serialized["username"] = user_fields[1]
        serialized["gardens"] = [{garden_titles[i] : item[i] for i in range(len(garden_titles))} for item in garden_fields]
        serialized["user_plants"] = [{userplant_titles[i] : item[i] for i in range(len(userplant_titles))} for item in userplant_fields]
    return jsonify(serialized)




@login_required
@app.route("/api/userharvests/", methods=["GET"])
def api_harvest_serializer():
    #TODO add jwt
    
    if current_user.is_anonymous == True:
        return jsonify({"status": 500, "message": "Not Authorized"})

    user_id = current_user.id
    if user_id is None:
        return jsonify({"status": 500, "message": "No user supplied"})
    serialized = {}
    harvests_titles = ["harvested_at", "plant_name", "userplant_name", "garden_name", "quantity", "pound", "ounce", "notes"]
    #TODO add metadata field

    q_string = """
    SELECT
    h.harvested_at,
    p.name,
    up.name,
    ug.name,
    h.quantity,
    h.pound,
    h.ounce,
    h.notes
    from harvests as h
    LEFT JOIN user_plants as up ON h.userplant_id = up.rowid
    LEFT JOIN plants as p ON h.plant_id = p.rowid
    LEFT JOIN user_gardens as ug ON h.garden_id = ug.rowid
    WHERE h.user_id = ? ORDER BY h.rowid DESC"""
    query_harvests = adb.cur.execute(q_string, (user_id,)).fetchall()
   
    serialized["harvests"] = [{harvests_titles[i] : harvests[i] for i in range(len(harvests_titles))} for harvests in query_harvests]
    return jsonify(serialized)

@app.route("/api/plants/<pid>", methods=["GET"])
def api_plant_serializer_by_id(pid):
    serialized = {}
    plant_titles = ["value", "label", "description", "info_url"]
    query_plant = adb.cur.execute("SELECT rowid, name, description, info_url from plants where rowid=?", pid).fetchone()
    print(query_plant)
    serialized["plant"] = {plant_titles[i] : query_plant[i] for i in range(len(plant_titles))}
    return jsonify(serialized)

@app.route("/api/plants/", methods=["GET"])
def api_plant_serializer():
    serialized = {}
    plant_titles = ["value", "label", "description", "info_url"]
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
        variety_titles = ["value", "label", "description", "info_url"]
        query_varietys = adb.cur.execute("SELECT rowid, name, description, info_url from varietys WHERE plant_id=?",(plant_id,)).fetchall()

        serialized["varietys"] = [{variety_titles[i] : variety[i] for i in range(len(variety_titles))} for variety in query_varietys]
        return jsonify(serialized)



    
@login_required    
@app.route("/api/delete/<data_type>/<id>", methods=["GET"])
def api_delete_type(data_type, id):
    if data_type is None or id is None:
        return jsonify({"status": 500, "message": "Missing argument"})
    data_type_list = [
        "harvests",
        "user_plants",
        "user_gardens"
    ]
    if data_type not in data_type_list:
        return jsonify({"status": 500, "message": "invalid argument"})
        
    belongs_to_user = adb.cur.execute(f"SELECT * FROM {data_type} WHERE user_id=?",(current_user.id,)).fetchone()
    if belongs_to_user is not None:
        adb.cur.execute(f"DELETE FROM {data_type} WHERE rowid=?",(id,)).fetchone()
        adb.con.commit()
        return jsonify({"status": 200, "message": "Delete succcessful!"})
    return jsonify({"status": 500, "message": "Uh oh! Something went wrong"})
    
@login_required    
@app.route("/api/export_data/<export_type>", methods=["GET"])
def api_export_user_harvests(export_type):
    if current_user.is_anonymous == True:
        return jsonify({"status": 500, "message": "Not Authorized"})

    user_id = current_user.id
    if user_id is None:
        return jsonify({"status": 500, "message": "No user supplied"})

    harvest_data_dump = adb.cur.execute("""SELECT
    h.rowid,
    h.harvested_at,
    up.name,
    p.name,
    ug.name,
    h.quantity,
    h.pound,
    h.ounce,
    h.notes,
    h.metadata
    from harvests as h
    LEFT JOIN user_plants as up ON h.userplant_id = up.rowid
    LEFT JOIN plants as p ON h.plant_id = p.rowid
    LEFT JOIN user_gardens as ug ON h.garden_id = ug.rowid
    WHERE h.user_id = ? ORDER BY h.rowid DESC""",(user_id,)).fetchall()
    harvest_titles = ["Harvest Id", "Havest Date", "Userplant Name",
                      "Plant Name", "Garden Name", "Quantity", "Pound",
                      "Ounce", "Notes", "Metadata"]
    if export_type == "csv":
        
        with open("/tmp/export.csv", "w") as cf:
            csvfile = csv.writer(cf)
            csvfile.writerow(harvest_titles)
            [csvfile.writerow(line) for line in harvest_data_dump]
        return send_file("/tmp/export.csv", mimetype='text/csv',download_name="exported_harvests.csv", as_attachment=True)
    elif export_type == "xlsx":
        wb = Workbook()
        ws = wb.active
        # TODO add titleso
        for row in range(len(harvest_data_dump)):
            for col in range(len(harvest_data_dump[row])):
                _ = ws.cell(column=col+1, row=row+1, value=harvest_data_dump[row][col])
        wb.save("/tmp/export.xlsx")
        return send_file("/tmp/export.xlsx",
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         download_name="exported_harvests.xlsx", as_attachment=True)
    elif export_type == "ui":
        pass # get data for front end 
    # serialized["varietys"] = [{variety_titles[i] : variety[i] for i in range(len(variety_titles))} for variety in query_varietys]


    # if __name__ == "__main__":
#     app.run()
