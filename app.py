import json
import boto3
from chalice import Chalice, NotFoundError, BadRequestError

r53 = boto3.client('route53')
app = Chalice(app_name='serverless-ddns')
app.debug = True


@app.route('/', api_key_required=True)
def index():
    hosted_zones = _get_dns_hosted_zones()
    if len(hosted_zones):
        result_json = {"hostzones": [{'id': zone['Id'].lstrip("/hostedzone/"), 'name': zone['Name']} for zone in hosted_zones]}
        return _json_dumps(result_json)
    else:
        raise NotFoundError("any hostzone is not found")


@app.route('/{hostzone}/{name}', methods=['GET', 'PUT', 'POST', 'DELETE'], api_key_required=True)
def manage_record(hostzone, name):
    request = app.current_request

    if request.method == 'GET':
        record_sets = _get_dns_record(hostzone=hostzone, name=name)
        if len(record_sets):
            record_set_detail = [{'value': i['ResourceRecords'][0]['Value'], 'type': i['Type'], 'ttl': i['TTL']} for i in record_sets]
            result_json = {'status': 'exist', 'detail': record_set_detail}
            return _json_dumps(result_json)
        else:
            raise NotFoundError("{} is not registered in {}".format(name, hostzone))

    elif request.method == 'PUT':
        values = [request.context['identity']['sourceIp']]
        return _json_dumps(_change_dns_record(hostzone=hostzone, name=name, values=values, action='UPSERT'))

    elif request.method == 'POST':
        values = request.json_body['records']
        record_type = request.json_body['type']
        ttl = request.json_body['ttl']
        return _json_dumps(_change_dns_record(hostzone=hostzone, name=name, values=values, action='UPSERT', record_type=record_type, ttl=ttl))

    elif request.method == 'DELETE':
        record_sets = _get_dns_record(hostzone=hostzone, name=name)
        if len(record_sets) == 1:
            record_type = record_sets[0]['Type']
            ttl = record_sets[0]['TTL']
            values = [i["Value"] for i in record_sets[0]['ResourceRecords']]
        elif len(record_sets) > 1:
            raise BadRequestError("too many records exist in {}".format(name))
        else:
            raise NotFoundError("{} is not registered in {}".format(name, hostzone))
        return _json_dumps(_change_dns_record(hostzone=hostzone, name=name, values=values, action='DELETE', record_type=record_type, ttl=ttl))


def _get_dns_hosted_zones():
    return r53.list_hosted_zones()['HostedZones']


def _get_dns_record(hostzone, name):
    record_sets = r53.list_resource_record_sets(
        HostedZoneId=hostzone
    )['ResourceRecordSets']

    # return record_sets
    return [i for i in record_sets if name == i['Name'] and i['Type'] == 'A' and 'ResourceRecords' in i]


def _change_dns_record(hostzone, name, values, action, ttl=300, record_type='A'):
    result = r53.change_resource_record_sets(
        HostedZoneId=hostzone,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': i} for i in values]
                    }
                }
            ]
        }
    )['ChangeInfo']

    return {'status': result['Status']}


def _json_dumps(result_json):
    return json.dumps(result_json, indent=2, separators=(',', ':'))
