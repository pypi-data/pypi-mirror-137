#   Copyright 2016, 2022 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging

from webob.exc import HTTPForbidden

from kallithea.lib import auth_modules, utils2
from kallithea.lib.compat import hybrid_property

log = logging.getLogger(__name__)


class KallitheaAuthPlugin(auth_modules.KallitheaAuthPluginBase):
    def __init__(self):
        pass

    @hybrid_property
    def name(self):
        return "internal"

    @hybrid_property
    def is_container_auth(self):
        return True

    def settings(self):
        return []

    def accepts(self, user, accepts_empty=True):
        return super(KallitheaAuthPlugin, self).accepts(user, accepts_empty=False)

    def get_user(self, username=None, **kwargs):
        remote_user = None

        # Try REMOTE_USER
        environ = kwargs.get('environ')
        if environ:
            remote_user = environ.get('REMOTE_USER')
            if remote_user:
                username = remote_user

        user = super(KallitheaAuthPlugin, self).get_user(username)

        # Container auth attempted, but no matching user, or the user is in-active
        # We do this here to avoid showing the login/forgot-password screens
        if remote_user:
            if not user or not user.active:
                raise HTTPForbidden()

        return user

    def auth(self, userobj, username, password, settings, **kwargs):
        if not userobj:
            log.debug("userobj was: %s skipping", userobj)
            return None

        if userobj.extern_type != self.name:
            log.warning(
                "userobj: %s extern_type mismatch got: `%s` expected: `%s`",
                userobj, userobj.extern_type, self.name)
            return None

        if not username:
            log.debug("Empty username - skipping...")
            return None

        user_data = {
            "username": userobj.username,
            "firstname": userobj.firstname,
            "lastname": userobj.lastname,
            "groups": [],
            "email": userobj.email,
            "admin": userobj.admin,
            "extern_name": userobj.user_id,
        }
        log.debug("user data: %s", user_data)

        # Container Auth
        environ = kwargs.get('environ')
        if environ:
            remote_user = environ.get('REMOTE_USER')
            if userobj.username == remote_user:
                log.info("user %s authenticated via container auth", user_data['username'])
                return user_data

        # Password Auth
        password_match = utils2.check_password(password, userobj.password)
        if userobj.username == username and password_match:
            log.info("user %s authenticated via password auth", user_data['username'])
            return user_data

        log.error("user %s failed to authenticate", username)
        return None

    def get_managed_fields(self):
        return []
