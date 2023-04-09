from sqlalchemy import create_engine 
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Boolean
from sqlalchemy.orm import relationship, sessionmaker 
from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect

#creating and connecting the engine
engine = create_engine('sqlite:///:memory:', echo = True)
engine = create_engine('sqlite:///realestate.db') 
engine.connect() 
#declaring the base for schema classes
Base = declarative_base() 

class Houses(Base):
	'''
	"Houses" are kept separate from listings because:
	- Columns like # of rooms define the house, not the listing.
	- I thought of listings as more administrative (the prices, agents, etc).
	'''
	__tablename__ = 'houses'
	house_id = Column(String, primary_key = True)
	name = Column(String(20))
	bedrooms = Column(Integer)
	bathrooms = Column(Integer)
	zipcode = Column(Numeric(5,0))

	def __repr__(self):
		return "<House(id={0}, name={1}, bedrooms = {2}, bathrooms = {3}, zipcode = {4})>".format(
			self.house_id, self.name, self.bedrooms, self.bathrooms, self.zipcode)
	
class Offices(Base):
	'''
	Offices only have info that pertain to them like names, addresses & zipcodes.
	'''
	__tablename__ = 'offices'
	office_id = Column(String, primary_key = True)
	office_name = Column(String)
	office_address = Column(String)
	office_zipcode = Column(Numeric(5,0))
	def __repr__(self):
		return "<House(id={0}, name={1}, address = {2}, zipcode = {3})>".format(
			self.office_id, self.office_name, self.office_address, 
			self.office_zipcode)
	
class Agents(Base):
	'''
	Agents have their names, phones & emails.
	'''
	__tablename__ = 'agents'
	agent_id = Column(String, primary_key= True)
	agent_name = Column(String)
	agent_phone = Column(Numeric(10,0))
	agent_email = Column(String)
	def __repr__(self):
		return "<Agent(id={0}, name={1}, phone = {2}, email = {3}, office = {4})>".format(
			self.agent_id, self.agent_name, self.agent_phone, 
			self.agent_email, self.office_id)

class AgentsOffices(Base):
	'''
	Separate table for agent-office connections since 1 agent can have many offices.
	'''
	__tablename__ = 'agents_offices'
	connection_id = Column(String, primary_key = True)
	agent_id = Column(String, ForeignKey('agents.agent_id'))
	office_id = Column(String, ForeignKey('offices.office_id'))
	def __repr__(self):
		return "<Agent(id={0}, office={1}>".format(
			self.agent_id, self.office_id)


class Listings(Base):
	'''
	Listings describe all adminisrative information required.
	They map to their houses, sellers, and agents for access to the specifics.
	Again, I tried to make my queries shorter and reduced the number of index schemas.
	'''
	__tablename__ = 'listings'
	listing_id = Column(String, primary_key = True)
	house_id = Column(String, ForeignKey('houses.house_id'))
	seller_id = Column(String, ForeignKey('sellers.seller_id'))
	agent_id = Column(String, ForeignKey('agents.agent_id'))
	listed_price = Column(Numeric(10,2))
	listed_date = Column(Date)
	#I initially used IntEnum but realized Booleans go much better with conditionals
	listing_status = Column(Boolean)
	def __repr__(self):
		return "<Listing(id={0}, house={1}, seller = {2}, agent = {3}, listed price = {4}, listed date= {5}, status = {6})>".format(
			self.listing_id, self.house_id, self.seller_id, self.agent_id, 
			self.listed_price, self.listed_date, self.listing_status)

class Sellers(Base):
	'''
	Sellers have all their relevant information here.
	'''
	__tablename__ = 'sellers'
	seller_id = Column(String, primary_key= True)
	seller_name = Column(String)
	seller_phone = Column(Numeric(10,0))
	seller_email = Column(String)
	def __repr__(self):
		return "<Seller(id={0}, name={1}, phone = {2}, email = {3})>".format(
			self.seller_id, self.seller_name, self.seller_phone, 
			self.seller_email)
	
class Purchases(Base):
	'''
	The purchases schema maps only to the house ids for better normalization.
	Other info can be accessed through linking with linkings by house id.
	'''
	__tablename__ = 'purchases'
	purchase_id = Column(String, primary_key = True)
	house_id = Column(String, ForeignKey('houses.house_id'))
	sale_price = Column(Numeric(10,2))
	sale_date = Column(Date)
	def __repr__(self):
		return "<Listing(id={0}, house={1}, sold price = {2}, sold date = {3})>".format(
			self.purchase_id, self.house_id, self.sale_price, self.sale_date)

class Commissions(Base):
	'''
	The commissions table stores each commission.
	This is better than storing by agents because we can access the dates.
	This schema links to agent ids and purchase ids (for query efficiency).
	'''
	__tablename__ = 'commissions'
	commission_id = Column(String, primary_key = True)
	agent_id = Column(String, ForeignKey('agents.agent_id'))
	purchase_id = Column(String, ForeignKey('purchases.purchase_id'))
	commission = Column(Numeric(10,2))
	def __repr__(self):
		return "<Commision(id={0}, agent={1}, purchase = {2}, commission = {3})>".format(
			self.commission_id, self.agent_id, self.purchase_id, self.commission)
	
#Making sure there are no left-over data from previous sessions
Base.metadata.drop_all(bind=engine)
#Creating all of the schemas
Base.metadata.create_all(engine)

#Letting the people running the file know what's happening
print("Created the following schemas:")
inspector = inspect(engine)
schemas = inspector.get_schema_names()
for schema in schemas:
	print(inspector.get_table_names(schema=schema))