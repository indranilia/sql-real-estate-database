# Real Estate Head Office
## Overview

A fictitious real estate database with data and queries made as part of coursework. 

## Execution

For macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```

For Windows:

```cmd
python3 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```
## Testing

I used the faker and random libraries to make fictitious data and test my inserts
and queries. 

How the fake data looks (example):
![Example schema](Schema.png)

How the output of the queries looks (example):
![Example queries](Outputs.png)

## Implementation notes


###Inserting data

(from the assignment description)

1. Whenever a house is listed then the following things need to happen:
  - All the relevant details of that house need to be captured, ie. at least: seller details, # of bedrooms, # of bathrooms, listing price, zip code, date of listing, the listing estate agent, and the appropriate office.
2. Whenever a house is sold then the following things need to happen:
  - The estate agent commission needs to be calculated. This happens on a sliding scale:
      - For houses sold below $100,000 the commission is 10%
      - For houses between $100,000 and $200,000 the commission is 7.5%
      - For houses between $200,000 and $500,000 the commission is 6%
      - For houses between $500,000 and $1,000,000 the commission is 5%
      - For houses above $1,000,000 the commission is 4%
  - All appropriate details related to the sale must be captured, ie. at least: buyer details, sale price, date of sale, the selling estate agent.
  - The original listing must be marked as sold.

###Queries

(from the assignment description)

Find the top 5 offices with the most sales for that month.
Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
Calculate the commission that each estate agent must receive and store the results in a separate table.
For all houses that were sold that month, calculate the average number of days on the market.
For all houses that were sold that month, calculate the average selling price


### Normalization

Up to 4NF (arguably).

- **1NF** - None of my schemas have doubles or composite data. I thought maybe I
should separate the dates into years, months, and days, but it is usually 
considered a single non-composite data and it's easy to calculate everything 
even without separating.

- **2NF** - All non-id columns depend on the column.For example, sellers only 
have their relevant info (same goes for agents, offices, houses). All other data
like listings still depend on the primary key (who the agent is dependent on 
what the listing is).

- **3NF** - All fields must be determined only by the key. All of my schema 
follow this idea. For example, my agents table only has agent-related info. The
agents-offices connection is kept separately in a agents-offices table.

- **4NF** - My schemas all have no multi-valued dependencies.
For example,  the listings only have relevant information, while houses is a 
separate schema with details about rooms and agents is also a separate schema
with contact info and names. For the commissions table though, I kept the admin_id
in even though it can be mapped separately through the listings (each listing
uniquely maps a house to an agent). I figured that since commissions are only
given to agents (at least in this scenario), this was okay still.

### Indices

- I created an index table for agents-offices connections since that is the 
one-to-many relationship specified in the assignment. Searching the indexes
for agents-offices first significantly reduces the search time.
- The listings are linked to house, agent, and seller ids. While I could have 
gone further and made separate schemas for each link, the combination of these ids
is unique and independent of each other. 
- We could use compositve or covering indices for the other tables, but the existing
indice linkings already make the queries quite efficient. I would consider other 
more comprehensive types if the dataset became exponentially larger.

### Transactions

- For the transactions, I focused on one main thing - every time there is a purchase,
there must also be an update to the listing status. If not, the whole transaction 
should fail. Thus, the insertions to purchases happens in the same function as the
listing update.
- The commissions are only committed if the purchases had been successfully committed.


**Notes on acid**
- A - purchase and listing status update fail together, commisions fail without 
purchases.
- C - the tables stay consistent. You can see that as soon as the purchases are 
made, the listings change, so no house is purchased and available. 
- I - each session happens in isolation, made sure by constraints in the function.
- D - changes persist from function to function. (NOTE:For testing purposes, 
the data is cleared upon initialization but this can be easily changed 
in `create.py`.)
