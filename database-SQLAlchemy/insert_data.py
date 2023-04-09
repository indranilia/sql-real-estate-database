from create import *
from faker import Faker
import random
from dateutil.relativedelta import relativedelta
from sqlalchemy import update
from decimal import Decimal
import uuid
#set variables here! I figured changing the code here might be cleaner.
#(I had initially set these as user inputs but didn't want to annoy anyone).

#for houses and purchases (should be a larger number)
a = 100

#I have around the same number here, but every function takes n inputs
#Feel free to play around with different numbers

#for agents, offices, and sellers (2 or 3 times smaller than a)
b = 50

#using the faker library for really nice fake data!
fake = Faker()

#starting the session and binding to the engine
Session = sessionmaker(bind=engine)
session = Session()

#Fake data generators

#STARTING WITH THE INDEPENDENT SCHEMAS (not foreign keyed by others)

def fake_houses(n):
    '''
    - Id as uuid
    - Faker for address data
    - Rand integers for # of rooms (feel free to change)

    input - number of fake houses needed
    output - list of n instances in a list
    '''
    houses = []
    for house in range(n):
        house_id = str(uuid.uuid1())
        name = fake.street_name()
        bedrooms = random.randint(1,10)
        bathrooms = random.randint(1,10)
        zipcode = fake.postcode()
        #creating an instance of Houses
        house = Houses(house_id = house_id, name = name, bedrooms = bedrooms, 
                   bathrooms = bathrooms, zipcode = zipcode)
        #storing together to run at once
        houses.append(house)
    return houses

def fake_offices(n):
    '''
    - Id as uuid
    - Faker for address data and names 
    - The office names look like human names, don't be alarmed

    input - number of fake offices needed
    output - list of n instances in a list
    '''
    offices = []
    for i in range(n):
        office_id = str(uuid.uuid1())
        office_name = fake.name()
        office_address = fake.street_address()
        office_zipcode = fake.postcode()  
        #creating an instance of Offices  
        office = Offices(office_id = office_id, office_name = office_name,
                         office_address = office_address, 
                         office_zipcode = office_zipcode)
        #storing together to run at once
        offices.append(office)
    return offices

def fake_sellers(n):
    '''
    - Id as uuid
    - Faker for address names and emails 
    - Just used randint for phone numbers because the faker numbers are weird

    input - number of fake sellers needed
    output - list of n instances in a list
    '''
    sellers = []
    for i in range(n):
        seller_id = str(uuid.uuid1())
        seller_name = fake.name()
        seller_phone = random.randint(1111111111,9999999999)
        seller_email = fake.email()
        #creating an instance of Sellers  
        seller = Sellers(seller_id = seller_id, seller_name = seller_name, 
                         seller_phone = seller_phone, seller_email = seller_email)
        #storing together to run at once
        sellers.append(seller)
    return sellers

#Running the faker functions and adding them to the sessions
#Not committing for now because the main sales isn't in yet
all_houses = fake_houses(a)
session.add_all(all_houses)
print("Added fake houses to the database!")
all_offices = fake_offices(b)
session.add_all(all_offices)
print("Added fake offices to the database!")
all_sellers = fake_sellers(b)
session.add_all(all_sellers)
print("Added fake sellers to the database!")


#THE NEXT BUNCH IS DEPENDENT ON OTHER SCHEMAS
def fake_agents(n):
    '''
    - Same logic as the other functions above to generate agents
    - For now, just random choosing an office out of those added earlier

    input - number of fake agents needed
    output - list of n instances in a list
    '''
    agents = []
    for agent in range(n):
        agent_id = str(uuid.uuid1())
        agent_name = fake.name()
        agent_phone = int(random.randint(1111111111,9999999999))
        agent_email = fake.email() 
        agent = Agents(agent_id = agent_id, agent_name = agent_name, 
                       agent_phone = agent_phone, agent_email = agent_email)
        agents.append(agent)
    return agents

#Running the faker function and adding all the agents
#Also, not the main sales data, so not committing
all_agents = fake_agents(b)
session.add_all(all_agents)
print("Added fake agents to the database!")

