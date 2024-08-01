from http import HTTPStatus

from src.common.error.http import HTTPError


class RequestExtensions:
    """
    Handles all request extensions.
    """

    def raise_if_dependency_unsuccessful(success: bool):
        """
        Raises an HTTPError if the operation is unsuccessful.

        Args:
            success (bool): The success flag of the operation.

        Raises:
            HTTPError: If the operation failed, indicating issues with external dependencies.
        """
        if not success:
            raise HTTPError(
                http_status=HTTPStatus.FAILED_DEPENDENCY,
                error_code="FailedProviderDependency",
                message="An error occurred while contacting the provider.",
            )

    def raise_if_not_found(entity: any, id: str, type: str):
        """
        Raises an HTTPNotFoundError if the entity is None.

        Args:
            entity (any); The entity to be evaluated.
            id (str): The entity identifier.
            type (str): The entity type.

        Raises:
            HTTPError: If the entity is None, indicating the item does not exist.
        """
        if not entity or (isinstance(entity, list) and len(entity) == 0):
            raise HTTPError(
                http_status=HTTPStatus.NOT_FOUND,
                error_code=f"{type.capitalize()}NotFound",
                message=f"The '{type}' with id '{id}' does not exist.",
            )
