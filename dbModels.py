from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    Id = db.Column(db.Integer,primary_key=True)
    Username = db.Column(db.String(300))

    def __init__(self,name):
        self.Username = name;


class Product(db.Model):
    __tablename__ = "Product"
    ItemId = db.Column(db.Integer,primary_key=True)
    ProductName = db.Column(db.String(100))
    ProductCode = db.Column(db.String(100))
    BranchId = db.Column(db.String(100))

    def __init__(self,ProductName,ProductCode,BranchId):
        self.ProductName = ProductName
        self.ProductCode = ProductCode
        self.BranchId = BranchId


class Variant(db.Model):
    __tablename__ = "Variant"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    ItemId = db.Column(db.Integer,db.ForeignKey('Product.ItemId'))

    def __init__(self,name):
        self.name = name


class UserActivity(db.Model):
    __tablename__ = "UserActivity"
    id = db.Column(db.Integer, primary_key=True)
    ItemId = db.Column(db.Integer)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'))
    ActivityId = db.Column(db.Integer, db.ForeignKey('Variant.id'))
    UpdateAt = db.Column(db.Date)

    def __init__(self,ItemId,UserId,ActivityId,UpdateAt):
        self.ItemId = ItemId
        self.UserId = UserId
        self.ActivityId = ActivityId
        self.UpdateAt = UpdateAt
