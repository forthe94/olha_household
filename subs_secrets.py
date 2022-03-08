import json
import os

private_key = os.getenv('PRIVATE_KEY')
private_key_id = os.getenv('PRIVATE_KEY_ID')
serv_acc = os.getenv('SERV_ACC')


def substitude_serv_acc():
    with open('serv_acc.json', 'w', encoding='utf-8') as file:
        file.write(serv_acc)