def fake_agent_offices(n):
    '''
    - Maps agents to offices (one agent can have several offices)
    - Index table

    input - number of fake connections needed
    output - list of n instances in a list
    '''
    agentsoffices = []
    for agent in all_agents:
        connection_id = str(uuid.uuid1())
        agent_id = agent.agent_id
        #office ids can repeat
        office_id = random.choice(all_offices).office_id
        agent_office = AgentsOffices(connection_id = connection_id, 
                                     agent_id = agent_id, office_id = office_id)
        agentsoffices.append(agent_office)
    return agentsoffices

all_agents_offices = fake_agent_offices(b)
session.add_all(all_agents_offices)
print("Added fake agents-offices to the database!")

def fake_listings(n):
    '''
    - Same logic as above
    - But choosing 1 for all statuses as a start (1 = available/listed)
    - Randomly chose houses, sellers, and agents (all independent of each other)
    '''
    listings = []
    for listing in range(n):
        listing_id = str(uuid.uuid1())
        listed_price = round(random.choice(range(50000,2000000)), 2)
        listed_date = fake.date_this_year()
        listing_status = 1
        house_id = random.choice(all_houses).house_id
        seller_id = random.choice(all_sellers).seller_id
        agent_id = random.choice(all_agents).agent_id
        listing = Listings(listing_id = listing_id, listed_price = listed_price,
                           listed_date = listed_date, listing_status = listing_status,
                           house_id = house_id, seller_id = seller_id, 
                           agent_id = agent_id)
        listings.append(listing)
    return listings

#Running the faker function and COMMITTING THIS TIME
#Because listings must be kept for history and carry important sales data
all_listings = fake_listings(a)
session.add_all(all_listings)
print("Added fake listings to the database!")
session.commit()


def fake_purchases():
    '''
    Getting fake purchases by:
    1. Randomly choosing an existing listing
    2. Matching the sale prices and dates to that 1 specific listing
    3. Prices fluctuate by -200 to 1000 (Does is show that I know nothing about real estate)
    4. The sale dates randomly increase by 1-12 months 
    5. As soon as any purchase is made, the status of the listing is updated (0 = sold)
    6. But, if the function does not work, the listing won't change and the purchase won't be recorded
    '''
    purchases = []
    for i in all_listings:
        if i.listing_status == True:
            purchase_id = str(uuid.uuid1())
            house_id = i.house_id 
            sale_price = i.listed_price + round(random.choice(range(-200,1000)), 2)
            sale_date = i.listed_date + relativedelta(months=random.randint(1,12))
            purchase = Purchases(purchase_id = purchase_id, house_id = house_id, 
                                    sale_price = sale_price, sale_date = sale_date)
            purchases.append(purchase)
            i.listing_status = False
    return purchases

#Committing immediately to not lose data
all_purchases = fake_purchases()    
    
session.add_all(all_purchases)
session.commit()

def add_commissions():
    '''
    Separate table for the commissions:
    - Sorted by commissions so that we can access the dates of each commission by linking it to the purchase
    - The commissions are calculated by the groups given in the assignments
    '''
    commissions = []
    for purchase in all_purchases:
        commission_id = str(uuid.uuid1())
        agent_id = session.query(Listings.agent_id).filter(Listings.house_id == 
                                                        purchase.house_id)
        purchase_id = purchase.purchase_id
        price = purchase.sale_price
        if price <= 100000:
            commission = round(Decimal(price)*Decimal(0.1),2)
        elif price > 100000 and price <= 200000:
            commission = round(Decimal(price)*Decimal(0.075), 2)
        elif price > 200000 and price <= 500000:
            commission = round(Decimal(price)*Decimal(0.06), 2)
        elif price > 500000 and price <= 1000000:
            commission = round(Decimal(price)*Decimal(0.075), 2)
        else:
            commission = round(Decimal(price)*Decimal(0.04), 2)
        commission = Commissions(commission_id = commission_id, agent_id = agent_id,
                                 purchase_id = purchase_id, commission = commission)
        commissions.append(commission)
    return commissions

#Committing the commissions too because they are based on purchases
#I was not sure if they should be committed with the purchases
#But I figured the safer, the better
all_commissions = add_commissions()
session.add_all(all_commissions)
session.commit()
print("Added fake purchases to the database!")

#closing this session
session.close()
