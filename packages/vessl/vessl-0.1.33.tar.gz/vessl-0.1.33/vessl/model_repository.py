from typing import List

from openapi_client import ModelRepositoryUpdateAPIInput
from openapi_client.models import (
    ModelRepositoryCreateAPIInput,
    ResponseModelRepositoryDetail,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name


def read_model_repository(
    repository_name: str, **kwargs
) -> ResponseModelRepositoryDetail:
    """Read model repository

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_repository_read_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
    )


def list_model_repositories(**kwargs) -> List[ResponseModelRepositoryDetail]:
    """List model repositories

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_repository_list_api(
        organization_name=_get_organization_name(**kwargs),
    ).results


def create_model_repository(
    name: str, description: str = None, **kwargs
) -> ResponseModelRepositoryDetail:
    """Create model repository

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_repository_create_api(
        organization_name=_get_organization_name(**kwargs),
        model_repository_create_api_input=ModelRepositoryCreateAPIInput(
            name=name,
            description=description,
        ),
    )


def update_model_repository(
    name: str, description: str, **kwargs
) -> ResponseModelRepositoryDetail:
    """Update model repository

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_update_api(
        organization_name=_get_organization_name(**kwargs),
        name=name,
        model_repository_update_api_input=ModelRepositoryUpdateAPIInput(
            description=description
        ),
    )


def delete_model_repository(name: str, **kwargs) -> object:
    """Delete model repository

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_repository_delete_api(
        organization_name=_get_organization_name(**kwargs),
        name=name,
    )
