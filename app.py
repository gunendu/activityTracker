from flask import Flask,request,jsonify
from dbModels import db,User,Product,Variant,UserActivity
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysqlP@ssword@localhost/weavedin'
db.init_app(app)

@app.route("/User/save",methods=['POST'])
def createUser():
    data = request.data()
    data = json.loads(data)
    db.session.add(data['name'])
    db.session.commit()
    return {}

@app.route("/Product/add",methods=['POST'])
def createProduct():
    data = request.data
    data = json.loads(data)
    product = Product(data['productname'],data['productcode'],data['branchid'])
    db.session.add(product)
    db.session.commit()
    return jsonify ({})

@app.route("/Item/Variants/add",methods=['POST'])
def createVariant():
    data = request.data
    data = json.loads(data)
    variant = Variant(data['name'],data['itemId'])
    db.session.add(variant)
    db.session.commit()
    return jsonify ({})

@app.route("/Item/Variants/edit",methods=['POST'])
def editVariant():
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
    response = db.session.query(UserActivity,User,Variant).join(User).join(Variant).filter(User.Id == userId).all()
    for row in response:
         temp1 = {}
         for res in row:
             temp = row2dict(res)
             for key in temp:
                 if key in ["Username","ItemId","name"]:
                     temp1[key] = temp[key]
         result.append(temp1)

    return jsonify({"out":result})

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

if __name__ == "__main__":
    app.run()
