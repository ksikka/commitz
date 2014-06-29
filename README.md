commitz
=======

Stats on commits and commit messages

API Authorization was had to be implemented since it
increases the rate limit from 60 to 5000 requests per hour.
As an added bonus, private repo commits can be analyzed, which may contain juicier commit stats.

A web server application was required since Github API doesn't support Client-side only OAuth flow.
Basic auth with AJAX was an option, but asking for Github credentials didn't seem like a good idea
since users are developers who're especially cognizant of the security risk.

The web server runs the OAuth site, and returns the access token to the client.

The rest of the logic on the frontend. API requests are made using AJAX, data is analyzed,
and the results are presented to the user.

The user can download a JSON of the data.

