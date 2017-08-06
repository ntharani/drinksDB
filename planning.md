# Outline of Approach

0. Choose what to have as a catalog.
1. Create visual mockup of what this could look like
2. Do data modeling in SQL, use sqlalchemy to create DB schema.
3. Create data to populate DB.
4. Create routes for this in python main file along with templates for each route under /templates.
5. Debug.

## 0. Drinks. (Don't think less of me)

Categories > List of SubTypes (Add / Delete) > Detail (Add / Delete)

Beer - Ale, Lager, 
Wine - Chardonay, Reisling, Merlot, Malbec, Cabernet Sauvingion
Spirits - Gin, Vodka, Rum
Mixers - Gin and Tonic, Rum n' Coke
Cocktails - Caipirinhia, Mojito
Other - Sake.

High Level Taxonomy:

Drink > Drink_Type > Drink Detail

Architecture:

Don't see this going past 140TB, and even 1TB, so SQLLite is appropriate for this.
Also bundled with Python so makes like a bit easier.

## 1. Done, will upload later.

## 2. Oooh.. online SaaS tools. :)

https://repository.genmymodel.com/ntharani/catalog

Based on this diagram, 3 x Classes

Class DrinkClass, Class DrinkSubType, Class Drink

## 3


