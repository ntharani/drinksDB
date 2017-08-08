"""Main Application Drinks Database"""
from __future__ import print_function
from flask import(Flask, render_template, request, redirect, jsonify,
                  url_for, flash)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import DrinkFamily, DrinkSubType, Drink, Base

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "The Drinks Category App"

# Connect to Database and create database session
engine = create_engine('sqlite:///drinks.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# oauth / login stuff
@app.route('/login')
def showLogin():
    """Login Page"""
    state = ''.join(random.choice(
        string.ascii_uppercase +
        string.digits
        ) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" %login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Google Social Login"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        # response = make_response(json.dumps('Invalid state parameter.'), 401)
        # print("Invalid state param")
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return(jsonify("Invalid state parameter."), 401)
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        """
        # NB: All the code below can be simplified by returning jsonify.
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print("Failed to upgrade auth code")
        return response
        """
        return(jsonify("Failed to upgrade the authorization code."), 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        # response = make_response(json.dumps(result.get('error')), 500)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return(jsonify(result.get('error')), 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return(jsonify("Token's user ID doesn't match given user ID."), 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return(jsonify("Token's client ID does not match app's."), 401)
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return(jsonify("Current user is already connected."), 200)

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '"'
    output += """ style = "
    width: 300px;
    height: 300px;
    border-radius: 150px;
    -webkit-border-radius: 150px;
    -moz-border-radius: 150px;">
    """
    flash("You are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Google Social Disconnect"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect(url_for('showDrinks'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Restaurant Information
@app.route('/drinks/<int:drink_familyURL_id>/JSON')
def drinkFamilyJSON(drink_familyURL_id):
    """JSON End Point"""
    items = session.query(DrinkSubType).filter_by(
        drink_family_id=drink_familyURL_id).all()
    return jsonify(ans=[i.serialize for i in items])


@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/JSON')
def drinkDetailJSON(drink_familyURL_id, type_id):
    """JSON End Point"""
    items = session.query(Drink).filter_by(drink_subtype_id=type_id).all()
    return jsonify(ans=[i.serialize for i in items])


@app.route('/drinks/JSON')
def drinksJSON():
    """JSON Endpoint"""
    drinks = session.query(DrinkFamily).all()
    return jsonify(ans=[r.serialize for r in drinks])


# Show all drinks
@app.route('/')
@app.route('/drinks/')
def showDrinks():
    drinks = session.query(DrinkFamily).add_columns(
        DrinkFamily.name,
        DrinkFamily.id).order_by(asc(DrinkFamily.name))
    print(drinks)
    # return "SHOW Drink Family Route!"
    return render_template('drink_family_home.html', drinks=drinks)


# Create a new drink family
@app.route('/drinks/new/', methods=['GET', 'POST'])
def newDrink():
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return redirect(url_for('showDrinks'))
    if request.method == 'POST':
        if request.form['name'] != "":
            newDrinkFamily = DrinkFamily(name=request.form['name'])
            session.add(newDrinkFamily)
            flash('New Drink Family %s Successfully Created'
                  % newDrinkFamily.name)
            session.commit()
            return redirect(url_for('showDrinks'))
        else:
            flash('New Drink Family Type Not Created.', 'error')
            return render_template('new_drink_family.html')
    else:
        return render_template('new_drink_family.html')
    # return "NEW Drink Family Route!"


# Edit a drink family
@app.route('/drinks/<int:drink_familyURL_id>/edit/', methods=['GET', 'POST'])
def editDrink(drink_familyURL_id):
    """EDIT REST endpoint"""
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return redirect(url_for('showDrinks'))
    drinkFamilyToUpdate = session.query(DrinkFamily).filter_by(
        id=drink_familyURL_id).first()
    if request.method == 'POST':
        if request.form['name']:
            drinkFamilyToUpdate.name = request.form['name']
            session.add(drinkFamilyToUpdate)
            session.commit()
            flash('Successfully Edited %s' % drinkFamilyToUpdate.name)
            return redirect(url_for('showDrinks'))
    else:
        return render_template('edit_drink_family.html',
                               drinkFamily=drinkFamilyToUpdate)

    # return "EDIT Drink Family Route!"


# Delete a drink family
@app.route('/drinks/<int:drink_familyURL_id>/delete/', methods=['GET', 'POST'])
def deleteDrink(drink_familyURL_id):
    """DELETE REST endpoint"""
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return redirect(url_for('showDrinks'))
    drinkFamilyToDelete = session.query(DrinkFamily).filter_by(
        id=drink_familyURL_id).first()
    if request.method == 'POST':
        session.delete(drinkFamilyToDelete)
        flash('%s Successfully Deleted' % drinkFamilyToDelete.name)
        session.commit()
        return redirect(url_for('showDrinks'))
    else:
        return render_template('delete_drink_family.html',
                               drinkFamily=drinkFamilyToDelete)
    # return "DELETE Drink Family Route!"


# Show drink subtypes
@app.route('/drinks/<int:drink_familyURL_id>/')
def showDrinkSubType(drink_familyURL_id):
    """SHOW REST Endpoint"""
    drinks = session.query(DrinkFamily).add_columns(
        DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    subdrinks = session.query(DrinkSubType).filter_by(
        drink_family_id=drink_familyURL_id).add_columns(
            DrinkSubType.name, DrinkSubType.id,
            DrinkSubType.drink_family_id).order_by(asc(DrinkSubType.name))
    action = drink_familyURL_id
    for subdrink in subdrinks:
        print(subdrink)
    return render_template('drink_subtype_home.html',
                           drinks=drinks, subdrinks=subdrinks, action=action)
    # return "SHOW Drink Family SubType Route!"


# Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/new/', methods=['GET', 'POST'])
def newDrinkSubType(drink_familyURL_id):
    """NEW REST endpoint"""
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return redirect(url_for('showDrinks'))
    parent_family = session.query(DrinkFamily).filter_by(
        id=drink_familyURL_id).first()
    if request.method == 'POST':
        if request.form['name'] != "":
            newSubDrinkFamily = DrinkSubType(
                name=request.form['name'],
                drink_family_id=drink_familyURL_id,
                drink_family=parent_family
            )
            session.add(newSubDrinkFamily)
            flash('%s Successfully Created' % newSubDrinkFamily.name)
            session.commit()
            return redirect(url_for(
                'showDrinkSubType',
                drink_familyURL_id=drink_familyURL_id
            ))
        else:
            flash('New Drink Sub Type Not Created.', 'error')
            return redirect(url_for(
                'showDrinkSubType',
                drink_familyURL_id=drink_familyURL_id
            ))
    else:
        return render_template('new_drink_sub_family.html')
    # return "NEW Drink Family Subtype Route!"


# Edit a drinkSubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/edit',
           methods=['GET', 'POST'])
def editDrinkSubType(drink_familyURL_id, type_id):
    """EDIT REST endpoint"""
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return(redirect(url_for('showDrinks')))
    subDrinkFamilyToUpdate = session.query(
        DrinkSubType).filter_by(id=type_id).first()
    if request.method == 'POST':
        if request.form['name']:
            subDrinkFamilyToUpdate.name = request.form['name']
            session.add(subDrinkFamilyToUpdate)
            session.commit()
            flash('Successfully Edited %s' % subDrinkFamilyToUpdate.name)
            return redirect(url_for('showDrinkSubType',
                                    drink_familyURL_id=drink_familyURL_id))
    else:
        return render_template('edit_sub_drink_family.html',
                               drinkFamily=subDrinkFamilyToUpdate)
    # return "EDIT Drink Family Subtype Route!"


# Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/delete',
           methods=['GET', 'POST'])
def deleteDrinkSubType(drink_familyURL_id, type_id):
    """DELETE REST endpoint"""
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return redirect(url_for('showDrinks'))
    drinkSubFamilyToDelete = session.query(
        DrinkSubType).filter_by(id=type_id).first()
    if request.method == 'POST':
        session.delete(drinkSubFamilyToDelete)
        flash('%s Successfully Deleted' % drinkSubFamilyToDelete.name)
        session.commit()
        return redirect(url_for('showDrinkSubType',
                                drink_familyURL_id=drink_familyURL_id))
    else:
        return render_template('delete_sub_drink_family.html',
                               subFamily=drinkSubFamilyToDelete)
    # return "DELETE Drink Family SubType Route!"


# Show drink subtype brands
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/')
def showDrinkList(drink_familyURL_id, type_id):
    drinks = session.query(DrinkFamily).add_columns(
        DrinkFamily.name, DrinkFamily.id).order_by(asc(DrinkFamily.name))
    drinklist = session.query(Drink).filter_by(
        drink_subtype_id=type_id).add_columns(
            Drink.name, Drink.id, Drink.description).order_by(asc(Drink.name))
    action_family = drink_familyURL_id
    action_sub = type_id
    for drink in drinklist:
        print(drink)
    return render_template('drink_list_home.html',
                           drinks=drinks,
                           drinklist=drinklist,
                           action_family=action_family,
                           action_sub=action_sub)


# Create a new drink subtype item
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/new/',
           methods=['GET', 'POST'])
def newDrinkList(drink_familyURL_id, type_id):
    parent_family = session.query(DrinkSubType).filter_by(id=type_id).first()
    if request.method == 'POST':
        if request.form['name'] != "":
            newDrinkL = Drink(name=request.form['name'],
                              description=request.form['description'],
                              drink_subtype_id=type_id,
                              drink_subtype=parent_family)
            session.add(newDrinkL)
            flash('%s Successfully Created' % newDrinkL.name)
            session.commit()
            return redirect(url_for('showDrinkList',
                                    drink_familyURL_id=drink_familyURL_id,
                                    type_id=type_id))
        else:
            flash('New Drink Sub Type Item Not Created.', 'error')
            return redirect(url_for('showDrinkList',
                                    drink_familyURL_id=drink_familyURL_id,
                                    type_id=type_id))
    else:
        return render_template('new_drink_sub_family_list.html')
    # return "NEW Drink Family Subtype Drink List Route!"


# Edit a drinkSubType Brand
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/edit',
           methods=['GET', 'POST'])
def editDrinkList(drink_familyURL_id, type_id, drink_id):
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return(redirect(url_for('showDrinks')))
    drinkToUpdate = session.query(Drink).filter_by(id=drink_id).first()
    if request.method == 'POST':
        if request.form['name']:
            drinkToUpdate.name = request.form['name']
        if request.form['description']:
            drinkToUpdate.description = request.form['description']
            session.add(drinkToUpdate)
            session.commit()
            flash('Successfully Edited %s' % drinkToUpdate.name)
            return redirect(url_for('showDrinkList',
                                    drink_familyURL_id=drink_familyURL_id,
                                    type_id=type_id))
    else:
        return render_template('edit_drink_item.html',
                               drinkToUpdate=drinkToUpdate)
    # return "EDIT Drink Family Subtype Drink List Route!"


# Delete a drink SubType
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/delete',
           methods=['GET', 'POST'])
def deleteDrinkList(drink_familyURL_id, type_id, drink_id):
    if 'username' not in login_session:
        flash('You need to login first', 'error')
        return(redirect(url_for('showDrinks')))
    drinkListItemToDelete = session.query(Drink).filter_by(id=drink_id).first()
    if request.method == 'POST':
        session.delete(drinkListItemToDelete)
        flash('%s Successfully Deleted' % drinkListItemToDelete.name)
        session.commit()
        return redirect(url_for('showDrinkList',
                                drink_familyURL_id=drink_familyURL_id,
                                type_id=type_id))
    else:
        return render_template('delete_drink_list.html',
                               drink=drinkListItemToDelete)
    # return "DELETE Drink Family SubType Drink List Route!"


# Show drink subtype brand detail
@app.route('/drinks/<int:drink_familyURL_id>/<int:type_id>/<int:drink_id>/')
def showDrinkListDetail(drink_familyURL_id, type_id, drink_id):
    drinks = session.query(DrinkFamily).add_columns(
        DrinkFamily.name,
        DrinkFamily.id).order_by(asc(DrinkFamily.name))
    drink_detail = session.query(Drink).filter_by(id=drink_id).add_columns(
        Drink.name, Drink.id, Drink.description).order_by(asc(Drink.name)).first()
    for drink in drink_detail:
        print(drink)
    return render_template('drink_detail.html',
                           drinks=drinks,
                           drink_detail=drink_detail,
                           type_id=type_id,
                           drink_id=drink_id)

    return "SHOW Drink Family SubType Drink List Item Detail Route!"


if __name__ == '__main__':
    app.secret_key = 'super_seotnhoenuhoeanuhoaenuh  au3242134luoaecblecret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
