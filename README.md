# Real Estate Head Office
## Overview

I coded this Assignment in SQL Alchemy. 

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
