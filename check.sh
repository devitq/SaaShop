#!/bin/bash

GREEN='\033[1;32m'
NC='\033[0m'

sort-requirements requirements/dev.txt
sort-requirements requirements/prod.txt
sort-requirements requirements/test.txt
sort-requirements requirements/lints.txt
printf "${GREEN}Requirements sorted${NC}\n"

cd saashop

black .
flake8 .
printf "${GREEN}Linters runned${NC}\n"

python manage.py makemigrations --check
python manage.py test
printf "${GREEN}Tests runned${NC}\n"
