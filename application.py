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
    if request.method == 'POST':
        if request.form['name'] != "":
            newDrinkFamily = DrinkFamily(name = request.form['name'])
            session.add(newDrinkFamily)
            flash('New Drink Family %s Successfully Created' % newDrinkFamily.name)
            session.commit()
            return redirect(url_for('showDrinks'))
        else:
            flash('New Drink Family Type Not Created.','error')
            return render_template('new_drink_family.html')
    else:
        return render_template('new_drink_family.html')
    # return "NEW Drink Family Route!"

#Edit a drink family
@app.route('/drinks/<int:drink_familyURL_id>/edit/', methods = ['GET', 'POST'])
def editDrink(drink_familyURL_id):
    return "EDIT Drink Family Route!"

#Delete a drink family
@app.route('/drinks/<int:drink_familyURL_id>/delete/', methods = ['GET','POST'])
def deleteDrink(drink_familyURL_id):
    drinkFamilyToDelete = session.query(DrinkFamily).filter_by(id = drink_familyURL_id).first()
    if request.method == 'POST':
        session.delete(drinkFamilyToDelete)
        flash('%s Successfully Deleted' % drinkFamilyToDelete.name)
        session.commit()
        return redirect(url_for('showDrinks'))
    else:
        return render_template('delete_drink_family.html',drinkFamily = drinkFamilyToDelete)
    # return "DELETE Drink Family Route!"

#Show drink subtypes
@app.route('/drinks/<int:drink_familyURL_id>/')
def showDrinkSubType(drink_familyURL_id):
    drinks = session.query(DrinkFamily).add_columns(DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    subdrinks = session.query(DrinkSubType).filter_by(drink_family_id = drink_familyURL_id ).add_columns(DrinkSubType.name, DrinkSubType.id, DrinkSubType.drink_family_id).order_by(asc(DrinkSubType.name))    
    action = drink_familyURL_id
    for subdrink in subdrinks:
        print(subdrink)
    return render_template('drink_subtype_home.html', drinks = drinks, subdrinks = subdrinks, action = action)
    # return "SHOW Drink Family SubType Route!"
     
#Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/new/',methods=['GET','POST'])
def newDrinkSubType(drink_familyURL_id):
    parent_family = session.query(DrinkFamily).filter_by(id = drink_familyURL_id).first()
    if request.method == 'POST':
        if request.form['name'] != "":
            newSubDrinkFamily = DrinkSubType(name = request.form['name'], drink_family_id = drink_familyURL_id, drink_family = parent_family)
            session.add(newSubDrinkFamily)
            flash('New Drink Sub Type %s Successfully Created' % newSubDrinkFamily.name)
            session.commit()
            return redirect(url_for('showDrinkSubType', drink_familyURL_id = drink_familyURL_id))
        else:
            flash('New Drink Sub Type Not Created.','error')
            return redirect(url_for('showDrinkSubType', drink_familyURL_id = drink_familyURL_id))                         
    else:
        return render_template('new_drink_sub_family.html')
    # return "NEW Drink Family Subtype Route!"

#Edit a drinkSubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/edit', methods=['GET','POST'])
def editDrinkSubType(drink_familyURL_id, type_id):
    return "EDIT Drink Family Subtype Route!"

#Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/delete', methods = ['GET','POST'])
def deleteDrinkSubType(drink_familyURL_id, type_id):
    drinkSubFamilyToDelete = session.query(DrinkSubType).filter_by(id = type_id).first()
    if request.method == 'POST':
        session.delete(drinkSubFamilyToDelete)
        flash('%s Successfully Deleted' % drinkSubFamilyToDelete.name)
        session.commit()
        return redirect(url_for('showDrinkSubType', drink_familyURL_id = drink_familyURL_id))
    else:
        return render_template('delete_sub_drink_family.html',subFamily = drinkSubFamilyToDelete)
    # return "DELETE Drink Family SubType Route!"

#Show drink subtype brands
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/')
def showDrinkList(drink_familyURL_id, type_id):
    drinks = session.query(DrinkFamily).add_columns(DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    drinklist = session.query(Drink).filter_by(drink_subtype_id = type_id ).add_columns(Drink.name, Drink.id, Drink.description).order_by(asc(Drink.name))
    action_family = drink_familyURL_id
    action_sub = type_id
    for drink in drinklist:
        print(drink)
    return render_template('drink_list_home.html', drinks = drinks, drinklist = drinklist, action_family = action_family, action_sub = action_sub)
    
#Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/new/',methods=['GET','POST'])
def newDrinkList(drink_familyURL_id, type_id):
    parent_family = session.query(DrinkSubType).filter_by(id = type_id).first()
    if request.method == 'POST':
        if request.form['name'] != "":
            newDrinkList = Drink(name = request.form['name'], description = request.form['description'],drink_subtype_id = type_id, drink_subtype = parent_family)
            session.add(newDrinkList)
            flash('New Drink Sub Type %s Successfully Created' % newDrinkList.name)
            session.commit()
            return redirect(url_for('showDrinkList', drink_familyURL_id = drink_familyURL_id,type_id = type_id))
        else:
            flash('New Drink Sub Type Item Not Created.','error')
            return redirect(url_for('showDrinkList', drink_familyURL_id = drink_familyURL_id,type_id = type_id ))            
    else:
        return render_template('new_drink_sub_family_list.html')
    # return "NEW Drink Family Subtype Drink List Route!"

#Edit a drinkSubType Brand
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/edit', methods=['GET','POST'])
def editDrinkList(drink_familyURL_id, type_id, drink_id):
    return "EDIT Drink Family Subtype Drink List Route!"

#Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/delete', methods = ['GET','POST'])
def deleteDrinkList(drink_familyURL_id, type_id, drink_id):
    drinkListItemToDelete = session.query(Drink).filter_by(id = drink_id).first()
    if request.method == 'POST':
        session.delete(drinkListItemToDelete)
        flash('%s Successfully Deleted' % drinkListItemToDelete.name)
        session.commit()
        return redirect(url_for('showDrinkList', drink_familyURL_id = drink_familyURL_id, type_id = type_id ))
    else:
        return render_template('delete_drink_list.html',drink = drinkListItemToDelete)
    # return "DELETE Drink Family SubType Drink List Route!"

#Show drink subtype brand detail
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/')
def showDrinkListDetail(drink_familyURL_id, type_id, drink_id):
    drinks = session.query(DrinkFamily).add_columns(DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    drink_detail = session.query(Drink).filter_by(id = drink_id ).add_columns(Drink.name, Drink.id, Drink.description).order_by(asc(Drink.name)).first()    
    for drink in drink_detail:
        print(drink)
    return render_template('drink_detail.html', drinks = drinks, drink_detail = drink_detail, type_id = type_id, drink_id = drink_id )

    return "SHOW Drink Family SubType Drink List Item Detail Route!"


if __name__ == '__main__':
  app.secret_key = 'super_seotnhoenuhoeanuhoaenuh  au3242134luoaecblecret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
