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

