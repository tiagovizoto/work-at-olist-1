## Endpoints

__ /v1/call/ __

- `POST /v1/call/`

  _201_

  `http POST http://127.0.0.1:8000/v1/call/ timestamp='2018-10-14T06:15:00Z' source=00999994545 destination=00999997878 type='start' call_id=84`

  Response:
  ```
  {
    "call_id": 666,
    "destination": "00999997878",
    "source": "00999994545",
    "timestamp": "2018-10-14T06:15:00Z"
  }
  ```

  `http POST http://127.0.0.1:8000/v1/call/ timestamp='2018-10-14T10:21:00Z' type='end'  call_id=666`

  Response:
  ```
  {
      "call_id": 666,
      "destination": "00999997878",
      "source": "00999994545",
      "timestamp": "2018-10-14T06:15:00Z"
  }
  ```

  _Examples 400_

  ```
    {
      "call_id": [
          "call start with this call id already exists."
      ]
    }

    [
      "No exist the call_id 8595 in start call records"
    ]

  ```
__ /v1/bill/fee/minute/ __

- `GET /v1/bill/fee/minute/`

  _200_
  ```
  HTTP 200 OK
  Allow: GET, POST, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  [
      {
          "id": 39,
          "price": "0.09",
          "start": "06:00:00",
          "end": "22:00:00"
      },
      {
          "id": 40,
          "price": "0.01",
          "start": "22:30:00",
          "end": "23:00:00"
      }
  ]
  ```

- `POST /v1/bill/fee/minute/`

  _201_
  ```
  http POST http://127.0.0.1:8000/v1/bill/fee/minute/ price=0.01 start=01:00:00 end=12:00:00

  HTTP/1.1 201 Created
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 60
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 18:37:46 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  {
      "end": "12:00:00",
      "id": 41,
      "price": "0.01",
      "start": "01:00:00"
  }

  ```

- `GET /v1/bill/fee/minute/<id>/`

  _200_
  ```
  HTTP 200 OK
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "id": 39,
      "price": "0.09",
      "start": "06:00:00",
      "end": "22:00:00"
  }
  ```

  _404_
  ```
  HTTP 404 Not Found
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "detail": "Not found."
  }
  ```

- `DELETE /v1/bill/fee/minute/<id>/`

  _204_
  ```
  HTTP/1.1 204 No Content
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Length: 0
  Date: Mon, 25 Feb 2019 10:31:28 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN
  ```
  _400 (301)_
  ```
  HTTP/1.1 301 Moved Permanently
  Content-Length: 0
  Content-Type: text/html; charset=utf-8
  Date: Mon, 25 Feb 2019 10:30:54 GMT
  Location: /v1/bill/fee/minute/39/
  ```


__ /v1/bill/fee/fixed/ __

- `GET /v1/bill/fee/fixed/`

  _200_
  ```
  HTTP 200 OK
  Allow: GET, POST, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  [
      {
          "id": 1,
          "price": "0.36",
          "start": "00:00:00",
          "end": "23:59:00"
      }
  ]
  ```

- `POST /v1/bill/fee/fixed/`

  _201_
  ```
  http POST http://127.0.0.1:8000/v1/bill/fee/fixed/ price=0.39 start=00:00:00 end=23:59:59

  HTTP/1.1 201 Created
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 59
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 18:42:12 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  {
      "end": "23:59:59",
      "id": 2,
      "price": "0.39",
      "start": "00:00:00"
  }

  ```
  _400_
  ```
  HTTP/1.1 400 Bad Request
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 28
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 18:41:52 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  [
      "Exist conflicts of times"
  ]
  ```

- `GET /v1/bill/fee/fixed/<id>/`

  _200_
  ```
  HTTP 200 OK
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "id": 1,
      "price": "0.36",
      "start": "00:00:00",
      "end": "23:59:00"
  }
  ```
  _404_
  ```
  HTTP 404 Not Found
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "detail": "Not found."
  }
  ```

- `DELETE /v1/bill/fee/fixed/<id>/`

  _204_
  ```
  HTTP/1.1 204 No Content
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Length: 0
  Date: Mon, 25 Feb 2019 10:31:28 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN
  ```
  _400 (301)_
  ```
  HTTP/1.1 301 Moved Permanently
  Content-Length: 0
  Content-Type: text/html; charset=utf-8
  Date: Mon, 25 Feb 2019 10:30:54 GMT
  Location: /v1/bill/fee/minute/39/

  ```


__ /v1/bill/ __

- `GET /v1/bill/<number phone>/`

  _200_
  ```
  HTTP/1.1 200 OK
  Allow: GET, HEAD, OPTIONS
  Content-Length: 697
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 10:38:59 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  {
      "calls_count": 2,
      "price": 67.14,
      "records": [
          [
              {
                  "duration": "00:00:00",
                  "end_call": {
                      "call_id": 100,
                      "timestamp": "2019-01-14T10:21:00Z"
                  },
                  "fixed_fee": {
                      "end": "23:59:00",
                      "id": 1,
                      "price": "0.36",
                      "start": "00:00:00"
                  },
                  "id": 7,
                  "price": "22.50",
                  "start_call": {
                      "call_id": 100,
                      "destination": "41992782762",
                      "source": "4197020434",
                      "timestamp": "2019-01-14T06:15:00Z"
                  }
              },
              {
                  "duration": "00:00:00",
                  "end_call": {
                      "call_id": 101,
                      "timestamp": "2019-01-20T10:21:00Z"
                  },
                  "fixed_fee": {
                      "end": "23:59:00",
                      "id": 1,
                      "price": "0.36",
                      "start": "00:00:00"
                  },
                  "id": 8,
                  "price": "44.64",
                  "start_call": {
                      "call_id": 101,
                      "destination": "41992782762",
                      "source": "4197020434",
                      "timestamp": "2019-01-20T06:15:00Z"
                  }
              }
          ]
      ]
  }

  ```
  _404_
  ```
  HTTP 404 Not Found
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "detail": "Not found."
  }
  ```

