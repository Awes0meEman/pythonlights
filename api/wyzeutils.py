import os
from wyze_sdk import Client, api
from wyze_sdk.errors import WyzeApiError

def printDevices(access_token):
    client = Client(token=access_token)

    try:
        response = client.devices_list()
        for device in client.devices_list():
            print(f"mac: {device.mac}")
            print(f"nickname: {device.nickname}")
            print(f"is_online: {device.is_online}")
            print(f"product model: {device.product.model}")
    except WyzeApiError as e:
        print(f"Got an error: {e}")

def main():
    response = login()
    if response != None:
        printDevices(response['access_token'])
    else:
        raise Exception("Error logging into Wyze API")

def verifyToken(token):
    if token == None:
        return False
    else:
        return True

def login():
    email = os.getenv('WYZE_EMAIL')
    password = os.getenv('WYZE_PASS')
    key_id = os.getenv('WYZE_KEY_ID')
    api_key = os.getenv('WYZE_API_KEY')
    if email == None:
        return None
    elif password == None:
        return None
    elif key_id == None:
        return None
    elif api_key == None:
        return None
    return Client().login(email=email, password=password, api_key=api_key, key_id=key_id)

#main()
