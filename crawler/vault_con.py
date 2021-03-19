import os
import hvac


class VaultClient:
    _client = None

    def __init__(self, mount_point):
        if not self._client:
            self._client = self._get_client()
        self.mount_point = mount_point

    @staticmethod
    def _get_client() -> hvac.Client:
        _client = hvac.Client(os.getenv('VAULT_ADDR'))

        _client.auth.approle.login(
            role_id=os.getenv('VAULT_ROLE_ID'),
            secret_id=os.getenv('VAULT_SECRET_ID')
        )

        return _client

    def get_value(self, path, key):
        get_response = self._client.secrets.kv.v2.read_secret_version(
            mount_point=self.mount_point, path=path
        )
        result = get_response['data']['data'].get(key)
        assert result, 'Incorrect fetch value from Vault'

        return result
