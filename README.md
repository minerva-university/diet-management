# Welcome to CS162 Final Project

This is a Diet Managment web application that produce diet recommendations and weight tracking.

## Project's branches

The project has two branches:

- `Main`: easier deployment
- `Deployment`: deploying using docker and multiple containers

## `Main` Branch
### Run the application
#### Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements

- Python 3
- Pip 3

```bash
brew install python3
```

Pip3 is installed with Python3

##### Installation

To install virtualenv via pip run:

```bash
pip3 install virtualenv
```

##### Usage

Creation of virtualenv:

```bash
virtualenv -p python3 venv
```

If the above code does not work, you could also do

```bash
python3 -m venv venv
```

To activate the virtualenv:

```bash
source venv/bin/activate
```

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

```bash
venv\Scripts\activate
```

To deactivate the virtualenv (after you finished working):

```bash
deactivate
```

Install dependencies in virtual environment:

```bash
pip3 install -r requirements.txt
```

#### Run Application

Start the server by running:

```bash
python3 run.py
```

if you are on windows:

for only one time of initializing the db

```bash
python3 insert_meals.py
```

Then:

```bash
python3 server.py
```

## `Deployment` branch

This branch uses Docker containers to deploy the application. You have firstly to checkout to the branch using git.

```bash
git checkout deployment
```

### running the application

To run the application you should have docker installed and then run the following commands:

```bash
docker build -t diet .
docker swarm init
docker stack deploy -c docker-compose.yml diet-swarm
```

For turning the application off:

```bash
docker stack rm diet-swarm
docker swarm leave --force
```

To run the integration tests:

```bash
docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit test
docker-compose -f docker-compose-test.yml down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

## General for both branches

### Environment Variables

All environment variables are stored within the `.env` file and loaded with dotenv package.

**Never** commit your local settings to the Github repository!

### Unit Tests

To run the unit tests use the following commands:

```bash
python3 -m venv venv_unit
source venv_unit/bin/activate
pip install -r requirements.txt
pytest unit_test
```
