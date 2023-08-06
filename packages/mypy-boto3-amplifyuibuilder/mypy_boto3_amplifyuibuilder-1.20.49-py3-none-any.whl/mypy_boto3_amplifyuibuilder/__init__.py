"""
Main interface for amplifyuibuilder service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplifyuibuilder import (
        AmplifyUIBuilderClient,
        Client,
        ListComponentsPaginator,
        ListThemesPaginator,
    )

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")

    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```
"""
from .client import AmplifyUIBuilderClient
from .paginator import ListComponentsPaginator, ListThemesPaginator

Client = AmplifyUIBuilderClient


__all__ = ("AmplifyUIBuilderClient", "Client", "ListComponentsPaginator", "ListThemesPaginator")
