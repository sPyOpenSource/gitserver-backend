Git Server Backend
==================

Motivation
----------
This is a sharing Website. It helps us to exchange source codes.

Installation
------------
Run following command to get the source code:

	git clone git://s55969da3.adsl.online.nl/gitserver/back-end.git --recursive

Now you have to go inside the folder. First you have to install the requirements:

	pip install -r requirements.txt

To run the webserver:

	./manage.py runserver

Now you can open a webbrowser and type http://localhost:8000.

Testing
-------
To test the code you can run following command:

	./manage.py test

Terms & Conditions
------------------
This application is base on an example from “Lightweight Django by Julia Elman and Mark Lavin (O’Reilly). Copyright 2014 Julia Elman and Mark Lavin. 978-1-4919-4594-0.”
