from flask import Flask,request,jsonify
from dbModels import db,User,Product,Variant,UserActivity
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysqlP@ssword@localhost/weavedin'
db.init_app(app)

@app.route("/User/save",methods=['POST'])
def createUser():
    user = request.data()
    data = json.loads(data)
    db.session.add(data['name'])
    db.session.commit()
    return {}

@app.route("/Item/Variants/add",methods=['POST'])
def createVariant():
    data = request.data
    data = json.loads(data)
    variant = Variant(data['name'])
    db.session.add(variant)
    db.session.commit()
    return jsonify ({})

@app.route("/Item/Variants/edit",methods=['POST'])
def createProduct():
    data = request.data
    data = json.loads(data)
    userId = data['userId']
    itemId = data['itemId']
    activityId = data['activityId']

    updateAt = datetime.datetime.now()
    userActivity = UserActivity(userId,itemId,activityId,updateAt)
    db.session.add(userActivity)
    db.session.commit()
    return jsonify ({})

@app.route("/User/Activity/<userId>",methods=['GET'])
def getUserActivity(userId):
    result = []
    response = db.session.query(User,UserActivity,Variant).filter(User.Id == UserActivity.UserId).filter(Variant.id == UserActivity.ActivityId).filter(User.Id == userId).all()
    for res in response:
        for row in res:
            result.append(row2dict(row))

    return jsonify({"out":result})

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

if __name__ == "__main__":
    app.run()
