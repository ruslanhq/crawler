import os
import hvac


def get_proxy_list():
    client = hvac.Client(url=os.environ['VAULT_ADDR'],
                         token=os.environ['VAULT_TOKEN'])
    read_response = client.secrets.kv.read_secret_version(path='proxy')
    result = read_response['data']['data']
    proxy_list = result['prx'].split()
    return proxy_list
