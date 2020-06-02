# Herolo messaging system

A simple messaging RestAPI written in python  
The service can be reached at https://herolo.duckdns.org
# Components

 - **Traefik** - a revearse proxy for accessing the REST API
 - **App** - REST API service 
	 - `Flask` as wsgi framework
	 - `gunicorn` as wsgi server 
 - **RDS** - A MySQL instance on AWS to presist the data  

# Deployment
The app is deployed in AWS on a EC2 instance with Docker engine installed.
the instance is configured as a swarm with a single manager node in order to enable to scale the app.

stack details:
 - The messaging REST API App scaled to 4 instances [link to App image at Docker hub](https://hub.docker.com/r/nissy34/herolo)
 - Traefik as a revearse proxy and automatic ssl certs [link to the image at Docker hub](https://hub.docker.com/_/traefik) 
	 - [Link to traefik dashboard](https://admin:adminadmin@traefik.herolo.duckdns.org/) (user: admin, password: adminadmin)


![Deployment](https://raw.githubusercontent.com/nissy34/Herolo-messaging-system/master/github/Deployment.png)

# DB schema
![schema](https://raw.githubusercontent.com/nissy34/Herolo-messaging-system/master/github/DBSchema.png)
<br/>**Note** a user can send a message to **more then one receiver** hence the meny-to-many between users and messages 
# Getting started

 1. create a user on the system with the `/users` endpoint
 2. get your token with the `/users/<username>/token` endpoint
 now that your user is set up and you have a token you can send and get messages

# RestAPI
**Base** https://herolo.duckdns.org
 - `/users`
	 - description: Create a user in the system
	 - method: `POST`
	 -  body: `{
			 username:<>,
			 email:<>,
			 password:<>
	      }`
	      
 - `/users/<username>/token`
  	 - description: create a Bearer token for the user
	 - method: `POST`
	 -  body: `{
			 password:<string>
	      }`
	      
 - `/users/<username>/messages`
     - description: Create a user in the system 
	     - **note** for now the endpoint only supports a single receiver
	 - method: `POST`
	 - header: `Authorization: Bearer <token>` - the Bearer token 
	 -  body: `{
			  receiver:<string - the receiver username>, 
			 subject:<string>,
			 message:<string>
	      }`
	      
 - `/users/<username>/messages?unread="true"&per_page=20%page=1`
     - description: Get **received** messages for the given user
	 - method: `GET`
	 - header: `Authorization: Bearer <token>` - the Bearer token 
	 -  query: 
		 - `unread=<"true"|"false">` - optional
			 - `unread="true"` return only unread messages
			 - `unread="false"` return only messages that have been read
			 - if not present return all messages
		 - `per_page=<int>` - optional (default 20) 
			 - max number of messages to return
		 - `page=<int>` - optional (default 1)
			 - which page of result to return
	 
		 
 - `/users/<username>/messages/<message_id>`
     - header: `Authorization: Bearer <token>` - the Bearer token
	 - method: `PATCH`
		 - description: Set a **received** message as read or unread
		 - body `{ read:<"true"|"false">}`
	  - method: `Delete`
		 - description: Delete the message. if the user is the sender it deletes the message from all receivers if the user is the receiver it only deletees the message from the receiver feed
