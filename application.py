"""Main Application Drinks Database"""
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import DrinkFamily, DrinkSubType, Drink, Base


#Connect to Database and create database session
engine = create_engine('sqlite:///drinks.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Show all drinks
@app.route('/')
@app.route('/drinks/')
def showDrinks():
  drinks = session.query(DrinkFamily).add_columns(DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
  print(drinks)
#   return "SHOW Drink Family Route!"
  return render_template('drink_family_home.html', drinks = drinks)

#Create a new drink family
@app.route('/drinks/new/', methods=['GET','POST'])
def newDrink():
    return "NEW Drink Family Route!"

#Edit a drink family
@app.route('/drinks/<int:drink_familyURL_id>/edit/', methods = ['GET', 'POST'])
def editDrink(drink_familyURL_id):
    return "EDIT Drink Family Route!"

#Delete a drink family
@app.route('/drinks/<int:drink_familyURL_id>/delete/', methods = ['GET','POST'])
def deleteDrink(drink_familyURL_id):
    return "DELETE Drink Family Route!"

#Show drink subtypes
@app.route('/drinks/<int:drink_familyURL_id>/')
def showDrinkSubType(drink_familyURL_id):
    drinks = session.query(DrinkFamily).add_columns(DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    subdrinks = session.query(DrinkSubType).filter_by(drink_family_id = drink_familyURL_id ).add_columns(DrinkSubType.name, DrinkSubType.id, DrinkSubType.drink_family_id).order_by(asc(DrinkSubType.name))    
    for subdrink in subdrinks:
        print(subdrink)
    return render_template('drink_subtype_home.html', drinks = drinks, subdrinks = subdrinks)
    # return "SHOW Drink Family SubType Route!"
     
#Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/new/',methods=['GET','POST'])
def newDrinkSubType(drink_familyURL_id):
    return "NEW Drink Family Subtype Route!"

#Edit a drinkSubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/edit', methods=['GET','POST'])
def editDrinkSubType(drink_familyURL_id, type_id):
    return "EDIT Drink Family Subtype Route!"

#Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/delete', methods = ['GET','POST'])
def deleteDrinkSubType(drink_familyURL_id, type_id):
    return "DELETE Drink Family SubType Route!"

#Show drink subtype brands
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/')
def showDrinkList(drink_familyURL_id, type_id):
    return "SHOW Drink Family SubType Drink List Route!"

#Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/new/',methods=['GET','POST'])
def newDrinkList(drink_familyURL_id, type_id):
    return "NEW Drink Family Subtype Drink List Route!"

#Edit a drinkSubType Brand
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/edit', methods=['GET','POST'])
def editDrinkList(drink_familyURL_id, type_id, drink_id):
    return "EDIT Drink Family Subtype Drink List Route!"

#Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/delete', methods = ['GET','POST'])
def deleteDrinkList(drink_familyURL_id, type_id, drink_id):
    return "DELETE Drink Family SubType Drink List Route!"

#Show drink subtype brand detail
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/')
def showDrinkListDetail(drink_familyURL_id, type_id, drink_id):
    return "SHOW Drink Family SubType Drink List Item Detail Route!"


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
