# pyCors
A Python Flask-based proxy adding Access-Control-Allow-Origin to all responses.
A fork of cors-proxy with the added feature of being deployable via docker, allowing you to define Origins via environment variables, and allowing you to set Access-Control-Allow-Credentials to true via environment variables (default remains false).
Can be found on [DockerHub](https://hub.docker.com/r/heyitsjono/pycors/).

## Instructions
Can be run from either `docker` or `docker-compose`.

For docker-compose:
Set up your `docker-compose.yml` file to include pycors, for example:

	services:
  	  pycors:
    	container_name: pycors
    	image: heyitsjono/pycors:latest
    	ports:
      	+ 5757:5000
    	environment:
      	+ ALLOW_ORIGIN=http://URL1,https://URL1,http://URL2
      	+ ALLOW_CREDENTIALS=false
    	restart: unless-stopped

Set `ALLOW_ORIGIN` to one origin (the IP/URL making the request to the pycors), or a comma-delimited list of origins.
Alternatively, you can also set `ALLOW_ORIGIN` to `*` to allow requests from any origin.
By default, `ALLOW ORIGIN` is not set to any value, in other words by default `Access-Control-Allow-Origin` will not be set to any value.

Set `ALLOW_CREDENTIALS` to `true` to enable `Access-Control-Allow-Credentials`, by default this is disabled.

From there just run `docker-compose up -d pycors`.

You should then be able to make requests to`http://127.0.0.1:5757/<URL>` for any `URL` and any HTTP method. The response content and return code will be returned to your service with the above `Access-Control-Allow-Origin/-Credentials` defined in the environment variables set.

For example: Access `https://jsonplaceholder.typicode.com/posts` with `http://127.0.0.1:5757/https://jsonplaceholder.typicode.com/posts`.
