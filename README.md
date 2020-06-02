# Herolo messaging system

A simple messaging RestAPI written in python 

# Deployment



# RestAPI

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
			 password:<>
	      }`
	      
 - `/users/<username>/messages`
     - description: Create a user in the system
	 - method: `POST`
	 - header: `Authorization: Bearer <token>` - the Bearer token 
	 -  body: `{
			 receiver:<"the receiver username">,
			 subject:<"the subject">,
			 message:<"the message">
	      }`
	      
 - `/users/<username>/messages?unread=true`
     - description: Get messages for the given user
	 - method: `GET`
	 - header: `Authorization: Bearer <token>` - the Bearer token 
	 -  query: `unread` - optional
		 - `unread="true"` return only unread messages
		 - `unread="false"` return only messages that have been read
		 - if not present return all messages
		 
 - `/users/<username>/messages/<message_id>`
     - header: `Authorization: Bearer <token>` - the Bearer token
	 - method: `PATCH`
		 - description: Set message as read or unread
		 - body `{ read:<"true"|"false">}`
	  - method: `Delete`
		 - description: Delete the message. if the user is the sender it deletes the message from all receivers if the user is the receiver it only deletees the message from the receiver feed

	
