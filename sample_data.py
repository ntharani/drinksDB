"""Populates drinks.db with sample.data"""
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
 
from database_setup import DrinkFamily, DrinkSubType, Drink, User, Base

#engine = create_engine('sqlite:///drinks.db')
engine = create_engine('postgresql://catalog:udacityNagib@localhost/ndrinks')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def populate_users(item):
    element = User(
        name = item["name"],
        email = item["email"],
        picture = item["picture"]
    )
    session.add(element)
    session.commit()

def populate_drink_family(item):
    user_i = session.query(User).filter_by(name = "Mary Poppins").first()
    print("populate drink method")
    print(user_i.name)
    element = DrinkFamily(name=item, user = user_i)
    session.add(element)
    session.commit()

def populate_beer(item):
    user_i = session.query(User).filter_by(name = "Mary Poppins").first()
    beerfamily = session.query(DrinkFamily).filter_by(name = "Beer").first()
    element = DrinkSubType(name = item, drink_family = beerfamily, user = user_i)
    session.add(element)
    session.commit()

def populate_ale(item):
    user_i = session.query(User).filter_by(name = "Mary Poppins").first()
    alefamily = session.query(DrinkSubType).filter_by(name = "Ale").first()
    element = Drink(
        name = item["name"], 
        drink_subtype = alefamily,
        description = item["description"],
        user = user_i
        )
    session.add(element)
    session.commit()


def populate_db():

    # Drink Families
    users = [
        {
        "name": "Mary Poppins",
        "email": "me@nagibtharani.com",
        "picture": "https://secure.gravatar.com/avatar/a36aecb1e7c20dbcc6f37254a0c438d3?s=64"
        }
    ]
    drinks_family_data = ["Beer", "Wine", "Mixers", "Spirits", "Cocktails","Other"]
    beers_data = ["Ale", "Stout", "Lager"]
    ale_data = [
        {
            "name": "Schneider Weiss",
            "description": "Schneider"
        },{
            "name":"Widmer Hefeweizen",
            "description": "Heferwiezen!!"
        },{
            "name": "Flying Dog in Heat Wheat",
            "description": "It's a wierd one."
        }
    ]
    wine_data = ["Merlot", "Cabernet Sauvingion","Chardonnay"]

    for user in users:
        populate_users(user)

    print("Done Users!")
    print(session.new)
    print(session.query(User.name).all())

    for drink in drinks_family_data:
        populate_drink_family(drink)

    print("Done Drinks!")
    print(session.new)
    print(session.query(DrinkFamily.name).all())

    for beer in beers_data:
        populate_beer(beer)

    print("Done Beers!")
    print(session.new)
    print(session.query(DrinkSubType.name).all())
    
    for ale in ale_data:
        populate_ale(ale)

    print("Done Ales!")
    print(session.new)
    print(session.query(Drink.name, Drink.description).all())

populate_db()

print("Drinks Table is")
abc = session.query(DrinkFamily).join(User).order_by(asc(DrinkFamily.name))
for a in abc:
    print('drinks table is %s %s') % (a.name, a.user_id)

print("Drinks SubType Table is")
abc = session.query(DrinkSubType).order_by(asc(DrinkSubType.name))
for a in abc:
    print(a.name)

print("Drinks List Table is")
abc = session.query(Drink).join(User).add_columns(User.name).order_by(asc(Drink.name))
for drink, user in abc:
    print(drink.name, user)
