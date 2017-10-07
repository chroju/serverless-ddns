Serverless DDNS
===============

Serverless DDNS management framework created via [Chalice](https://github.com/aws/chalice).

Usage
-----

Manipulate with REST API.

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
