"""
Main interface for amplifyuibuilder service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amplifyuibuilder import (
        AmplifyUIBuilderClient,
        Client,
        ListComponentsPaginator,
        ListThemesPaginator,
    )

    session = get_session()
    with async session.create_client("amplifyuibuilder") as client:
        client: AmplifyUIBuilderClient
        ...


    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```
"""
from .client import AmplifyUIBuilderClient
from .paginator import ListComponentsPaginator, ListThemesPaginator

Client = AmplifyUIBuilderClient


__all__ = ("AmplifyUIBuilderClient", "Client", "ListComponentsPaginator", "ListThemesPaginator")
