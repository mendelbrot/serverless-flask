This is a serverless flask application with basic features that most apps would need to get going. It has:

* environment variables
* a connection to a database
* logging
* json schema validation

If you want to program in Python, and use Serverless, then Flask is a good choice because it's lightweight.  It transitions well from the original purpose as a server which is constantly running and handles everything, to becoming a microservice with a small area of concern that's quickly spun up when needed and then shut down.  

[Here's a slightly different tutorial for reference.](https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb)

### What this app does

It's expecting an http get request.  It will be a json request so it needs the header `Content-Type application/json', and the request body has the form:

```
{
    "name": "Greg"
}
```

In my mongo database there's a people collection with a document having the property `name: "greg"`.  When it finds a name it its people collection that matches the request, this app will respond with:

```
{
    "message": "Hello Greg!"
}
```

.  Otherwise, if it doesn't find the matching name or there is any other error, it responds with:

```
{
    "message": "Did not find person."
}
```

Just for fun, and for no particular reason, it also does schema validation on the request and response json.

### Prerequisites

You have an AWS account and you've maybe used the [AWS CLI](https://aws.amazon.com/cli/) before.

### Getting started

This app is connected to a mongo database.  In the project directory, you will need to create a .env file and put in `DATABASE_URL=<your database connection string>`.  (Double check that it is git ignored.) I assume that you have a mongo database already set up, or you will change the code to connect to your preferred database. 

Next, make sure [serverless](https://www.npmjs.com/package/serverless) is installed.  Serverless is an npm package that is meant to be installed globally.  In Ubuntu, I had problems with permissions running global packages that were installed with sudo.  I did some research and found [nvm](https://github.com/nvm-sh/nvm), a version manager for node.  This is installed for the user (not requiring sudo) so it fixes the permission problem and has the added benefit that you can easily switch between different versions of node if you ever need to.

To install nvm and get the latest long-term support version of node:

```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash
$ nvm install --lts
```

Then you will want to make sure you know what version you are using and have it set as the default.  I did `$ nvm ls 14` which gave me the exact version of node 14 I had installed.  (In my case it was 14.15.1)  And then I set that to be the default with `$ nvm alias default 14.15.1`

Once node was set up, I installed serverless globally:

```
npm i -g serverles
```

Then in the project directory, run `npm install` to create the node_modules folder with the packages serverless needs to run and deploy the app.  One package to mention is [serverless-wsgi](https://www.npmjs.com/package/serverless-wsgi).   It allows the app to be served locally for development and testing.

Next, we need to install the Python packages.  I like to create a [virtual environment](https://pypi.org/project/virtualenv/) in the project directory:

```
$ virtualenv venv --python=python3
```

To activate and deactivate the environment:

```
$ source venv/bin/activate
$ deactivate
```

Now to install the packages.  This project uses a requirements.txt to keep track of the Python dependencies, much like the package.json tracks the node dependencies.

To install the packages listed in requirements.txt: 

```
pip install -r requirements.txt
```

If you install new packages, you will need to add them to the requirements.txt file.  The command `$ pip freeze > requirements.txt` will update requirements.txt with all of the packages currently installed in your venv. 

Before running anything, take a minute to make sure the settings in serverless.yml are good.  Here's a snippet of the provider and functions settings:

```
provider:
  name: aws
  runtime: python3.8
  region: us-west-2

functions:
  app:
    handler: wsgi_handler.handler
    name: serverless-flask
    events:
      - http: 
          path: /
          method: get
```

Under provider, you can change the region, and you can put a profile name.  (The profile setting will use credentials from the specified [AWS profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) if you have those stored on your computer.)  Setting `profile: greg` in the .yml would be equivalent to deploying with the `--profile greg` option.

Under functions, `name: serverless-flask` sets the name of the lambda function that's deployed. 

Now everything should be set to go LoL!

To run locally:

```
$ sls wsgi serve
```

To deploy to AWS:

```
$ sls deploy
```

