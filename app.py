import json
import boto3
from chalice import Chalice

r53 = boto3.client('route53')
app = Chalice(app_name='serverless-ddns')

SEPS = (',', ':')


@app.route('/')
def index():
    hosted_zones = _get_dns_hosted_zones()
    if len(hosted_zones):
        return [{'id': zone['Id']} for zone in hosted_zones]
    else:
        return json.dumps({}, indent=2, separators=SEPS)


@app.route('/{hostzone}/{name}', methods=['GET', 'PUT'])
def state_of_record(hostzone, name):
    request = app.current_request

    if request.method == 'GET':
        record_sets = _get_dns_record(hostzone=hostzone, name=name)
        if len(record_sets):
            record_set_detail = [{'value': i['Value'], 'type': i['Type'], 'ttl': i['TTL']} for i in record_sets['ResourceRecords']]
            result_json = { 'status': 'exist', 'detail': record_set_detail }
            return json.dumps(result_json, indent=2, separators=SEPS)
        else:
            return json.dumps({"status": "absent"}, indent=2, separators=SEPS)
    elif request.method == 'PUT':
        if request.json_body:
            records = request.json_body['records']
            record_type = request.json_body['type']
            ttl = request.json_body['ttl']
        else:
            records = [request.context['identity']['sourceIp']]
            record_type = 'A'
            ttl = 300

        result = client.change_resource_records_sets(
            HostedZoneId=hostzone,
            ChangeBatch={
                Changes:[
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name'
                        }
                    }
                ]
            }
        )['ChangeInfo']

        result_json = { 'status': result['Status'], detail}
        return json.dumps(result_json, indent=2, separators=SEPS)


def _get_dns_hosted_zones():
    return r53.list_hosted_zones()['HostedZones']


def _get_dns_record(hostzone, name):
    record_sets = r53.list_resource_record_sets(
        HostedZoneId=hostzone
    )['ResourceRecordSets']

    if name[-1] is not '.':
        name = name + '.'

    return [i for i in record_sets if name is i['Name'] and i['Type'] is 'A' and hasattr(i, 'ResourceRecords')]
