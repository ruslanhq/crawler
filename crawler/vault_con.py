import os

import hvac


class VaultClient:
    _client = None

    def __init__(self, mount_point):
        if not self._client:
            self._client = self._get_client()
        self.mount_point = mount_point

    @staticmethod
    def _get_client():
        return hvac.Client(
            url=os.getenv('VAULT_ADDR'),
            token=os.getenv('VAULT_TOKEN')
        )

    def get_value(self, path, key):
        get_response = self._client.secrets.kv.v2.read_secret_version(
            mount_point=self.mount_point, path=path
        )
        result = get_response['data']['data'].get(key)
        assert result, 'Incorrect fetch value from Vault'

        return result
