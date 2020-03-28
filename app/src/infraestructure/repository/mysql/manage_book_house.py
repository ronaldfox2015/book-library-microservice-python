# src/models/manage_book_house.py
from . import db
import datetime
from marshmallow import fields, Schema


class CustomersModel(db.Model):
  """
  Todo Model
  """

  __tablename__ = 'customers'

  id = db.Column(db.Integer, primary_key=True)
  document_number = db.Column(db.String(12), nullable=False)
  document_type = db.Column(db.String(8), nullable=False)
  tradename = db.Column(db.String(200), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  district = db.Column(db.String(200), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

class CustomersSchema(Schema):
  """
  Todo Schema
  """
  id = fields.Int(dump_only=True)
  document_number = fields.Str(required=True)
  document_type = fields.Str(required=True)
  tradename = fields.Str(required=True)
  address = fields.Str(required=True)
  district = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)


