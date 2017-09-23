Refugive
========

Motivation
----------
This is a sharing Website. It helps people to exchange good for free.

Installation
------------
Run following command to get the source code:

	git clone https://spy@s55969da3.adsl.online.nl/refugive/back-end.git --recursive

Now you have to go inside the folder. First you have to install the requirements:

	pip install -r requirements.txt

To run the webserver:

	./manage.py runserver

Now you can open a webbrowser and type http://localhost:8000.

Admin username and password
----------------------------
Open a terminal and run this command:

	./manage.py createsuperuser

You should be now able to login at:

	http://localhost:8000/admin/

Using These Examples
--------------------
The various folders and files in this repository correspond to the projects created throughout the book.

Terms & Conditions
------------------
This application is base on an example from “Lightweight Django by Julia Elman and Mark Lavin (O’Reilly). Copyright 2014 Julia Elman and Mark Lavin. 978-1-4919-4594-0.”
