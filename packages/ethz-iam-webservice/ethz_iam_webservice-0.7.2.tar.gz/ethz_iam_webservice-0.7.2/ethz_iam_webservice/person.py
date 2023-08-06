import copy
import json
import os

from .utils import (
    check_password,
    format_leitzahl,
    format_notification,
    gen_password,
    to_date,
)
from .verbose import VERBOSE

guest_properties_required = [
    "firstname",
    "lastname",
    "mail",
    "description",
    "dateofbirth",
    "hostorg",
    "host",
    "technicalcontact",
    "admingroup",
    "notification",
    "startdate",
    "enddate",
]

guest_properties_optional = [
    "title",
    "salutation",
    "ahvNo",
    "addressLine1",
    "addressLine2",
    "addressLine3",
    "postCode",
    "place",
    "countryName",
]

guest_properties_update = [
    "description",
    "hostOrg",
    "host",
    "guestTechnicalContact",
    "endDate",
    "notification",
    "respAdminRole",
    "deactivationStartDate",
    "deactivationEndDate",
]


class Person:
    def __init__(self, conn, data=None, **keyvals):
        """create or update a new (guest) identity in IAM.
        Following properties are required:
        - firstname,
        - lastname,
        - mail,
        - description,
        - dateofbirth,
        - hostorg,
        - host,
        - technicalcontact,
        - admingroup,
        - notification,
        - startdate,
        - enddate

        The following properties are optional:
        - title

        """
        self.conn = conn
        self.data = data
        self.npid = None
        self.firstname = None
        self.familyname = None
        self.email = None
        self.description = None
        self.date_of_birth = None
        self.host_organization = None
        self.host_npid = None
        self.mail_technical_contact = None
        self.admin_group = None
        self.valid_from = None
        self.valid_until = None
        self.title = None

        if data:
            self.is_new = False
            for perskat in data.get("perskats", []):
                perskat["von"] = to_date(perskat["von"]).strftime("%Y-%m-%d")
                perskat["bis"] = to_date(perskat["bis"]).strftime("%Y-%m-%d")

            for key in data:
                setattr(self, key, data[key])
        else:
            self.is_new = True
            for key in guest_properties_required:
                if key in keyvals:
                    setattr(self, key, keyvals[key])
                else:
                    raise ValueError(f"the {key} property is required.")

    def save(self):
        body = {
            key: getattr(self, key, None)
            for key in guest_properties_required + guest_properties_optional
        }
        if self.is_new:
            endpoint = "/usermgr/person/"
            resp = self.conn._post_request(endpoint, body)
            action = "created"
        else:
            endpoint = f"/usermgr/person/{self.npid}"
            resp = self.conn._put_request(endpoint, body)
            action = "updated"

        if resp.ok:
            # TODO: get the new npid from post request?
            if VERBOSE:
                print(
                    f"Person {self.firstname} {self.familyname} was successfully {action}"
                )
        elif resp.status_code == 401:
            raise ValueError(
                "the provided admin-username/password is incorrect or you are not allowed to create/update this person"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(f"unable to create/update this person: {data['message']}")

    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))

    def new_user(
        self,
        username,
        password=None,
        firstname=None,
        familyname=None,
        mail=None,
        description=None,
    ):
        if len(username) < 6:
            raise ValueError("Usernames must be 6 chars or longer")
        if password is None:
            password = gen_password()
        elif not check_password(password):
            raise ValueError(
                "the initial password must contain at least Lowercase, uppercase characters and a digit"
            )
        if description is None:
            description = username
        endpoint = "/usermgr/person/{}".format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body)
        if resp.ok:
            user = self.conn.get_user(username)
            user.init_password = password
            if VERBOSE:
                print("new user {} was successfully created".format(username))
            return user
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])


class Guest:
    def __init__(self, conn, data=None, is_new=False):
        self.date_fields = [
            "startDate",
            "endDate",
            "deactivationStartDate",
            "dateOfBirth",
        ]
        self.conn = conn
        self.is_new = is_new
        if data:
            self._set_data(data)

    def _set_data(self, data):
        for key in data:
            if key in self.date_fields:
                d = to_date(data[key])
                data[key] = d
        self.data = data

    def _server_body(self):
        """Transform data to be send to the server"""
        body = copy.deepcopy(self.data)
        for date_field in self.date_fields:
            if date_field in body:
                body[date_field] = body[date_field].strftime("%d.%m.%Y")
        return body

    def _data_formatted(self):
        body = copy.deepcopy(self.data)
        for date_field in self.date_fields:
            if date_field in body:
                body[date_field] = body[date_field].strftime("%Y-%m-%d")
        return body

    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))

    def save(self):
        endpoint = "/guests"
        hostname = self.conn.hostname_new
        endpoint_base = self.conn.endpoint_base_new

        if self.is_new:
            resp = self.conn._post_request(
                endpoint,
                self._server_body(),
                hostname=hostname,
                endpoint_base=endpoint_base,
            )
            if resp.ok:
                guest_info = json.loads(resp.content.decode())
                self._set_data(guest_info)
                if VERBOSE:
                    print(
                        f"Guest successfully created with username: {self.data['username']}"
                    )

        else:
            endpoint += f"/{self.data['username']}"
            resp = self.conn._put_request(
                endpoint,
                self._server_body(),
                hostname=hostname,
                endpoint_base=endpoint_base,
            )
            if resp.ok:
                if VERBOSE:
                    print(f"Guest successfully updated.")
                guest_info = json.loads(resp.content.decode())
                self._set_data(guest_info)

        if resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        elif not resp.ok:
            if resp.content:
                raise ValueError(f"{resp.status_code}: {resp.content}")
            else:
                raise ValueError(f"got status: {resp.status_code}")
