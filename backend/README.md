# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Task-Completed

1. Used Flask-CORS to enable cross-domain requests and set response headers. 
2. Created an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, current category, categories. 
3. Created an endpoint to handle GET requests for all available categories. 
4. Created an endpoint to DELETE question using a question ID. 
5. Created an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Created a POST endpoint to get questions based on category. 
7. Created a POST endpoint to get questions based on a search term. It returns any questions for whom the search term is a substring of the question. 
8. Created a POST endpoint to get questions to play the quiz. This endpoint takes category and previous questions parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Created error handlers for all expected errors including 400, 404, 422 and 500.
10. Created a POST endpoint to which require the type of category to be create to create new category.
11. Created a DELETE endpoint to delete a category from the list of categories.  


## API Documentation
If you want to play a quiz based on several categories or want to make a new quiz for your folks, Trivia is your online solution.
### Overview
The Trivia API is organized around **REST**.This API has predictable resource-oriented URLs, accepts form-encoded request bodies, return **JSON-encoded** responses, and uses standard HTTP response codes, authentication, and verbs.

Trivia API helps you create, play quiz based on category of questions.
- It lets you create a new question, or new questions category.
- It also helps you delete an existing question, or an existing category of questions.

In this documentation you will find existing endpoints, and related methods that are helping the API to serve the requests.

### Base URL
Since this API is not hosted in any specific domain, it can only be accessed when `flask` is running locally.To make requests to the API via `curl` you need to use the default domain on which the flask server is running locally.

```http://127.0.0.1:5000/```


### Errors
Trivia uses conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the `2xx` range indicate success. Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted). Codes in the `5xx` range indicate an error with Trivia servers (these are rare).
Specific error **status_code** and error **message** is provided in `JSON` format along with **success** key having value `false`

Sample error response - 

error response for `status_code: 400`. 
```
{
      'success':False,
      'error': 400,
      'message': 'bad request'
}, 400
```

- **2.xx**
  - `status_code`: **200**, `message`: **'success'**
    indicates success
- **4.xx** 
  - `status_code`: **400**, `message`: **'bad request'**
    indicates that the server cannot or will not process the request due to something that is perceived to be a client error occured due to inapproriate or insufficient details.
  - `status_code`: **404**, `message`: **'resource not found'**
    indiactes that requested resource is not found.
  - `status_code`: **405**, `message`: **'method not allowed'**
    indicates that the request method is known by the server but is not supported by the target resource.
  - `status_code`: **422**, `message`: **'unprocessable'**
    indicates that the server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.
- **5.xx**
  - `status_code`: **500**, `message`: **'internal server error'**
    indicates that server cannot process the request for an unknown reason





### Endpoints Available
Here is a an overview of major resources that are served with.
```  
    ---------------------------------------------------------------------------------------------
      Resource Endpoint           GET          POST         DELETE          
    ---------------------------------------------------------------------------------------------
      /questions            available         available       available
      /categories             available         available       available
      /quizzes                   -            available         -        
```



### Resource endpoint library

