# Floy Technical Challenge

## Questions

**1. What were the reasons for your choice of API/protocol/architectural style used for the client-server communication?**
Flask is a very simple, feature rich and versatile rest_api framework. Mongo_db combines very good with flask and the fact that the data model does not include any relation between tables makes a document oriented db more appealing.




**2.  As the client and server communicate over the internet in the real world, what measures would you take to secure the data transmission and how would you implement them?**

I'd Protect the endpoints with oauth and jwt tokens, implemented in every method of the api and add a method for token generation validating a user key. 
