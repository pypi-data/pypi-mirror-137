#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""Main module."""

import logging as logthings
import re
import sys

import requests
from compose_x_common.aws import validate_iam_role_arn
from compose_x_common.compose_x_common import keyisset, set_else_none
from requests.auth import HTTPDigestAuth

from .errors import evaluate_atlas_api_return


def setup_logging():
    """Function to setup logging for ECS ComposeX.
    In case this is used in a Lambda function, removes the AWS Lambda default log handler

    :returns: the_logger
    :rtype: Logger
    """
    default_level = True
    formats = {
        "INFO": logthings.Formatter(
            "%(asctime)s [%(levelname)8s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ),
        "DEBUG": logthings.Formatter(
            "%(asctime)s [%(levelname)8s] %(filename)s.%(lineno)d , %(funcName)s, %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ),
    }

    logthings.basicConfig(level="INFO")
    root_logger = logthings.getLogger()
    for h in root_logger.handlers:
        root_logger.removeHandler(h)
    the_logger = logthings.getLogger("mongodb_atlas_api_sdk")

    if not the_logger.handlers:
        if default_level:
            formatter = formats["INFO"]
        else:
            formatter = formats["DEBUG"]
        handler = logthings.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        the_logger.addHandler(handler)

    return the_logger


LOGGER = setup_logging()


class Atlas(object):
    """
    Main class for all others


    :cvar str _hostname: The MongoDB API Hostname
    :cvar str _api: Path to the API
    :
    """

    _hostname = "cloud.mongodb.com"
    _api = "/api/atlas/v1.0"

    def __init__(
        self,
        public_key: str,
        private_key: str,
        api_path: str = None,
        hostname: str = None,
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.api_path = self._api if api_path is None else api_path
        self.hostname = self._hostname if hostname is None else hostname

        self.url = f"https://{self.hostname}{self.api_path}"
        self.auth = HTTPDigestAuth(self.public_key, self.private_key)
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }

    @evaluate_atlas_api_return
    def get_raw(self, url: str = None, ignore_failure: bool = False, **kwargs):
        return requests.get(
            url, auth=self.auth, headers=self.headers, verify=True, **kwargs
        )

    @evaluate_atlas_api_return
    def post_raw(self, url: str = None, **kwargs):
        return requests.post(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def put_raw(self, url: str = None, **kwargs):

        return requests.put(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def patch_raw(self, url: str = None, **kwargs):

        return requests.patch(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=True,
            **kwargs,
        )

    @evaluate_atlas_api_return
    def delete_raw(self, url: str = None, **kwargs):
        return requests.delete(
            url, auth=self.auth, headers=self.headers, verify=True, **kwargs
        )


class AtlasProject(object):
    """
    Class to represent a project
    """

    def __init__(self, atlas_manager: Atlas, project_id: str):
        """

        :param Atlas atlas_manager:
        :param str project_id:
        """
        self.project_id = project_id
        self._atlas_manager = atlas_manager
        self.uri = f"{self._atlas_manager.url}/groups/{self.project_id}"

        self._users_uri = f"{self.uri}/databaseUsers"

    @property
    def atlas_manager(self):
        return self._atlas_manager

    @property
    def users(self):
        req = self.atlas_manager.get_raw(self._users_uri)
        _users = {}
        import json

        for result in req.json()["results"]:
            _user = DatabaseUser(
                self._atlas_manager,
                self,
                result["username"],
            )
            _user.set_from_api_describe(**result)
            _users[result["username"]] = _user
        return _users


class DatabaseUser(object):
    """
    Class to represent and manipulate the Database User
    """

    AWS_TYPES = ["ROLE", "USER"]

    def __init__(
        self,
        atlas_manager: Atlas,
        atlas_project: AtlasProject,
        username: str,
        password: str = None,
        database: str = None,
        aws_iam_type: str = None,
        ldap_auth_type: str = None,
        x509_type: str = None,
    ) -> None:
        """
        :param atlas_project:
        :param username:
        :param database:
        """
        self._atlas_manager = atlas_manager
        self._atlas_project = atlas_project
        self._username = username
        self._password = password
        self._links = []
        self._roles = []
        self._scopes = []
        if database:
            self._database = database
        else:
            self._database = "admin"

        if aws_iam_type or self._username.startswith("arn:aws:iam::"):
            self._database = r"$external"
            if aws_iam_type:
                self._aws_iam_type = aws_iam_type
            else:
                self.define_aws_iam_type()
        else:
            self._aws_iam_type = "NONE"
        self._ldap_auth_type = ldap_auth_type if ldap_auth_type else "NONE"
        self._x509_type = x509_type if x509_type else "NONE"

    def __repr__(self):
        return f"{self.group_id}::{self._username}@{self._database}"

    def validate_type(self):
        are_set = []
        id_props = ["_aws_iam_type", "_password", "_ldap_auth_type", "_x509_type"]
        for prop in id_props:
            if hasattr(self, prop):
                value = getattr(self, prop)
                if isinstance(value, str) and value != "NONE":
                    are_set.append(prop)
                elif not isinstance(value, str) and value is not None:
                    are_set.append(prop)
        if not are_set:
            raise AttributeError("No identification property is set", id_props)
        elif len(are_set) > 1:
            raise AttributeError(
                "There is more than id property defined with another value that NONE",
                are_set,
                "Only one can be set",
            )

    def define_aws_iam_type(self):
        """
        Simple function to define the awsIAMType of the resource if the username looks like an AWS ARN but
        the aws_iam_type was not set
        """
        arn_valid = re.compile(
            r"^arn:aws(?:-[a-z-]+)?:iam::[0-9]{12}:(?P<type>role|user)/[\S]+$"
        )
        parts = arn_valid.match(self._username)
        if not parts:
            raise ValueError(
                "ARN",
                self._username,
                "is not a valid ARN for a user or a role. Must match",
                arn_valid.pattern,
            )
        self._aws_iam_type = parts.group("type").upper()

    def set_from_api_describe(self, **kwargs):
        """
        Sets the attributes values based on the GET reply from MongoDB API.
        """
        self._links = set_else_none("links", kwargs, [])
        self._username = kwargs["username"]
        self._database = kwargs["databaseName"]
        self._aws_iam_type = set_else_none("awsIAMType", kwargs, "NONE")
        self._x509_type = set_else_none("x509Type", kwargs, "NONE")
        self._ldap_auth_type = set_else_none("ldapAuthType", kwargs, "NONE")
        if keyisset("roles", kwargs):
            for _role in kwargs["roles"]:
                self.add_role(**_role)
        if keyisset("scopes", kwargs):
            for _scope in kwargs["scopes"]:
                self.add_scope(**_scope)

    @property
    def group_id(self):
        return self._atlas_project.project_id

    @property
    def username(self):
        return self._username

    @property
    def roles(self):
        return self._roles

    @property
    def scopes(self):
        return self._scopes

    @property
    def href(self):
        for link in self._links:
            if "href" in link and "rel" in link and link["rel"] == "self":
                return link["href"]
        return None

    @property
    def uri(self):
        if self.href:
            return self.href
        else:
            if self._aws_iam_type in self.AWS_TYPES:
                return (
                    f"{self._atlas_project.uri}/databaseUsers/{self._database}/"
                    f"{requests.utils.quote(self._username, safe='')}"
                )
            else:
                return f"{self._atlas_project.uri}/databaseUsers/{self._database}/{self._username}"

    @property
    def exists(self):
        """
        Whether the user exists in the project

        :rtype: bool
        """

        _req = self._atlas_manager.get_raw(self.uri, ignore_failure=True)
        if _req.status_code == 404:
            return False
        return True

    def create(self):
        """
        To create a new user
        """
        req = self._atlas_manager.post_raw(
            self._atlas_project._users_uri, json=self.model
        )
        self.set_from_api_describe(**req.json())
        LOGGER.info(f"{self} - Created successfully.")

    def read(self):
        _req = self._atlas_manager.get_raw(self.uri)
        return _req.json()

    def update(self):
        if not self.href and self.exists:
            self.set_from_api_describe(**self.read())
        _req = self._atlas_manager.patch_raw(self.uri, json=self.model)
        self.set_from_api_describe(**_req.json())
        LOGGER.info(f"{self} - Updated successfully")

    def delete(self):
        """
        To delete one self from project
        """
        if not self.href and self.exists:
            self.set_from_api_describe(**self.read())
        _req = self._atlas_manager.delete_raw(self.uri)
        if _req.status_code == 204:
            LOGGER.info(f"{self} - Deleted successfully")
            self._roles = []
            self._scopes = []
        else:
            LOGGER.error(f"{_req.status_code} - Error on delete for {self}")

    def add_role(
        self, name: str = None, database: str = None, collection: str = None, **kwargs
    ):
        """
        Adds a new DatabaseUserRole to user
        """
        role_name = name if name else set_else_none("roleName", kwargs)
        role_database = database if database else set_else_none("databaseName", kwargs)
        role_collection = (
            collection if collection else set_else_none("collectionName", kwargs)
        )
        if not role_database and role_name == "readWriteAnyDatabase":
            role_database = "admin"
        if not role_name or not role_database:
            raise AttributeError(
                "No roleName nor databaseName set for new DatabaseUserRole",
                role_name,
                role_database,
                role_collection,
                kwargs,
            )
        role = DatabaseUserRole(role_name, role_database, role_collection)
        if role not in self.roles:
            self.roles.append(role)

    def add_scope(self, name: str = None, scope_type: str = None, **kwargs):
        """
        Adds a new DatabaseUserRole to user
        """
        _scope_name = name if name else set_else_none("name", kwargs)
        _scope_type = scope_type if scope_type else set_else_none("type", kwargs)
        if not _scope_name or not _scope_type:
            raise AttributeError(
                "Missing scope name or scope type for DatabaseUserScope",
                _scope_name,
                _scope_type,
                kwargs,
            )
        scope = DatabaseUserScope(_scope_name, _scope_type)
        if scope not in self.scopes:
            self.scopes.append(scope)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, secret):
        self._password = secret

    @property
    def model(self):
        self.validate_type()
        content = {
            "databaseName": self._database,
            "awsIAMType": self._aws_iam_type,
            "x509Type": self._x509_type,
            "ldapAuthType": self._ldap_auth_type,
            "roles": [
                role.model for role in self.roles if isinstance(role, DatabaseUserRole)
            ],
            "scopes": [
                scope.model
                for scope in self.scopes
                if isinstance(scope, DatabaseUserScope)
            ],
            "username": self._username,
        }
        if self._password and self._aws_iam_type == "NONE":
            content["password"] = self._password
        return content


class DatabaseUserRole(object):
    """
    Represents a DB User role
    """

    admin_only_roles = [
        "atlasAdmin" "backup",
        "clusterMonitor",
        "readWriteAnyDatabase",
        "readAnyDatabase",
        "killOpSession",
        "enableSharding",
        "dbAdminAnyDatabase",
    ]
    non_admin_roles = ["read", "readWrite", "dbAdmin"]
    collections_only_roles = ["read", "readWrite"]
    predefined_roles = admin_only_roles + non_admin_roles

    def __init__(self, name: str, database: str = None, collection: str = None):
        if (
            name in self.non_admin_roles
            and collection
            and name not in self.collections_only_roles
        ):
            raise ValueError(
                f"Predefined role {name} is not valid for collections. Use one of",
                self.collections_only_roles,
                "or a custom role",
            )
        self.database = database
        self.role_name = name
        self.collection = collection

        if self.role_name in self.admin_only_roles:
            self.database = "admin"
            self.collection = None

    @property
    def model(self):
        """
        Returns dict that is used for API calls related to the user
        """
        content = {"databaseName": self.database, "roleName": self.role_name}
        if self.collection:
            content["collectionName"] = self.collection
        return content

    def __eq__(self, other):
        if other.database == self.database and other.role_name == self.role_name:
            return True
        return False


class DatabaseUserScope(object):
    """
    Represents a database user scope
    """

    allowed_scopes = ["CLUSTER", "DATA_LAKE"]

    def __init__(self, scope_name: str, scope_type: str):
        if scope_type not in self.allowed_scopes:
            raise ValueError(
                "scope_type must be one of", self.allowed_scopes, "got", scope_type
            )
        self.name = scope_name
        self.type = scope_type

    def __eq__(self, other):
        if self.name == other.name and self.type == other.type:
            return True
        return False

    def __repr__(self):
        return f"{self.type}::{self.name}"

    @property
    def model(self):
        """
        Returns dict for user API interactions
        """
        content = {"name": self.name, "type": self.type}
        return content
