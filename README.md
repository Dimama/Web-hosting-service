# Web-hosting-service
Training project: Simple web hosting portal using microservices on Flask

[![Build Status](https://travis-ci.org/Dimama/Web-hosting-service.svg?branch=develop)](https://travis-ci.org/Dimama/Web-hosting-service)

[![Coverage Status](https://coveralls.io/repos/github/Dimama/Web-hosting-service/badge.svg?branch=develop)](https://coveralls.io/github/Dimama/Web-hosting-service?branch=develop)

## Setup and run
1. Make virtual environment and activate
2. `pip install -r requirements.txt`
3. In users_service/application/const.py set `DB_URI`
4. run `python manage.py setup_db` in users_service/
5. run `python manage.py run` in users_service/
6. repeat `3-5` steps for servers_service and rent_service
6. run `python manage.py run` in gateway_service/

## Gateway API
root URI = `http://localhost:8080`

| URI | METHOD | Description |Body parameters | Parameters | Status codes|
| :---:              | :---:|    :---:      |:---:      | :---:      | :---: |
| /server?page={page}&size={size}| GET | Get servers with pagination| - | page, size(optional)| 200, 400, 404 |
| /server/{id}| GET | Get info about server | - | id | 200, 400, 404 |
| /user/{id}/rent| POST | Create rent for user| server_id, duration| id | 201, 400, 404, 422 |
| /user/{id}/rent| GET | Get rents for user |- | id | 200, 400, 404 |
| /user/{user_id}/rent/{rent_id}| DELETE | Delete user's rent | - | user_id, rent_id| 204, 400, 404 |
