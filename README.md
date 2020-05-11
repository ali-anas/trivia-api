# Full Stack API Project

## Full Stack Trivia

Trivia is a simple question and answer quiz game.It provides you following features - 

1) Display questions - both all questions and by category. Questions shows the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Motivation

The main motivation of the project is learn how to design, develop and document the RESTful APIs 
Completing this trivia app give me the ability to structure plan, implement, and test an API which are consumed by the frontend of the application, and can also be consumed by other other authorised resources.

Each module of backend code is implemented by following 'Test-Driven-Development'. 
Each endpoint is unit-tested to check the expected behaviour and error handling for the different types of requests.

Here is development strategy i followed -
1. Write and formulate test (keeping in my the end goal of each module and associated errors that could be encountered)
2. Fail test
3. Write code to pass test and reach end goal 
4. Pass test (if yes go to step 5 else go to step 3)
5. Refactor


## Project structure

```
 maindirectory
  ├── README.md
  ├── backend **Contains API and test suit.**
  |   |
  │   ├── README.md **Contains backend server setup and API documentation**
  |   |
  │   ├── config.py **Contains information for database connection**
  |   |
  │   ├── models.py
  |   |
  │   ├── flaskr
  │   │   └── __init__.py **App creation & API endpoints.**
  |   |
  │   ├── requirements.txt **The dependencies to be installed with "pip3 install -r requirements.txt"**
  |   |
  │   └── test_flaskr.py **22 unittests to check expected behaviour from API**
  |   |
  │   └── trivia.psql **database dumb, restore with "psql trivia < trivia.psql"**
  |
  └── frontend **start frontend with "npm start"**
      |
      ├── README.md **Contains Frontend Setup**
      |
      └── src
          └── components **Contains React Components**
```


## Tasks


1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)
 

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 


[View the README.md within ./frontend for more details.](./frontend/README.md)
