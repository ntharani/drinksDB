"""Populates drinks.db with sample.data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import DrinkFamily, DrinkSubType, Drink, Base

engine = create_engine('sqlite:///drinks.db')
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


def populate_drink_family(item):
    element = DrinkFamily(name = item)
    session.add(element)
    # session.commit()

def populate_beer(item):
    element = DrinkSubType(name = item, drink_family = DrinkFamily(name="Beer"))
    session.add(element)
    # session.commit()

def populate_ale(item):
    element = Drink(
        name = item["name"], 
        drink_subtype = DrinkSubType(name="Ale"),
        description = item["description"]
        )
    session.add(element)
    # session.commit()


def populate_db():

    # Drink Families
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
