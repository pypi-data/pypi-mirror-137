# -*- coding: utf-8 -*-
# (c) 2009-2022 Martin Wendt and contributors; see WsgiDAV https://github.com/mar10/wsgidav
# Original PyFileServer (c) 2005 Ho Chun Wei.
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php
"""
Implementation of a domain controller that uses realm/user_name/password mappings
from the configuration file and uses the share path as realm name.

user_mapping is defined a follows::

    simple_dc: {
        user_mapping = {
            "realm1": {
                "John Smith": {
                    "password": "YouNeverGuessMe",
                },
                "Dan Brown": {
                    "password": "DontGuessMeEither",
                    "roles": ["editor"]
                }
            },
            "realm2": {
                ...
            }
        },
    }

The "*" pseudo-share is used to pass a default definition::

    user_mapping = {
        "*": {  // every share except for 'realm2'
            "Dan Brown": {
                "password": "DontGuessMeEither",
                "roles": ["editor"]
            }
        },
        "realm2": {
            ...
        }
    },

A share (even the "*" pseudo-share) can be set to True to allow anonymous access::

    user_mapping = {
        "*": {
            "Dan Brown": {
                "password": "DontGuessMeEither",
                "roles": ["editor"]
            },
        },
        "realm2": True
    },

The SimpleDomainController fulfills the requirements of a DomainController as
used for authentication with http_authenticator.HTTPAuthenticator for the
WsgiDAV application.

Domain Controllers must provide the methods as described in
DomainControllerBase_

.. _DomainControllerBase : dc/base_dc.py

"""
from cloudos_webdav_server.wsgidav import util
from cloudos_webdav_server.wsgidav.dc.base_dc import BaseDomainController
from .services import RealAccessService

__docformat__ = "reStructuredText"

_logger = util.get_module_logger(__name__)


class CloudosDomainController(BaseDomainController):
    def __init__(self, wsgidav_app, config):
        super().__init__(wsgidav_app, config)

        dc_conf = util.get_dict_value(config, "cloudos_dc")
        self.realm_access_service = RealAccessService(dc_conf.get("data_source"))

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def _get_realm_user_entry(self, realm, user_name=None):
        """Return the matching user_map entry (falling back to default '*' if any)."""
        # print(self.user_map)
        realm_entry = self.realm_access_service.get(realm)
        if realm_entry is None:
            realm_entry = self.realm_access_service.get("*")
        if user_name is None or realm_entry is None:
            return realm_entry
        return realm_entry.get(user_name)

    def get_domain_realm(self, path_info, environ):
        """Resolve a relative url to the appropriate realm name."""
        print("get_domain_realm ",path_info)
        path_info=path_info.strip('/')
        if not path_info:
            return "/"
        else:
            return "/"+path_info.split("/")[0]

    def require_authentication(self, realm, environ):
        """Return True if this realm requires authentication (grant anonymous access otherwise)."""

        realm_entry = self._get_realm_user_entry(realm)
        print("require_authentication ", realm, "realm_entry:",realm_entry)
        if realm_entry is None:
            _logger.error(
                'Missing configuration simple_dc.user_mapping["{}"] (or "*"): '
                "realm is not accessible!".format(realm)
            )
        if realm_entry is True:
            return  False

        return  realm!="/:public"
        # realm_entry = self._get_realm_entry(realm)
        # if realm_entry is None:
        #     _logger.error(
        #         'Missing configuration simple_dc.user_mapping["{}"] (or "*"): '
        #         "realm is not accessible!".format(realm)
        #     )
        # return realm_entry is not True

    def basic_auth_user(self, realm, user_name, password, environ):
        """Returns True if this user_name/password pair is valid for the realm,
        False otherwise. Used for basic authentication."""
        user = self._get_realm_user_entry(realm,user_name)
        if user is not None and password == user.get("password"):
            environ["wsgidav.auth.roles"] = user.get("roles", [])
            return True
        return False

    def supports_http_digest_auth(self):
        # We have access to a plaintext password (or stored hash)
        return True

    def digest_auth_user(self, realm, user_name, environ):
        """Computes digest hash A1 part."""
        user = self._get_realm_user_entry(realm, user_name)
        if user is None:
            return False
        password = user.get("password")
        environ["wsgidav.auth.roles"] = user.get("roles", [])
        # print(dict(realm=realm,user_name=user_name,user=user))
        return self._compute_http_digest_a1(realm, user_name, password)
