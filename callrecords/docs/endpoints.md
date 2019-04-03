# Endpoints

*The examples use [HTTPie](https://httpie.org/) for api requests*

- [Fees](#fees)
- [Calls Start and End](#calls)
- [Last Bill](#last)
- [Year and month bills](#month-and-year)
- [Year Bills](#year)


____
## Fees
The endpoint fees accept several periods, but must not overlap.

#### Minute
The charge applies to each completed 60 seconds cycle.

- ` POST /v1/bill/fee/minute/ `
    
> Example: `http POST http://127.0.0.1:8000/v1/bill/fee/minute/ price=0.09 start=06:00:00 end=22:00:00`

HTTP 201
```
{
    "end": "22:00:00",
    "id": 2,
    "price": "0.09",
    "start": "06:00:00"
}
```

- ` GET /v1/bill/fee/minute/`

> Example: `http http://127.0.0.1:8000/v1/bill/fee/minute/`

HTTP 200
```
List all minute fee
```

- ` GET /v1/bill/fee/minute/< id > `

> Example: `http http://127.0.0.1:8000/v1/bill/fee/minute/2/`

HTTP 200

```
{
    "end": "22:00:00",
    "id": 2,
    "price": "0.09",
    "start": "06:00:00"
}
```



- ``` DELETE /v1/bill/fee/minute/< id > ```
> Example: `http DELETE http://127.0.0.1:8000/v1/bill/fee/minute/2/`

HTTP 204


#### Fixed
Fixed charges that are used to pay for the cost of the connection.

- ``` POST /v1/bill/fee/fixed/ ```
> Example: `http POST http://127.0.0.1:8000/v1/bill/fee/fixed/ price=0.99 start=00:00:00 end=23:00:00`

HTTP 201
```
{
    "end": "23:00:00",
    "id": 2,
    "price": "0.99",
    "start": "00:00:00"
}
```


- ``` GET /v1/bill/fee/fixed/< id > ```
> Example: `http http://127.0.0.1:8000/v1/bill/fee/fixed/2/`

HTTP 200
```
{
    "end": "23:00:00",
    "id": 2,
    "price": "0.99",
    "start": "00:00:00"
}
```

- ` GET /v1/bill/fee/fixed/`

> Example: `http http://127.0.0.1:8000/v1/bill/fee/fixed/`

HTTP 200
```
List all fixed fee
```


- ``` DELETE /v1/bill/fee/fixed/< id > ```
> Example: `http DELETE http://127.0.0.1:8000/v1/bill/fee/fixed/2/`

HTTP 204

____
## Calls

#### Start
Creates a start of call records

- ` POST /v1/call/ `
> Example: `http POST http://127.0.0.1:8000/v1/call/ timestamp='2016-02-29T12:00:00Z' source:=99988526423 destination:=99997858585 type='start' id:=1`

HTTP 201
```
{
    "destination": 9933468278,
    "id": 1,
    "source": 99988526423,
    "timestamp": "2016-02-29T12:00:00Z"
}

```

#### End
Finishes the call

- ```POST /v1/call/ ```
> Example: `http POST http://127.0.0.1:8000/v1/call/ timestamp='2016-02-29T14:00:00Z' type='end'  id:=1`

HTTP 201
```
{
    "id": 1,
    "timestamp": "2016-02-29T14:00:00Z"
}
```
___
## Bills

#### Last 
Gets the last bill

- ```GET /v1/bill/< number phone >/ ```
> Example: `http http://127.0.0.1:8000/v1/bill/99888888888/`

HTTP 200
```
{
    "calls_count": 2,
    "price": 34.26,
    "records": [
        [
            {
                "call_end": {
                    "id": 91,
                    "timestamp": "2019-02-10T22:10:56Z"
                },
                "call_start": {
                    "destination": 9933468278,
                    "id": 91,
                    "source": 99888888888,
                    "timestamp": "2019-02-10T21:57:13Z"
                },
                "duration": "0d0h13m43s",
                "fixed_fee": {
                    "end": "23:59:59",
                    "id": 1,
                    "price": "0.39",
                    "start": "00:00:00"
                },
                "id": 18,
                "price": "0.57"
            },
            {
                "call_end": {
                    "id": 92,
                    "timestamp": "2019-02-10T12:10:56Z"
                },
                "call_start": {
                    "destination": 9933468278,
                    "id": 92,
                    "source": 99888888888,
                    "timestamp": "2019-02-10T05:57:13Z"
                },
                "duration": "0d6h13m43s",
                "fixed_fee": {
                    "end": "23:59:59",
                    "id": 1,
                    "price": "0.39",
                    "start": "00:00:00"
                },
                "id": 19,
                "price": "33.69"
            }
        ]
    ]
}

```

#### Month and Year
Gets the bill by year and month informed

- ```GET /v1/bill/< number phone >/< year >/< month >/ ```
> Example: `http http://127.0.0.1:8000/v1/bill/99888888888/2018/03/`

HTTP 200
```
{
    "calls_count": 1,
    "price": 86.97,
    "records": [
        [
            {
                "call_end": {
                    "id": 87,
                    "timestamp": "2018-03-01T22:10:56Z"
                },
                "call_start": {
                    "destination": 9933468278,
                    "id": 87,
                    "source": 99888888888,
                    "timestamp": "2018-02-28T21:57:13Z"
                },
                "duration": "1d0h13m43s",
                "fixed_fee": {
                    "end": "23:59:59",
                    "id": 1,
                    "price": "0.39",
                    "start": "00:00:00"
                },
                "id": 16,
                "price": "86.97"
            }
        ]
    ]
}

```

#### Year
Gets the all bills of year informed

- ```GET /v1/bill/< number phone >/< year >/ ```
> Example: `http http://127.0.0.1:8000/v1/bill/99888888888/2018/`

HTTP 200
```
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
        "count_records": 1,
        "month": 3,
        "price": 86.97,
        "records": [
            [
                {
                    "call_end": {
                        "id": 87,
                        "timestamp": "2018-03-01T22:10:56Z"
                    },
                    "call_start": {
                        "destination": 9933468278,
                        "id": 87,
                        "source": 99888888888,
                        "timestamp": "2018-02-28T21:57:13Z"
                    },
                    "duration": "1d0h13m43s",
                    "fixed_fee": {
                        "end": "23:59:59",
                        "id": 1,
                        "price": "0.39",
                        "start": "00:00:00"
                    },
                    "id": 16,
                    "price": "86.97"
                }
            ]
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
        "count_records": 0,
        "month": 10,
        "price": 0.0,
        "records": [
            []
        ]
    },
    {
        "count_records": 0,
        "month": 11,
        "price": 0.0,
        "records": [
            []
        ]
    },
    {
        "count_records": 0,
        "month": 12,
        "price": 0.0,
        "records": [
            []
        ]
    }
]


```
____