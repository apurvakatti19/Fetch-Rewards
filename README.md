# Fetch Rewards Back-end Take home assignment

# Requirements
* python3
* Packages : Flask, Numpy

# Install Requirements
```
bash
cd Fetch_Rewards
make package
```

# Assumptions
* add_points REST endpoint accept parameters as a json constisting of payerName, points and transactionDate

# Run the app
```
bash
cd Fetch_Rewards
make app
```

# Run the tests
```
bash
cd Fetch_Rewards
make test
```

# REST API

The REST API to the app is described below.

## Add points to the User account

### Request

`POST /add_points/`

    curl -i -H 'Accept: application/json''payerName='DANNON'&'points'=300'&'transactionDate'="10/31 10AM' http://localhost:5000/add_points/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json


## Deduct points from the User account

### Request

`DELETE /delete_points/`

    curl -i -H 'Accept: application/json''points_to_deduct'=5000 http://localhost:5000/delete_points/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    [["DANNON",-100,"now"],["UNILEVER",-200,"now"],["MILLER COORS",-4700,"now"]]

`GET /balance/`

    curl -i -H 'Accept: application/json' http://localhost:5000/delete_points/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {"DANNON":1000,"MILLER COORS":5300,"UNILEVER":0}

# Makefile

| **Options**         | **Description**                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------ |
| `app`             | Starts the application at default port 5000                                     |
| `test`            | Runs the Flask End-to End API tests using pytest with coverage                                                   |
|  `packages`       | Installs the necessary packages to run and test this application                  |