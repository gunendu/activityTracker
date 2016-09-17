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
    Properties = db.Column(db.String(100))
    BranchId = db.Column(db.String(100))

    def __init__(self,Properties,BranchId):
        self.Properties = Properties
        self.BranchId = BranchId


class Variant(db.Model):
    __tablename__ = "Variant"
    id = db.Column(db.Integer,primary_key=True)
    Variants = db.Column(db.String(100))
    ItemId = db.Column(db.Integer,db.ForeignKey('Product.ItemId'))

    def __init__(self,name,ItemId):
        self.Variants = name
        self.ItemId = ItemId


class Property(db.Model):
    __tablename__ = "Property"
    id = db.Column(db.Integer,primary_key=True)
    VariantId = db.Column(db.Integer,db.ForeignKey('Variant.id'))
    Properties = db.Column(db.String())

    def __init__(self,VariantId,Properties):
        self.VariantId = VariantId
        self.Properties = Properties


class UserActivity(db.Model):
    __tablename__ = "UserActivity"
    id = db.Column(db.Integer, primary_key=True)
    ItemId = db.Column(db.Integer, db.ForeignKey('Product.ItemId'))
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'))
    VariantId = db.Column(db.Integer, db.ForeignKey('Variant.id'))
    PropertyId = db.Column(db.Integer, db.ForeignKey('Property.id'))
    UpdateAt = db.Column(db.Date)
    value = db.Column(db.String(100))

    def __init__(self,UserId,ItemId,VariantId,PropertyId,value,UpdateAt):
        self.ItemId = ItemId
        self.UserId = UserId
        self.VariantId = VariantId
        self.PropertyId = PropertyId
        self.value = value
        self.UpdateAt = UpdateAt
