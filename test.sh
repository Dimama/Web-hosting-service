#!/bin/bash

# run with activate virtual environment in root directory of project

mkdir coverage_dir
cd gateway_service/
coverage run --source="application/resources/" -m unittest discover -s test/
cp .coverage ../coverage_dir/.coverage.gateway

cd ../users_service/
coverage run  --source="application/resources/" --omit="application/resources/__init__.py" -m unittest discover -s test/
cp .coverage ../coverage_dir/.coverage.users

cd ../coverage_dir/
coverage combine
coverage report -m
