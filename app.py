import json
import boto3
from chalice import Chalice

r53 = boto3.client('route53')
app = Chalice(app_name='serverless-ddns')
app.debug = True


@app.route('/')
def index():
    hosted_zones = _get_dns_hosted_zones()
    if len(hosted_zones):
        return [{'id': zone['Id']} for zone in hosted_zones]
    else:
        return _json_dumps({})


@app.route('/{hostzone}/{name}', methods=['GET', 'PUT', 'POST', 'DELETE'])
def manage_record(hostzone, name):
    request = app.current_request

    if request.method == 'GET':
        record_sets = _get_dns_record(hostzone=hostzone, name=name)
        if len(record_sets):
            record_set_detail = [{'value': i['ResourceRecords'][0]['Value'], 'type': i['Type'], 'ttl': i['TTL']} for i in record_sets]
            result_json = {'status': 'exist', 'detail': record_set_detail}
            return _json_dumps(result_json)
        else:
            return _json_dumps({"status": "absent"})

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
        if len(record_sets):
            record_set_detail = [{'value': i['ResourceRecords'][0]['Value'], 'type': i['Type'], 'ttl': i['TTL']} for i in record_sets]
            result_json = {'status': 'exist', 'detail': record_set_detail}
        return _json_dumps(_change_dns_record(hostzone=hostzone, name=name, values=values, action='DELETE'))


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