- `GET /v1/bill/<number phone>/<year>/`

  _200_
  ```
  HTTP/1.1 200 OK
  Allow: GET, HEAD, OPTIONS
  Content-Length: 4036
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 10:37:37 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  [
      {
          "count_records": 0,
          "month": 1,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 2,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 3,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 4,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 5,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 6,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 7,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 8,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 0,
          "month": 9,
          "price": 0.0,
          "records": [
              []
          ]
      },
      {
          "count_records": 7,
          "month": 10,
          "price": 466.02,
          "records": [
              [
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 33,
                          "timestamp": "2018-10-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 1,
                      "price": "22.14",
                      "start_call": {
                          "call_id": 33,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 30,
                          "timestamp": "2018-10-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 2,
                      "price": "22.14",
                      "start_call": {
                          "call_id": 30,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 85,
                          "timestamp": "2018-10-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 3,
                      "price": "22.14",
                      "start_call": {
                          "call_id": 85,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 84,
                          "timestamp": "2018-10-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 4,
                      "price": "22.50",
                      "start_call": {
                          "call_id": 84,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 81,
                          "timestamp": "2018-10-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 5,
                      "price": "22.14",
                      "start_call": {
                          "call_id": 81,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 106,
                          "timestamp": "2018-10-30T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 13,
                      "price": "155.34",
                      "start_call": {
                          "call_id": 106,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-30T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 108,
                          "timestamp": "2018-10-17T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 15,
                      "price": "199.62",
                      "start_call": {
                          "call_id": 108,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-10-17T06:15:00Z"
                      }
                  }
              ]
          ]
      },
      {
          "count_records": 1,
          "month": 11,
          "price": 687.78,
          "records": [
              [
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 109,
                          "timestamp": "2018-11-01T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 16,
                      "price": "221.76",
                      "start_call": {
                          "call_id": 109,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-11-01T06:15:00Z"
                      }
                  }
              ]
          ]
      },
      {
          "count_records": 2,
          "month": 12,
          "price": 909.8999999999999,
          "records": [
              [
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 103,
                          "timestamp": "2018-12-14T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 10,
                      "price": "88.92",
                      "start_call": {
                          "call_id": 103,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-12-14T06:15:00Z"
                      }
                  },
                  {
                      "duration": "00:00:00",
                      "end_call": {
                          "call_id": 105,
                          "timestamp": "2018-12-18T10:21:00Z"
                      },
                      "fixed_fee": {
                          "end": "23:59:00",
                          "id": 1,
                          "price": "0.36",
                          "start": "00:00:00"
                      },
                      "id": 12,
                      "price": "133.20",
                      "start_call": {
                          "call_id": 105,
                          "destination": "41992782762",
                          "source": "4197020434",
                          "timestamp": "2018-12-18T06:15:00Z"
                      }
                  }
              ]
          ]
      }
  ]

  ```
  _404_
  ```
  HTTP 404 Not Found
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "detail": "Not found."
  }
  ```

- `GET /v1/bill/<number phone>/<year>/<month>/`

  _200_
  ```
  HTTP/1.1 200 OK
  Allow: GET, HEAD, OPTIONS
  Content-Length: 2312
  Content-Type: application/json
  Date: Mon, 25 Feb 2019 10:34:55 GMT
  Server: WSGIServer/0.2 CPython/3.7.2
  Vary: Accept, Cookie
  X-Frame-Options: SAMEORIGIN

  {
      "calls_count": 3,
      "price": 466.02,
      "records": [
          [
              {
                  "duration": "00:00:00",
                  "end_call": {
                      "call_id": 30,
                      "timestamp": "2018-10-14T10:21:00Z"
                  },
                  "fixed_fee": {
                      "end": "23:59:00",
                      "id": 1,
                      "price": "0.36",
                      "start": "00:00:00"
                  },
                  "id": 2,
                  "price": "22.14",
                  "start_call": {
                      "call_id": 30,
                      "destination": "41992782762",
                      "source": "4197020434",
                      "timestamp": "2018-10-14T06:15:00Z"
                  }
              },
              {
                  "duration": "00:00:00",
                  "end_call": {
                      "call_id": 85,
                      "timestamp": "2018-10-14T10:21:00Z"
                  },
                  "fixed_fee": {
                      "end": "23:59:00",
                      "id": 1,
                      "price": "0.36",
                      "start": "00:00:00"
                  },
                  "id": 3,
                  "price": "22.14",
                  "start_call": {
                      "call_id": 85,
                      "destination": "41992782762",
                      "source": "4197020434",
                      "timestamp": "2018-10-14T06:15:00Z"
                  }
              },
              {
                  "duration": "00:00:00",
                  "end_call": {
                      "call_id": 81,
                      "timestamp": "2018-10-14T10:21:00Z"
                  },
                  "fixed_fee": {
                      "end": "23:59:00",
                      "id": 1,
                      "price": "0.36",
                      "start": "00:00:00"
                  },
                  "id": 5,
                  "price": "22.14",
                  "start_call": {
                      "call_id": 81,
                      "destination": "41992782762",
                      "source": "4197020434",
                      "timestamp": "2018-10-14T06:15:00Z"
                  }
              }
          ]
      ]
  }
  ```
  _404_
  ```
  HTTP 404 Not Found
  Allow: GET, DELETE, HEAD, OPTIONS
  Content-Type: application/json
  Vary: Accept

  {
      "detail": "Not found."
  }
  ```


