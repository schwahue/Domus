from ctypes import addressof
from webapp import db, ma 

# Listing Class/Model

# Can be created either by agent or seller
class Listing(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))


  price = db.Column(db.Float)
  price_type = db.Column(db.String)

  # For sale / For rent / Room rental etc
  listing_type = db.Column(db.String)

  # HDB / Condo / Bungalow etc..
  property_type = db.Column(db.String)

  # Photos 
  s3_object_link = db.Column(db.String(100))
  # Virtual Tour
  virtual_tour_url = db.Column(db.String(100))


  # new
  district = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  bedroom = db.Column(db.Integer, nullable=False)
  listed_by = db.Column(db.String(50), nullable=False)

  def __init__(self, name, description, price, price_type, listing_type, property_type, s3_object_link, virtual_tour_url, district, address, bedroom, listed_by):
    self.name = name
    self.description = description
    self.price = price
    self.price_type = price_type
    self.listing_type = listing_type
    self.property_type = property_type
    self.s3_object_link = s3_object_link
    self.virtual_tour_url = virtual_tour_url
    self.district = district
    self.address = address
    self.bedroom = bedroom
    self.listed_by = listed_by

# Listing Schema
class ListingSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'price_type', 'listing_type', 'property_type', 's3_object_link', 'virtual_tour_url', 'district', 'address', 'bedroom', 'listed_by')
