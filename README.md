**In progress**
# pyCors
A Python Flask-based proxy adding Access-Control-Allow-Origin to all responses.
A fork of cors-proxy with the added feature of being deployable via docker, allowing you to define Origins via environment variables, and allowing you to set Access-Control-Allow-Credentials to true via environment variables (default remains false).

## Instructions
1. 
You can then access `http://127.0.0.1:5000/<URL>` for any `URL` and any HTTP method. The response content and return code will be forwarded.

Example: Access `https://jsonplaceholder.typicode.com/posts` with `http://127.0.0.1:5000/https://jsonplaceholder.typicode.com/posts`.


Docker Usage