#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
MongoDB Atlas API SDK Exceptions and error handling
"""

from compose_x_common.compose_x_common import keyisset

USER_ERRORS = ["USER_ALREADY_EXISTS", "INVALID_ATTRIBUTE", "DUPLICATE_DATABASE_ROLES"]


class AtlasGenericException(Exception):
    """
    Generic class handling for the SDK using the request as input
    """

    def __init__(self, msg, code, details):
        """

        :param msg:
        :param code:
        :param details:
        """
        super().__init__(msg, code, details)


class DatabaseUserError(AtlasGenericException):
    """
    Top class for DatabaseUser exceptions
    """

    def __init__(self, code, details):
        if details.get("errorCode", None) == "USER_ALREADY_EXISTS":
            raise (DatabaseUserConflict(code, details))
        if details.get("errorCode", None) == "INVALID_ATTRIBUTE":
            raise (DatabaseUserInvalidAttribute(code, details))
        if details.get("errorCode", None) == "DUPLICATE_DATABASE_ROLES":
            raise (DatabaseUserDuplicateDatabaseRole(code, details))
        super().__init__("Something was wrong with the client request.", code, details)


class DatabaseUserConflict(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User already exists"), code, details)


class DatabaseUserInvalidAttribute(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User attribute error"), code, details)


class DatabaseUserDuplicateDatabaseRole(AtlasGenericException):
    """
    Exception when the
    """

    def __init__(self, code: int, details: dict):
        super().__init__(details.get("detail", "User attribute error"), code, details)


def evaluate_atlas_api_return(function):
    """
    Decorator to evaluate the requests payload returned
    """

    def wrapped_answer(*args, **kwargs):
        """
        Decorator wrapper
        """
        payload = function(*args, **kwargs)
        if payload.status_code not in [200, 201, 202, 204] and not keyisset(
            "ignore_failure", kwargs
        ):
            details = payload.json()
            if details.get("errorCode", None) in USER_ERRORS:
                raise DatabaseUserError(payload.status_code, details)
            else:
                raise AtlasGenericException(
                    details.get("errorCode", None), payload.status_code, details
                )
        elif keyisset("ignore_failure", kwargs):
            return payload
        return payload

    return wrapped_answer
