Serverless DDNS
===============

Serverless DDNS management REST API framework created via [Chalice](https://github.com/aws/chalice).

Function
--------

* Manage private DDNS framework with Amazon Route 53.
* Create, update and delete DNS records via REST API with Amazon API Gateway.

Usage
-----

Manipulate with REST API.

### GET hostzone

```bash
$ curl -s -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XGET http://your-url/hostzone
{
  "status": "exist",
  "record_sets": [
    {
      "records": ["192.168.11.1"],
      "type": "A",
      "ttl": 300
    }
  ]
}
```

### GET hostzone/record

```bash
$ curl -s -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XGET http://your-url/hostzone/record
{
  "status": "exist",
  "detail": {
    "records": ["192.168.11.1"],
    "type": "A",
    "ttl": 300
  }
}
```

### PUT hostzone/record

```bash
$ cat record.json
{
  "records": ["192.168.11.1"],
  "type": "A",
  "ttl": 300
}

# Response status 200 OK
$ curl -s -H "Content-type: application/json" -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XPUT http://your-url/hostzone/record -d @record.json
{
  "status": "created",
  "detail": {
    "records": ["192.168.11.1"],
    "type": "A",
    "ttl": 300
  }
}

# if you don't specify request body, IP address will be set up with your source global IP.
$ curl -s -H "Content-type: application/json" -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XPUT http://your-url/hostzone/record
{
  "status": "created",
  "detail": {
    "records": ["203.0.113.111"],
    "type": "A",
    "ttl": 300
  }
}

# Response status 400 Bad request
$ curl -s -H "Content-type: application/json" -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XPUT http://your-url/hostzone/record -d @record.json
{
  "status": "error",
  "detail": {
    "message": "There is missing parameters."
  }
}
```

### DELETE hostzone/record

```bash
# Response status 200 OK
$ curl -s -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XDELETE http://your-url/hostzone/record
{
  "status": "deleted"
}
```

LICENSE
-------

[MIT](https://github.com/chroju/serverless-ddns/blob/master/LICENSE)

Author
------

[chroju](https://chroju.net)

