===========
WebhookTest 
===========
WebhokTest is web application written in Django, which being deployed to any web-hosting, should simplify debugging of webhooks against your local development environment. It allows to create an unique URLs, like http://webhooktest.org/<your_uid>/, and then catch request data posted to this URL. So then it could be re-submitted to your localhost by Ajax cross-domain call or by curl command.

Features
========
* Your Webhook data feeds are secure.
* Ajax call and curl command for pass-through request data to the localhost.
* Configurable Webhook alias and local endpoint URL.
* Sequential numbering of post data withing Webhook feed.
* Ability to delete post and feed.

Installation
============
::

	git clone https://github.com/aschem/webhooktest.git
	cd webhooktest
	pip install -r requirements.txt
	./manage.py syncdb
	./manage.py runserver

 
