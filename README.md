Serverless DDNS
===============

Serverless DDNS management REST API framework created via [Chalice](https://github.com/aws/chalice).

This framework provides REST API endpoints and methods to realize private Dynamic DNS in cooperation with the Route53 hostzone that registered your own domain. For example, you could register a DNS A record to resolve any domain to your global IP address with PUT method.

```bash
$ curl -s -H "Content-type: application/json" -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XPUT http://your-url/hostzone/myhome.example.net
{
  "status": "created",
  "detail": {
    "records": ["203.0.113.111"],
    "type": "A",
    "ttl": 300
  }
}
```


Setup
-----

This framework can be setup with Chalice.

### Requirements

Since Chalice can only deploy AWS Lambda and API Gateway, you must prepare the following items with yourself.

* Get your own domain name to use with DDNS.
* Register your domain name with AWS Route53.

### Deploy serverless-ddns

**NOTE:** The deploy process described here is a temporary one. It can be deployed more easily in the future :bow: .

What is written here contains a simplified usage of AWS Chalice. It is recommended that you read [Chalice Documentation](http://chalice.readthedocs.io/en/latest/quickstart.html) and understand what kind of tool it is.

You could install chalice with pip.

```bash
$ pip install chalice
```

First, clone this repo.

```bash
$ git clone https://github.com/chroju/serverless-ddns
```

Next, create your own IAM policy json from `policy-example.json`. You must rewrite hosted zone ID of 26L with yours.

```bash
$ cp .chalice/{policy-example,policy}.json
$ vim .chalice/policy.json

# ...
#
#   {
#     "Effect": "Allow",
#     "Action": [
#       "route53:ListResourceRecordSets"
#     ],
#     "Resource": "arn:aws:route53:::hostedzone/XXXXXXXXXXXXXX" <= Rewrite here.
#   }
# ]
# ...
```

You could deploy serverless-ddns at this point. Make your AWS credential file if you have not make it.

```bash
$ mkdir ~/.aws
$ cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION
```

and deploy. If succeeded, you get API endpoint URL.

```bash
$ chalice deploy --stage prod
...
https://XXXXXXXXXX.execute-api.ap-northeast-1.amazonaws.com/api/
```

At the last, setup API key in AWS console. Please reference AWS Developer guide like [here (in Japanese)](http://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/api-gateway-setup-api-key-with-restapi.html).


REST API
--------

After you finished the setup, you could manipulate DDNS with REST API.

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
# IP address will be set up with your source global IP.
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
$ curl -s -H "Content-type: application/json" -H "Authorization: Token token=XXXXXXXXXXXXXXXXXXXX" -XPUT http://your-url/hostzone/record
{
  "status": "error",
  "detail": {
    "message": "There is missing parameters."
  }
}
```

### POST hostzone/record

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


LICENSE
-------

[MIT](https://github.com/chroju/serverless-ddns/blob/master/LICENSE)


Author
------

[chroju](https://chroju.net)

