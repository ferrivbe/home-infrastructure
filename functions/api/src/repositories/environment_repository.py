import os

from src.common.constants.environment import EnvironmentConstants
from src.common.error.http import HTTPInternalServerError


class EnvironmentRepository:
    """
    Manages access to environment variables related to the application's configuration.

    This class provides methods to retrieve specific environment variables necessary for the application's
    file distribution system. It includes error handling for missing environment variables to prevent runtime errors
    and ensure that the necessary configurations are available for the application's operations.

    Attributes:
        environment (dict): A dictionary representing the current environment variables.
    """

    def __init__(self):
        """
        Initializes the EnvironmentRepository instance by setting the environment attribute to the current
        operating system's environment variables.
        """
        self.environment = os.environ

    def get_api_host(self) -> str:
        """
        Retrieves the API host from an environment variable.

        This method accesses a specific environment variable that stores the API host URL
        using the `_get_environment_variable` method with the `EnvironmentConstants.API_HOST` key.

        Returns:
            str: The API host URL retrieved from the environment variable. If the environment
                 variable is not set, the method behavior (e.g., return value, raising an exception)
                 depends on the implementation of `_get_environment_variable`.

        Note:
            This method assumes that `_get_environment_variable` is implemented in the class
            and that `EnvironmentConstants.API_HOST` is a valid key that corresponds to the API host
            environment variable.
        """
        return self._get_environment_variable(EnvironmentConstants.API_HOST)

    def get_aws_region(self) -> str:
        """
        Retrieves the AWS region from an environment variable.

        This method accesses a specific environment variable that stores the AWS region name
        using the `_get_environment_variable` method with the `EnvironmentConstants.REGION` key.

        Returns:
            str: The AWS region name retrieved from the environment variable. If the environment
                 variable is not set, the method behavior (e.g., return value, raising an exception)
                 depends on the implementation of `_get_environment_variable`.

        Note:
            This method assumes that `_get_environment_variable` is implemented in the class
            and that `EnvironmentConstants.REGION` is a valid key that corresponds to the AWS region
            environment variable.
        """
        return self._get_environment_variable(EnvironmentConstants.REGION_NAME)

    def get_service_environment_name(self) -> str:
        """
        Retrieves the name of the service environment from an environment variable.

        This method specifically fetches the name of the environment used for the service, which is typically
        utilized for identifying the current operating environment (e.g., development, staging, production).

        Returns:
            str: The name of the service environment as specified in the environment variable.

        Raises:
            HTTPInternalServerError: If the environment variable is missing, indicating a misconfiguration or
                                    a missing setup step in the environment.
        """
        return self._get_environment_variable(EnvironmentConstants.SERVICE_ENVIRONMENT)

    def _validate_environment_variable(
        self, environment_variable: str, environment_variable_name: str
    ):
        """
        Validates that an environment variable is not None.

        If the environment variable is None, indicating it is missing, this method raises an HTTPInternalServerError
        to signal the issue.

        Args:
            environment_variable (str): The value of the environment variable to be validated.
            environment_variable_name (str): The name of the environment variable being validated.

        Raises:
            HTTPInternalServerError: If the environment variable is None, indicating it is missing.
        """
        if environment_variable is None:
            raise HTTPInternalServerError(
                "EnvironmentVariableMissing",
                "The environment variable '%(name)s' is missing in current context."
                % {"name": environment_variable_name},
            )

    def _get_environment_variable(self, environment_variable_name: str) -> str:
        """
        Retrieves and processes an environment variable.

        This method fetches an environment variable's value by its name and replaces any '\\n' characters
        with '\n'. It then validates the variable to ensure it is not None.

        Args:
            environment_variable_name (str): The name of the environment variable to retrieve.

        Returns:
            str: The processed value of the environment variable.

        Raises:
            HTTPInternalServerError: If the environment variable is missing.
        """
        environment_variable: str = os.getenv(environment_variable_name).replace(
            r"\n", "\n"
        )

        self._validate_environment_variable(
            environment_variable=environment_variable,
            environment_variable_name=environment_variable_name,
        )

        return environment_variable