1. /questions
   1. [GET /questions](#get-questions)
   2. [POST /questions](#post-questions)
   3. [DELETE /questions/<question_id>](#delete-questions)
2. /quizzes
   1. [POST /quizzes](#post-quizzes)
3. /categories
   1. [GET /categories](#get-categories)
   2. [GET /categories/<category_id>/questions](#get-categories-questions)
   3. [POST /categories](#post-categories)
   4. [DELETE /categories](#delete-categories)

# <a name="get-questions"></a>
### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Request Arguments: 
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. List of dict of questions with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **integer** `category`
      - **integer** `difficulty`
  2. **list** `categories`
  3. **list** `current_category`
  4. **integer** `total_questions`
  5. **boolean** `success`

#### Example response
```js
{
"categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"current_category": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
}

```
#### Errors
If you try fetch a page which does not have any questions, you will encounter an error which looks like this:

```bash
curl -X GET http://127.0.0.1:5000/questions?page=15211521
```

will return

```js
{
  "success": false,
    "error": 404,
    "message": "resource not found"  
}
```

# <a name="post-questions"></a>
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "This a test question?", "category" : 3 , "answer" : "Yes", "difficulty" : 1 }' -H 'Content-Type: application/json'
```

- Searches database for questions with a search term, if provided. Otherwise,
it will insert a new question into the database.
- Request Arguments: **None**
- Request Headers :
  - if you want to **search** (_application/json_)
       1. **string** `searchTerm` (*required)
  - if you want to **insert** (_application/json_) 
       1. **string** `question` (*required)
       2. **string** `answer` (*required)
       3. **integer** `category` (*required)
       4. **integer** `difficulty` (*required)
- Returns: 
  - if you searched:
    1. List of dict of `questions` which match the `searchTerm` with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **integer** `category`
        - **integer** `difficulty`
    2. List of dict of ``current_category`` with following fields:
        - **integer** `id`
        - **string** `type`
    3. **integer** `total_questions`
    4. **boolean** `success`
  - if you inserted:
    1. List of dict of all `questions` with following fields:
        - **integer** `id` 
        - **string** `question`
        - **string** `answer`
        - **integer** `category`
        - **integer** `difficulty`
    2. **integer** `total_questions`
    3. **integer** `created`  id of inserted question
    4. **boolean** `success`

#### Example response
Search Questions
```js
{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },

   [...] // all current categories

  ],
  "questions": [
    {
      "answer": "Yes",
      "category": 3,
      "difficulty": 1,
      "id": 24,
      "question": "This is a test question?"
    }

    [...] // + all questions which contain the search term in its question
  
  ],
  "success": true,
  "total_questions": 20
}

```
Create Question
```js
{
  "created": 26, // id of created question
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
   
   [...] // + all questions in database

  ],
  "success": true,
  "total_questions": 21
}

```


#### Errors
**Search related**

If you try to search with a searchTerm which does not exist in any `question` , it will response with an `404` error code:

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```

will return

```js
{
  "success": false,
    "error": 404,
    "message": "resource not found"
}
```
**Insert related**

If you try to insert a new `question`, but forget to provide a required field, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "a question without provided any answer possible?", "category" : 1, "difficulty" : 1 }' -H 'Content-Type: application/json'
```

will return

```js
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```
# <a name="delete-questions"></a>
### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on given id
- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id from deleted question.
    - **boolean** `success`


#### Example response
when tries to delete a question which exist and have an id `10`
```js
{
    "deleted": 10,
    "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `404` error:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```
will return
```js
{
  "success": false
    "error": 404,
    "message": "resource not found"
  
}
```

# <a name="post-quizzes"></a>
### 4. POST /quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 3], "quiz_category" : {"type" : "Science", "id" : 1}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by mantaining a list of already asked questions and a category to ask question from, in random order.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` with **integer** ids of already asked questions
     1. **dict** `quiz_category` with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **integer** `category`
      - **integer** `difficulty`
  2. **boolean** `success`

#### Example response
```js
{
  "question": {
    "answer": "Yes",
    "category": 3,
    "difficulty": 1,
    "id": 24,
    "question": "This is a test question?"
  },
  "success": true
}

```
### Errors

If you try to play the quiz game without a valid JSON body, it will response with an  `400` error.

```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : []} ' -H 'Content-Type: application/json'
```
will return
```js
{
  "success": false,
    "error": 400,
    "message": "bad request"
}

```
# <a name="get-categories"></a>
### 5. GET /categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a list of all `categories` with its `type` as values.
- Request Arguments: **None**
- Request Headers : **None**
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example response
```js
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```
### Errors

Endpoint does not raise any specific errors until there are questions available beacuese questions will have some certain category associated with them.

# <a name="get-categories-questions"></a>
### 6. GET /categories/<category_id>/questions

Get all questions from a specific `category`.
suppose `2` is a valid category then -
```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
- Fetches all `questions` (paginated) from one specific category with id `2`.
- Request Arguments:
  - **integer** `category_id` (*required)
  - **integer** `page` (optinal, 10 questions per Page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. **integer** `current_category` id of accessed category
  2. List of dict of all questions with following fields:
     - **integer** `id` 
     - **string** `question`
     - **string** `answer`
     - **integer** `category`
     - **integer** `difficulty`
  3. **integer** `total_questions`
  4. **boolean** `success`

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### Errors
This endpoint can give `404` error. For example, if you ask for questions of a category that does not actually have questions currently becauese we are not mapping relation between number of questions the category is related to.So there can be a case that we either deleted all questions related to particular category or just inserted a new category.Such cases will throw error `404` 
```bash
curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1
```
will return
```js
{
  "success": false,
    "error": 404,
    "message": "resource not found"
  
}
```
# <a name="post-categories"></a>
### 7. POST /categories

Create new category.
```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "type" : "Favourites"}' -H 'Content-Type: application/json'
```

- Inserts a new `category` to extend the game with questions from new category.
- Request Arguments: **None**
- Request Headers : (_application/json_) 
   1. **string** type (*required)
- Returns: 
  1. List of dict of all existing `categories` with following fields:
      - **integer** `id` 
      - **string** `type`
  2. **integer** `total_categories` number of all `categories`
  3. **integer** `created`  id of inserted `category`
  4. **boolean** `success`

#### Example response
```js
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    },
    {
      "id": 7,
      "type": "Favourites"
    }
  ],
  "created": 7,
  "success": true,
  "total_categories": 7
}
```


#### Errors

If you try to insert a new category without `type` field, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "name" : "Favourites"}' -H 'Content-Type: application/json'
```

will return

```js
{
  "success": false,
    "error": 400,
    "message": "bad request"
}
```
# <a name="delete-categories"></a>
### 8. DELETE /categories/<category_id>

Delete a Category suppose if there is a category with id 8
```bash
curl -X DELETE http://127.0.0.1:5000/categories/8
```
- Deletes specific `category` based on given id
- Request Arguments: 
  - **integer** `category_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id of deleted `category`.
    - **boolean** `success`


#### Example response
```js
{
  "deleted": 8,
  "success": true
}
```

### Errors

If you try to delete a `category` which does not exist, it will throw an `404` error:

```bash
curl -X DELETE http://127.0.0.1:5000/categories/100
```
will return
```js
{
  "success": false,
    "error": 404,
    "message": "resource not found"
}
```




## Testing
To run the tests, run
make sure you are at top level of backend directory and also make sure you working in virtual environment to work with term 'json'
otherwise running test can lead to such type of error:
```
TypeError: __init__() got an unexpected keyword argument 'json'
``` 
commands to run test :

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```