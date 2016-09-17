from flask import Flask,request,jsonify
from dbModels import db,User,Product,Variant,UserActivity,Property
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysqlP@ssword@localhost/weavedin'
db.init_app(app)

@app.route("/user/save",methods=['POST'])
def createUser():
    data = request.data()
    data = json.loads(data)
    user = User(data['name'])
    db.session.add(user)
    db.session.commit()
    return {}

@app.route("/product/add",methods=['POST'])
def createProduct():
    data = request.data
    data = json.loads(data)
    product = Product(data['property'],data['branchid'])
    db.session.add(product)
    db.session.commit()
    return jsonify ({"ItemId":product.ItemId})

@app.route("/variants/add",methods=['POST'])
def createVariant():
    data = request.data
    data = json.loads(data)
    variant = Variant(data['name'],data['itemId'])
    db.session.add(variant)
    db.session.commit()
    return jsonify ({"VariantId":variant.id})

@app.route("/property/add",methods=['POST'])
def createProperty():
    data = request.data
    data = json.loads(data)
    prop = Property(data['variantId'],data['property'])
    db.session.add(prop)
    db.session.commit()
    return jsonify ({"PropertyId":prop.id})

@app.route("/activity/log",methods=['POST'])
def editProduct():
    data = request.data
    data = json.loads(data)
    userId = data['userId']

    itemId = data['itemId']
    varianceId = data.get('varianceId',"")
    propertyId = data.get('propertyId',"")

    sellingPrice = data.get('sellingPrice',"")
    costPrice = data.get('costPrice',"")
    quantity = data.get('quantity',"")

    itemName = data.get('itemName',"")
    itemCode = data.get('itemCode',"")

    updateAt = datetime.datetime.now()

    if itemId and not varianceId and not propertyId:
        for key in data:
            if key in ["itemName","itemCode"]:
                userActivity = UserActivity(userId,itemId,None,None,data[key],updateAt)
                db.session.add(userActivity)
                db.session.commit()

    if itemId and varianceId and not propertyId:
        userActivity = UserActivity(userId,itemId,varianceId,None,data[key],updateAt)
        db.session.add(userActivity)
        db.session.commit()

    if itemId and varianceId and propertyId:
        for key in data:
            if key in ["sellingPrice","costPrice","Quantity"]:
                userActivity = UserActivity(userId,itemId,varianceId,propertyId,data[key],updateAt)
                db.session.add(userActivity)
                db.session.commit()

    return jsonify({})

@app.route("/variants/edit",methods=['POST'])
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

@app.route("/user/activity/<userId>",methods=['GET'])
def getUserActivity(userId):
    result = []
    response = db.session.query(UserActivity).filter(User.Id == userId).all()
    for row in response:
         temp = row2dict(row)
         result.append(temp)

    print formulateResponse(result,userId)
    return jsonify({"out":result})

def formulateResponse(result,userId):
    propids = []
    itemids = []
    res = ""
    user = User.query.filter(User.Id==userId).first()
    if user is not None:
        res = res + user.Username + " edited "
    for d in result:
        if d['PropertyId'] is not None:
            propids.append(d['PropertyId'])
        itemids.append(d['ItemId'])

    propids = set(propids)
    response = Property.query.filter(Property.id.in_(propids)).all()
    for key in response:
        temp = row2dict(key)
        res = res + temp['Properties'] + ","

    res = res + " of "
    itemids = set(itemids)
    response = Product.query.filter(Product.ItemId.in_(itemids)).all()
    for key in response:
        temp = row2dict(key)
        res = res + temp['Properties']
        
    return res
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

if __name__ == "__main__":
    app.run()
