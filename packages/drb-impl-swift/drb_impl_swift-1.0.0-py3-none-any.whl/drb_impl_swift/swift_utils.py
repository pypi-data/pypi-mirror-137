import io
from typing import Dict

import swiftclient.client


class SwiftAuth:
    """
    This class give us all the requirement to connect to a swift service.

    Parameters:
        authurl: authentication URL (default: None)
        user: user name to authenticate as (default: None)
        key: key/password to authenticate with (default: None)
        retries: Number of times to retry the request before failing
                 (default: 5)
        preauthurl: storage URL (if you have already authenticated)
                    (default: None)
        preauthtoken: authentication token (if you have already
                      authenticated) note authurl/user/key/tenant_name
                      are not required when specifying preauthtoken
                      (default: None)
        snet: use SERVICENET internal network default is False (default: False)
        starting_backoff: initial delay between retries
                          (seconds) (default: 1)
        max_backoff: maximum delay between retries
        (seconds) (default: 64)
        auth_version: OpenStack auth version (default: 1)
        tenant_name: The tenant/account name, required when connecting
                     to an auth 2.0 system (default: None).
        os_options: The OpenStack options which can have tenant_id,
                    auth_token, service_type, endpoint_type,
                    tenant_name, object_storage_url, region_name,
                    service_username, service_project_name,
                    service_key (default: None).
        insecure: Allow to access servers without checking SSL certs.
                  The server's certificate will not be verified
                  (default: False).
        cert: Client certificate file to connect on SSL server
              requiring SSL client certificate (default: None).
        cert_key: Client certificate private key file (default: None).
        ssl_compression: Whether to enable compression at the SSL layer.
                         If set to 'False' and the pyOpenSSL library is
                         present an attempt to disable SSL compression
                         will be made. This may provide a performance
                         increase for https upload/download operations
                         (default: True).
        retry_on_ratelimit: by default, a ratelimited connection will
                            raise an exception to the caller. Setting
                            this parameter to True will cause a retry
                            after a backoff (default: False).
        timeout: The connect timeout for the HTTP connection (default: None).
        session: A keystoneauth session object (default: None).
        force_auth_retry: reset auth info even if client got unexpected
                          error except 401 Unauthorized (default: False).
    """

    def __init__(self, authurl=None, user=None,
                 key=None, preauthurl=None,
                 preauthtoken=None,
                 os_options: Dict = None,
                 auth_version="1",
                 **kwargs):
        self.authurl = authurl
        self.user = user
        self.key = key
        self.preauthurl = preauthurl
        self.preauthtoken = preauthtoken
        self.os_options = os_options
        self.auth_version = auth_version

        self.retries = kwargs.get('retries', 5)
        self.snet = kwargs.get('snet', False)
        self.starting_backoff = kwargs.get('starting_backoff', 1)
        self.max_backoff = kwargs.get('max_backoff', 64)
        self.tenant_name = kwargs.get('tenant_name', None)
        self.cacert = kwargs.get('cacert', None)
        self.insecure = kwargs.get('insecure', False)
        self.cert = kwargs.get('cert', None)
        self.cert_key = kwargs.get('cert_key', None)
        self.ssl_compression = kwargs.get('ssl_compression', True)
        self.retry_on_ratelimit = kwargs.get('retry_on_ratelimit', False)
        self.timeout = kwargs.get('timeout', None)
        self.session = kwargs.get('session', None)
        self.force_auth_retry = kwargs.get('force_auth_retry', False)


class SwiftConnection:
    """
    This class use the singleton pattern to provide too
    much connection to the swift server.

    Parameters:
        auth: An Auth object to provide all the information required
              to establish the connection with the server.
    """
    swift = None

    def __new__(cls,
                auth: SwiftAuth):
        if cls.swift is None:
            cls.swift = swiftclient.client.Connection(
                auth.authurl, auth.user,
                auth.key, auth.retries,
                auth.preauthurl,
                auth.preauthtoken, auth.snet,
                auth.starting_backoff,
                auth.max_backoff, auth.tenant_name,
                auth.os_options,
                auth.auth_version, auth.cacert,
                auth.insecure, auth.cert,
                auth.cert_key,
                auth.ssl_compression,
                auth.retry_on_ratelimit,
                auth.timeout, auth.session,
                auth.force_auth_retry)
        return cls.swift


class Download(io.BytesIO):

    def __init__(self, response: swiftclient.client._RetryBody):
        self._resp = response
        self._buff = bytearray(0)
        super().__init__(self._buff)

    def read(self, *args, **kwargs):
        if isinstance(self._resp, bytes):
            return self._resp
        if not (len(args) > 0 and isinstance(
                args[0], int) and args[0] > 0):
            for chunk in self._resp:
                self._buff.extend(chunk)

            return self._buff
        for chunk in self._resp:
            self._buff.extend(chunk)
            if len(self._buff) >= args[0]:
                return self._buff

    def close(self) -> None:
        super().close()
        self._resp.close()
