# Team Growth

## Project Topic: Community and E-Learning

## Motivation

- The project aims to provide an intuitive platform for aspiring African entrpreneurs who are participating in the [**African Impact Challenge**](https://www.africanimpact.ca/the-african-impact-challenge). We aim to provide an interactive platform that will help the community interact and learn from one another, as well as provide E-Learning facilities that will guide these aspirants towards building their ideas.

- Our platform will primarily be used for the pre-incubation and the incubation stages of the [African Impact Challenge](https://www.africanimpact.ca/the-african-impact-challenge).

- This project will significantly help the [African Impact Initiative](https://www.africanimpact.ca) to produce great innovation, helping the community grow and prosper. 

- Team Growth's primary goal is to contribute their skills to create a web-platform that is innovative, scalable, and intuitive. All published code will be peer reviewed, to ensure they meet quality expectations. Throughout the process, Team Growth hopes that all its members will collectively mature to become more experienced software engineers.

## Installation

One time install:
`pip3 install virtualenv`

Set up repo for developers after cloning
`cd project-growth`
`git flow init -d`
`git pull origin develop`
`git flow feature start feature_name`

Running the code:
`virtualenv -p python3 .`
`source bin/activate`
`pip install django`
`pip install django-crispy-forms` <- Used by forums
`pip install pillow` <- to prevent error No module named 'PIL'
`cd Growth`
`python3 manage.py runserver`

- Currently, we are planning to have a web application to design our project specifics.

Some of the technologies which are going to be used are:

***( NOTE: As our team consists of both MacOS as well as Windows Users, we will provide a link that contains the installation guides for both of these platforms below. )***

1. **NoSQL**

- Link: https://docs.oracle.com/en/database/other-databases/nosql-database/19.5/admin/installing-oracle-nosql-database.html

2. **Python**

- Link: https://www.python.org/downloads/

3. **Django**

- Windows: https://docs.djangoproject.com/en/1.8/howto/windows/
- Mac:     https://appdividend.com/2018/03/28/how-to-install-django-in-mac/

4. **React**
- We will use React staging create-react-app to deploy our project. 
- Plugins used: react-router-dom, antd, npm, yarn
- npm download page: https://www.npmjs.com/get-npm  
- yarn: npm install -g yarn
- antd download: write yarn add antd in cmd
- less: yarn add less less-loader
- Steps:
- 1. You can ignore antd, less right now
- 2. npm install -g create-react-app
- 3. clone the project
- 4. cd ./admin_client
- 5. npm start
- 6. visit localhost:3000

- Windows: https://www.liquidweb.com/kb/install-react-js-windows/
- Mac:     https://www.zeolearn.com/magazine/setup-react-mac

4. **Pillow**
- Use "pip install pillow" to install 

## Contribution

- Do you use git flow? ***YES***
- What do you name your branches? ***Master branch, Develop branch (will be updated as we progress through the sprints)***
- Do you use github issues or another ticketing website? ***Github issues will be used***
- Do you use pull requests? ***Will be planning to use pull requests as we progress through the sprints***




