import json
import os

private_key = os.getenv('PRIVATE_KEY')
private_key_id = os.getenv('PRIVATE_KEY_ID')


def substitude_serv_acc():
    with open('serv_acc.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    data['private_key'] = private_key.replace(' ', '\n')
    data['private_key_id'] = private_key_id
    print(data)
    with open('serv_acc.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

