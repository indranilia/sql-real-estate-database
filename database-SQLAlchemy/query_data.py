from create import Offices, Purchases, Listings, Agents, AgentsOffices, Commissions, Houses, Sellers, engine
from insert_data import session
from datetime import *
from sqlalchemy import func
from sqlalchemy.orm import relationship, sessionmaker 

#I was not sure if I should completely separate the engine for this
#But since this is all for testing, I figured there is not much harm keeping them together

#Set dates here
start = date(2023, 7, 1) 
end = date(2023, 8, 1)

#All Queries have been double-checked manually (using sqlite viewer's filter)
#They follow the assignment instructions and print all results

print("Top 5 offices with the most sales between {0} and {1}".format(start, end))
query1 = session.query(Offices.office_address,
                        func.sum(Purchases.sale_price)).group_by(
                        Offices.office_id).filter(AgentsOffices.office_id == 
                        Offices.office_id).filter(
                        Listings.agent_id == AgentsOffices.agent_id).filter(
                        Purchases.house_id == Listings.house_id, 
                        Purchases.sale_date.between(start, end)).order_by(func.sum(Purchases.sale_price).desc())
print(query1.limit(5).all())

print("Top 5 Agents with the most sales between {0} and {1}".format(start, end))
query2 = session.query(Agents.agent_name, Agents.agent_email,
                        Agents.agent_phone,func.sum(Purchases.sale_price)).filter(
                        Listings.agent_id == Agents.agent_id).filter(
                        Purchases.house_id == Listings.house_id, 
                        Purchases.sale_date.between(start, end)).group_by(
                        Agents.agent_id).order_by(func.sum(
                        Purchases.sale_price).desc())
print(query2.limit(5).all())

print("Calculating commissions for each estate agent between {0} and {1}".format(start, end))

query3 = session.query(Agents.agent_name, func.sum(Commissions.commission)).group_by(Agents.agent_id).filter(
                        Agents.agent_id == Commissions.agent_id).filter(
                        Listings.agent_id == Agents.agent_id).filter(
                        Purchases.house_id == Listings.house_id, Purchases.sale_date.between(start, end))

print(query3.all())

print("Calculating the average number of days on the market for the houses sold between {0} and {1}".format(start, end))
query4 = session.query(func.avg(func.julianday(Purchases.sale_date)) -
                            func.julianday(Listings.listed_date)).filter(Purchases.house_id == 
                        Listings.house_id, Purchases.sale_date.between(start, end))

print(query4.all())

print("Calculating the average selling price for the houses sold between {0} and {1}".format(start, end))
query5 = session.query(func.avg(Purchases.sale_price)).filter(Purchases.sale_date.between(start, end))

print(query5.all())

#closing this session
session.close()