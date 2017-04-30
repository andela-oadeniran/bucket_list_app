[![Build Status](https://travis-ci.org/andela-oadeniran/bucket_list_api.svg?branch=develop)](https://travis-ci.org/andela-oadeniran/bucket_list_api)
[![Coverage Status](https://coveralls.io/repos/github/andela-oadeniran/bucket_list_api/badge.svg?branch=develop)](https://coveralls.io/github/andela-oadeniran/bucket_list_api?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-oadeniran/BucketListApi/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-oadeniran/BucketListApi/?branch=develop)

## Bucket List API

### Table of Content
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [API Resource Endpoints](#api-resource-endpoints)
4. [Usage](#usage)
5. [Other Features](#other-features)
6. [Running Tests](#running-tests)
7. [Project Demo](#project-demo)
8. [Author](#author)
9. [LICENSE](#license)
10. [FINAL WORDS](#final-words)

### <a name="introduction"></a>Introduction
A little background. Everybody has those things they plan to do before a reference point in their life. That is why you make a Bucket List. The BucketListApi can be easily integrated to your application to help serve this end. This is an Andela idea/project to help pre-entry level developers hone their programming (in this case python) skills.

### <a name="installation"></a>Installation
1. Install system requirements python3.6, virtualenv and virtualenvwrapper.
2. Clone/Download the repo `$ git clone git@github.com:andela-oadeniran/bucket_list_api.git`.
3. Navigate to the project folder root.
4. Create and activate a virtual environment. `$ mkvirtualenv bucketenv --python=[path/to/python3]`
5. Install project dependencies with  `$ pip install -r requirements.txt`
6. Run the migration script to setup database:
    * Create migrations by running `$ python manage.py db migrate`.
    * Apply migrations with `$ python manage.py db upgrade`.
7. Run the server using `$ python server.py`.

### <a name="api-resource-endpoints"></a>API Resource Endpoints
| EndPoint                             | Functionality                 | Public Access       |
| ------------------------------------ | ----------------------------- | ------ |
| POST /auth/register                  | Register a user               | TRUE   |
| POST /auth/login                     | Logs a user in                | TRUE   |
| POST /bucketlists/                   | Create a new bucket list      | FALSE  |
| GET /bucketlists/                    | List all created bucket lists | FALSE  |
| GET /bucketlists/id                  | Get single bucket list        | FALSE  |
| PUT /bucketlists/id                  | Update a bucket list          | FALSE  |
| DELETE /bucketlists/id               | Delete a bucket list          | FALSE  |
| POST /bucketlists/id                 | Create a new item bucket list | FALSE  |
| PUT /bucketlists/id/items/item_id    | Update a bucket list item     | FALSE  |
| DELETE /bucketlists/id/items/item_id | Delete an item in bucket list | FALSE  |

### <a name="usage"></a>Usage
Running the Application: By Default the project runs on the Development config
run on a different config by export to the environment variable example `export BUCKETLIST_SETTINGS=[/path/to/config/class]`
The app runs on port 5000 by default to run on a different port example 'export PORT=5555'
1. Register a user.
    > CREATE A USER /api/v1/auth/register
    ```
    Request Example
        curl -i -X POST -d "username=miguel&password=anderson" http://localhost:5000/api/v1/auth/register
    ```
    ```
    Response
        HTTP/1.0 201 CREATED
        Content-Type: application/json
        Content-Length: 33
        Server: Werkzeug/0.12.1 Python/3.6.0
        Date: Sun, 23 Apr 2017 18:18:33 GMT
        "Hello your username is Miguel "
    ```

2. Login a User:
    > GET TOKEN FOR A REGISTERED USER /api/v1/login
    ```
    Request
        curl -i -X POST -d "username=miguel&password=anderson" http://localhost:5000/api/v1/auth/login
    ```
    >
    ```
    Response
        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 142
        Server: Werkzeug/0.12.1 Python/3.6.0
        Date: Sun, 23 Apr 2017 19:43:25 GMT
        {
            "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
        }
    ```
3. BucketList Api Endpoint
   > CREATE A NEW BUCKETLIST /api/v1/bucketlists
    ```    
     Request
         curl -i -X POST -d "name=Before I am 50" http://127.0.0.1:5000/api/v1/bucketlists/ -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
    ```
    ```
    Response
        HTTP/1.0 201 CREATED
        Content-Type: application/json
        Content-Length: 175
        Server: Werkzeug/0.12.1 Python/3.6.0
        Date: Sun, 23 Apr 2017 20:14:28 GMT
        {
            "created_by": "3",
            "date_created": "2017-04-23 20:14:28",
            "date_modified": "2017-04-23 20:14:28",
            "id": "5",
            "items": [],
            "name": "Before I Am 50"
        }
    ```
    > READ THE BUCKETLIST /api/v1/bucketlists/<bucketlist_id>
    ```
    Request
        curl -X GET http://127.0.0.1:5000/api/v1/bucketlists/ -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
    ```
    ```
    Response
        {
        "data": {
                "Bucketlist1": {
                    "created_by": "3",
                    "date_created": "2017-04-23 20:14:28",
                    "date_modified": "2017-04-23 20:14:28",
                    "id": "5",
                    "items": [],
                    "name": "Before I Am 50"
                }
            },
            "next_page": null,
            "pages": 1,
            "previous_page": null
        }
    ```
    > UPDATE THE BUCKETLIST /api/v1/bucketlists/<bucketlist_id>/items/<item_id>
    ```
    Request Example
     curl -i -X PUT -d "name=Before I am 60" http://127.0.0.1:5000/api/v1/bucketlists/5 -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU
    ```
    ```
    Response
        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 175
        Server: Werkzeug/0.12.1 Python/3.6.0
        Date: Sun, 23 Apr 2017 21:53:28 GMT
        {
            "created_by": "3",
            "date_created": "2017-04-23 20:14:28",
            "date_modified": "2017-04-23 21:53:28",
            "id": "5",
            "items": [],
            "name": "Before I Am 60"
        }
    ```
4. Bucketlist item api
> CREATE A NEW BUCKETLIST ITEM /api/v1/bucketlists/<bucketlist_id>/items
```
Request
    curl -i -X POST -d"name=travel round the world" http://127.0.0.1:5000/api/v1/bucketlists/5/items -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
```
```
Response
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 164
    Server: Werkzeug/0.12.1 Python/3.6.0
    Date: Sun, 23 Apr 2017 21:05:52 GMT
    {
        "date_created": "2017-04-23 21:05:52",
        "date_modified": "2017-04-23 21:05:52",
        "done": "False",
        "id": "8",
        "name": "Travel Round The World"
    }
```
> UPDATE A BUCKETLIST ITEM /api/v1/bucketlists/<bucketlist_id>/item/<item_id>
```
Request example
    curl -i -X PUT -d"name=travel round the world and back" http://127.0.0.1:5000/api/v1/bucketlists/5/items/8 -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
```
```
Response
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 173
    Server: Werkzeug/0.12.1 Python/3.6.0
    Date: Sun, 23 Apr 2017 21:41:32 GMT
    {
        "date_created": "2017-04-23 21:05:52",
        "date_modified": "2017-04-23 21:41:32",
        "done": "False",
        "id": "8",
        "name": "Travel Round The World And Back"
    }
```
> DELETE A BUCKETLIST ITEM /api/v1/bucketlists/<bucketlist_id>/item/<item_id>
```
Request Example
    curl -i -X DELETE http://127.0.0.1:5000/api/v1/bucketlists/5/items/8 -H "Token:eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5Mjk3NjYwNSwiZXhwIjoxNDkzMDYzMDA1fQ.eyJpZCI6M30.zO0EmrV-LgoGiN2cUHwjbtEQnsdG9305VGxyfp-5uPU"
```
```
Response
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 28
    Server: Werkzeug/0.12.1 Python/3.6.0
    Date: Sun, 23 Apr 2017 21:45:12 GMT
    "Successfully deleted Item"
```


### <a name="running-tests"></a>Running Tests
1. Navigate to the project directory.
2. Run `py.test --cov-report term-missing --cov bucketlist_api` to run test and check coverage.

### <a name="project-demo"></a>Project Demo
Click [here](https://www.youtube.com/watch?v=9wzH5_iwY5o) to view a short project demo

## <a name="author"></a>Author
Oladipupo Adeniran

## <a name="license"></a>License
<a href='https://github.com/andela-oadeniran/bucketlist-api/blob/develop/LICENSE'>MIT </a>

## <a name="final-words"></a>Final Words
Appreciation goes to
1. All the Folks at Andela because we are EPIC and awesome like that
2. Special shout out goes to Njira Perci you can follow her [@njirap](). She is an Amazing Human Being and literally propelled the discipline and doggedness to accomplish this task.
3. "pygo" team members at Andela because we would do great things together.
