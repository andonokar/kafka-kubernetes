import requests
import re
import json


def lambda_handler(event, context):
    # ALTERAR O ID SEMPRE QUE DERRUBAR E SUBIR O KAFKA
    url = "http://10.0.3.221:8088/query"
    headers = {"Accept": "application/vnd.ksql.v1+json"}
    data = {
        "ksql": f"PRINT '{event['queryStringParameters']['topic']}' FROM BEGINNING;"
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    dicionario = {'statusCode': 200, 'response': []}
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response JSON
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                r = re.findall(r"value:\s*(.*})", decoded_line)
                if r:
                    json_dict = json.loads(r[0])
                    if json_dict.get('etapa') == f"{event['queryStringParameters']['etapa']}":
                        dicionario.get('response').append(json_dict)
            else:
                break
        print(dicionario)
        return {
            'statusCode': 200,
            'body': json.dumps(dicionario['response'])
        }
    else:
        return f"Request failed with status code: 500"
