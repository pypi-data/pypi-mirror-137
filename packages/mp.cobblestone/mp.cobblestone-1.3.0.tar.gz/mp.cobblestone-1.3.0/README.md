# Cobblestone

Cobblestone is a project templater to create a database-abstraction REST API. Just like [Django](https://www.djangoproject.com/), Cobblestone is not intended to implement a fully tailored database-modeling API; instead, it provides a generic starting architecture - then it's up to you to create your custom API by adding files!

Cobblestone is here to help you prototype and develop REST APIs super quickly. In particular, it provides you with an automatic router for all the resources you register to easily list instances, create a new instance, get an instance by unique id… It also offers a common way of defining your models no matter the database system you choose.

The full documentation is available [over here](https://minapecheux.gitlab.io/cobblestone/).

## TL;DR

_Note: check out the [official Getting started guide](https://minapecheux.gitlab.io/cobblestone/docs/getting-started/) for more details on setting up a Cobblestone project._

### Install the Cobblestone Python library

*Note: it is recommended to use a virtual env to avoid mixing up all of your dependencies. For example, you can use `venv` or `pipenv` to make a clean environment for your project.*

To install the Cobblestone module, run:

```
pip install mp.cobblestone
```

### Initialize a new project

You now have a new CLI command available: `cobblestone init`. To create your project, simply run:

```
cobblestone init <project_name>
```

### Start up the project

To run your newly created project, simply use the `cobblestone start` command:

```
cobblestone start [--debug] <project_name>
```

⚠️ This command will require Docker to be up and running on your computer.

### Test it out!

To check everything is working:

1. go to http://localhost:8000/docs: you should see a nice Swagger doc with some auto-generated endpoints for the "user" resource! However, you need some users in your database to access them because they are protected via the OAuth2 scheme and require an access token.

2. run the database init script to create an admin user:

    ```
    python db_init.py
    ```

    By default, this script will only add an admin user to the database (with login "admin" and password "admin"). You may create your own users in addition by passing extra args to the script:

    ```
    python db_init.py --users <user1>:<pwd1> <user2>:<pwd2> ...
    ```

3. finally, head back to the Swagger doc and try to run the `/users-me` endpoint. First, click on the lock at the top-right corner and use one of the users you created (or the admin one) to log in; then, click on "Try it out" and execute the request: this should return a JSON payload with the login, firstname, lastname and unique id of the user you connected as.

### Deploy and run the project with Docker

When you are satisfied with your API, you may want to deploy the whole project. To do so easily, you can containerize it using Docker. To help you in this task, Cobblestone CLI has various Docker-like commands: `deploy`, `run` and `stop`.

To create and run a Docker image containing your API (plus the associated database if need be), run:

```
cobblestone deploy <project_name>
cobblestone run <project_name>
```

To stop your API docker (and the associated database container if there is one), use:

```
cobblestone stop <project_name>
```
