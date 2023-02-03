# qmenta

There are three folder on the repository:

 - database: Which contains all needed files to create the Database server Docker image
 - server_app: With all the files needed for running the server backend app
 - vanilla_app: Containing html and javascript files to execute the front end


Unfortunatelly, I haven't had enough time for making them all work together. It seems to be problems with the network for the containers


For executing, I have had to start the Database Docker. Then starting the server_app and finally, I use Postman to send the requests to the backend. 

The problem for the front_end is that, as the apache is not serving the pages, the cookies created on the backend are not properly recovered and therefore the app is not working


Also to be taken into account is that I created a virtual env for developing the server_app. I attached the file requirements.txt for installing all the needed packages
