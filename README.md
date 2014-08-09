commitz
=======

Stats on all of your github repos.

A web server application was required since Github API doesn't support Client-side only OAuth flow.

Dependencies
------------

- python 2.7
- Flask
- couchdb

Configuration
-------------

Create a JSON at the root of the repo called `config.json`:

    {
        "GITHUB_CLIENT_ID":"XXX",
        "GITHUB_CLIENT_SECRET":"XXX",
        "GITHUB_CALLBACK_URL":"http://devserver.com:5000/auth", /* REPLACE W YOUR domain:port */
        "GITHUB_CALLBACK_SHORT_URL":"/auth",
        "DEBUG": true,
        "SECRET_KEY": "XXX"
    }

How to run
----------

1. run couchdb in a terminal somewhere
2. run python server.py
3. add this to your /etc/hosts : `127.0.0.1	devserver.com`
4. then go to devserver.com:5000 and you should see a page

