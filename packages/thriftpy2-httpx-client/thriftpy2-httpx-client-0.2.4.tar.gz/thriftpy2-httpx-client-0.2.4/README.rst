ThriftPy2 HTTPX Client
======================

This package is provides an alternative HTTP client for ThriftPy2 which
uses HTTPX instead of the builtin ``http.client`` and ``http.server``
libraries. This allows the developer to use more complex features like
authentication, fine grained timeouts, and asyncio.

Examples:
---------

**Setup (Borrowed from ThriftPy2 Docs):**

.. code-block:: thrift

    # pingpong.thrift
    service PingPong {
        string ping(),
    }

.. code-block:: python

    import thriftpy2
    from thriftpy2.http import make_server

    pingpong_thrift = thriftpy2.load(
        "pingpong.thrift",
        module_name="pingpong_thrift",
    )

    class Dispatcher(object):
        def ping(self):
            return "pong"

    server = make_server(
        service=pingpong_thrift.PingPong,
        handler=Dispatcher(),
        host='127.0.0.1',
        port=6000,
    )
    server.serve()


**Async Usage:**

.. code-block:: python

    from thriftpy2_httpx_client import make_aio_client

    client = await make_aio_client(pingpong_thrift, url='http://localhost:6000')
    print(await client.ping())  # prints 'pong'


**Sync Usage:**

.. code-block:: python

    from thriftpy2_httpx_client import make_sync_client

    client = make_sync_client(pingpong_thrift, url='http://localhost:6000')
    print(client.ping())  # prints 'pong'


Additional keyword arguments can be passed to the client to configure
the internal ``httpx.AsyncClient()`` and ``httpx.Client()`` instances. For
example, you can enable Kerberos authentication using ``httpx-gssapi``:

.. code-block:: python

    from httpx_gssapi import HTTPSPNEGOAuth
    from thriftpy2_httpx_client import make_aio_client

    client = await make_aio_client(
        pingpong_thrift,
        url='http://localhost:6000',
        auth=HTTPSPNEGOAuth(),
    )
    print(await client.ping())  # prints 'pong'
