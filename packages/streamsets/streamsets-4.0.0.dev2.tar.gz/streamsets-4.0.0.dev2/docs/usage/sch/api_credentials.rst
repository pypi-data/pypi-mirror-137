.. _api-credentials:
Api Credentials
===============
An API credential consists of a credential ID and an authentication token.

Creating a new Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you create an API credential, Control Hub returns the credential ID and authentication token values in
a :py:class:`streamsets.sdk.sch_api.Command` object.
You must copy and store the authentication token (json value specified for the key 'authToken' ) in a secure location.
You cannot retrieve the token value from Control Hub at a later time.

If you lose the authentication token or if the token becomes compromised, you can regenerate the API credential.

To create a new :py:class:`streamsets.sdk.sch_models.ApiCredential` object and add it to Control Hub,
use the :py:class:`streamsets.sdk.sch_models.ApiCredentialBuilder` class.
Use the :py:meth:`streamsets.sdk.ControlHub.get_api_credential_builder` method to instantiate the builder object:

.. code-block:: python

    >>> api_credential_builder = sch.get_api_credential_builder()
    >>> api_credential = api_credential_builder.build(name='From SDK', generate_auth_token=True)
    >>> command = sch.add_api_credential(api_credential)
    >>> command.response.json()
    {'label': 'From SDK', 'userId': '3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046',
    'componentId': '93a9f902-0619-4f6d-8aab-174be9155046',
    'authToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJzIjoiZDZjYmFhODZmMDBmM2I3ZjhkOTBkMzUwZTc4YTY0Y2Q3MjVjYTBlOGY2ZjM5YzAwMjU0ZDlmMDUzZmIxZTYwYzkzOWI2NDhkZTU4NmE2MmMzZmFiMjQzOWY3ZGNhZGI0NTVlMzRlNTg4MjYyNjAyYWU5MzEwYzU5NzlhZGIxM2EiLCJ2IjoxLCJpc3MiOiJkZXYiLCJqdGkiOiI5M2E5ZjkwMi0wNjE5LTRmNmQtOGFhYi0xNzRiZTkxNTUwNDYiLCJvIjoiM2JiNzM4MzYtYjdlYy0xMWViLWI5M2MtNzU4ZDczMDEwMDQ2In0.',
    'active': True}

Retrieving existing Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve api_credentials you can use :py:meth:`streamsets.sdk.ControlHub.api_credentials` or
:py:meth:`streamsets.sdk.ControlHub.api_credentials.get` method.

.. code-block:: python

    >>> # Get all api credentials belonging to current organization
    >>> sch.api_credentials
    [<ApiCredential (name=From SDK, credential_id=271500ee-1d77-43cc-a0bf-5bf2f2c0bd1f, active=True, created_by=3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046)>,
    <ApiCredential (name=From SDK 2, credential_id=7d995b08-b86e-449c-b5e4-83d4aed30c8a, active=True, created_by=3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046)>,
    <ApiCredential (name=Kirti, credential_id=0ce71215-f09d-4c9e-946a-d30c1d1e9df8, active=False, created_by=3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046)>
    >>>
    >>> # Get a particular api credential
    >>> sch.api_credentials.get(name='From SDK')
    <ApiCredential (name=From SDK, credential_id=271500ee-1d77-43cc-a0bf-5bf2f2c0bd1f, active=True,
    created_by=3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046)>

Deactivating an existing Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API credentials must be active to use the credentials to call a Control Hub REST API.
You can temporarily deactivate an API credential to disable using that credential to access Control Hub.

For this purpose, you can use :py:meth:`streamsets.sdk.ControlHub.deactivate_api_credential` method.

.. code-block:: python

    >>> api_credential = sch.api_credentials.get(name='From SDK')
    >>> sch.deactivate_api_credential(api_credential)
    <sdk.sch_api.Command object at 0x1081befd0>
    >>> api_credential.active
    False

Activating an existing Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API credentials must be active to use the credentials to call a Control Hub REST API.
To activate, you can use :py:meth:`streamsets.sdk.ControlHub.activate_api_credential` method.

.. code-block:: python

    >>> api_credential = sch.api_credentials.get(name='From SDK')
    >>> sch.activate_api_credential(api_credential)
    <sdk.sch_api.Command object at 0x10820bba8>
    >>> api_credential.active
    True

Renaming an existing Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can rename an API credential. Renaming a credential simply changes the display name of the credential in
the API Credentials view.

Renaming a credential does not change the generated credential ID or authentication token.
For this purpose, you can use :py:meth:`streamsets.sdk.ControlHub.rename_api_credential` method.

.. code-block:: python

    >>> api_credential = sch.api_credentials.get(name='From SDK')
    >>> api_credential.name = 'From SDK Updated Name'
    >>> sch.rename_api_credential(api_credential)
    >>> fetched_api_credential = sch.api_credentials.get(name='From SDK Updated Name')
    >>> fetched_api_credential.name
    'From SDK Updated Name'

Regenerating auth token for an existing Api Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you lose the authentication token for a credential or if the token becomes compromised, you can regenerate the
API credential. When you regenerate a credential, Control Hub retains the credential name and ID,
but generates a new authentication token.

For this purpose, you can use :py:meth:`streamsets.sdk.ControlHub.regenerate_api_credential_auth_token` method.

.. code-block:: python

    >>> api_credential = sch.api_credentials.get(name='From SDK')
    >>> sch.regenerate_api_credential_auth_token(api_credential)
    {'label': 'From SDK', 'userId': '3b56a1a4-b7ec-11eb-b93c-f3705df146b8@3bb73836-b7ec-11eb-b93c-758d73010046',
    'componentId': '93a9f902-0619-4f6d-8aab-174be9155046',
    'authToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJzIjoiYjYyM2Q1NzM1M2RiODY3Zjc4MzI1MzNmYzA4YTBiOTU4ZWMyN2Y5NGU2NTE3ZGE1N2U3MzQ2NTVjMmY5YmQ5YWI2YzlhNGQ1ODEiLCJ2IjoxLCJpc3MiOiJkZXYiLCJqdGkiOiIyNzE1MDBlZS0xZDc3LTQzY2MtYTBiZi01YmYyZjJjMGJkMWYiLCJvIjoiM2JiNzM4MzYtYjdlYy0xMWViLWI5M2MtNzU4ZDczMDEwMDQ2In0.',
    'active': True}

Deleting existing Api Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When needed, you can delete API credentials. You can delete active or deactivated API credentials.

For this purpose, you can use :py:meth:`streamsets.sdk.ControlHub.delete_api_credentials` method.


.. code-block:: python

    >>> # Delete an api credential
    >>> api_credential = sch.api_credentials.get(name='From SDK')
    >>> sch.delete_api_credentials(api_credential)
    >>>
    >>> # Delete multiple api credentials
    >>> api_credentials = sch.api_credentials.get(name='From SDK')
    >>> sch.delete_api_credentials(*api_credentials)
