import json
import re
import requests
import os
from urllib.parse import urlparse, urljoin, quote
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import datetime
from .group import Group
from .person import Person, Guest
from .user import User
from .verbose import VERBOSE
from .mailinglist import Mailinglist
from .utils import (
    gen_password,
    check_password,
    to_date,
    format_leitzahl,
    format_notification,
)


class ETH_IAM_conn:
    def __init__(
        self,
        admin_username=None,
        admin_password=None,
        hostname="https://iam.passwort.ethz.ch",
        hostname_new="https://iamws.ethz.ch",
        endpoint_base="/iam-ws-legacy",
        endpoint_base_new="/",
        verify_certificates=True,
    ):
        self._admin_username = admin_username or self.get_username()
        self._admin_password = admin_password or self.get_password()
        self.hostname = hostname
        self.hostname_new = hostname_new
        self.endpoint_base = endpoint_base
        self.endpoint_base_new = endpoint_base_new
        self.verify_certificates = verify_certificates
        self.timeout = (1, 60)
        # self._get_version()

    def get_username(self):
        username = os.environ.get("IAM_USERNAME", "")
        if not username:
            raise ValueError(
                "No IAM_USERNAME env variable found. Please provide an admin username"
            )
        self.username = username

    def get_password(self):
        password = os.environ.get("IAM_PASSWORD", "")
        if not password:
            raise ValueError(
                "No IAM_PASSWORD env variable found. Please provide an admin password"
            )
        self.password = password

    def _get_version(self, endpoint="/version"):
        full_url = urljoin(self.hostname, self.endpoint_base + endpoint)
        resp = requests.get(
            full_url,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        if resp.ok:
            data = json.loads(resp.content.decode())
            """
            {"ETH IAM Web services":{"build date":"2021-01-12 10:23","build version":"2019-1.2"}}'
            """
            self.build_date = data.get("ETH IAM Web services", {}).get("build date")
            self.build_version = data.get("ETH IAM Web services", {}).get(
                "build version"
            )
        else:
            raise ValueError("a general error occured")

    def _delete_request(
        self,
        endpoint,
        success_msg=None,
        not_allowed_msg=None,
        failed_msg=None,
    ):
        full_url = urljoin(self.hostname, self.endpoint_base + endpoint)
        admin_password = self._admin_password
        resp = requests.delete(
            full_url,
            headers={"Accept": "application/json"},
            auth=(self._admin_username, admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        if not success_msg:
            return resp

        if resp.ok:
            if VERBOSE:
                print(success_msg)
        elif resp.status_code == 401:
            if not_allowed_msg is None:
                not_allowed_msg = (
                    f"You are NOT ALLOWED to do a DELETE operation on {endpoint}"
                )
            raise ValueError(not_allowed_msg)
        else:
            data = json.loads(resp.content.decode())
            if not failed_msg:
                failed_msg = f"FAILED to do a DELETE operation on {endpoint}"
            raise ValueError(failed_msg + ": " + data["message"])

    def _post_request(
        self,
        endpoint,
        body,
        hostname=None,
        endpoint_base=None,
        success_msg=None,
        not_allowed_msg=None,
        failed_msg=None,
    ):
        if not hostname:
            hostname = self.hostname
        if not endpoint_base:
            endpoint_base = self.endpoint_base
        elif endpoint_base == "/":
            endpoint_base = ""
        full_url = urljoin(hostname, endpoint_base + endpoint)
        admin_password = self._admin_password
        resp = requests.post(
            full_url,
            json.dumps(body),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            auth=(self._admin_username, admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        if not success_msg:
            return resp

        if resp.ok:
            if VERBOSE:
                print(success_msg)
        elif resp.status_code == 401:
            if not_allowed_msg is None:
                not_allowed_msg = (
                    f"You are NOT ALLOWED to do a POST operation on {endpoint}"
                )
            raise ValueError(not_allowed_msg)
        else:
            data = json.loads(resp.content.decode())
            if not failed_msg:
                failed_msg = f"FAILED to do a POST operation on {endpoint}"
            raise ValueError(failed_msg + ": " + data["message"])

    def _put_request(
        self,
        endpoint,
        body,
        hostname=None,
        endpoint_base=None,
        success_msg=None,
        not_allowed_msg=None,
        failed_msg=None,
    ):
        if not hostname:
            hostname = self.hostname
        if not endpoint_base:
            endpoint_base = self.endpoint_base
        elif endpoint_base == "/":
            endpoint_base = ""
        full_url = urljoin(hostname, endpoint_base + endpoint)
        admin_password = self._admin_password
        resp = requests.put(
            full_url,
            json.dumps(body),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            auth=(self._admin_username, admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        if not success_msg:
            return resp

        if resp.ok:
            if VERBOSE:
                print(success_msg)
        elif resp.status_code == 401:
            if not_allowed_msg is None:
                not_allowed_msg = (
                    f"You are NOT ALLOWED to do a PUT operation on {endpoint}"
                )
            raise ValueError(not_allowed_msg)
        else:
            data = json.loads(resp.content.decode())
            if not failed_msg:
                failed_msg = f"FAILED to do a PUT operation on {endpoint}"
            raise ValueError(failed_msg + ": " + data["message"])

    def _get_request(self, endpoint, hostname=None, endpoint_base=None):
        if not hostname:
            hostname = self.hostname
        if not endpoint_base:
            endpoint_base = self.endpoint_base
        elif endpoint_base == "/":
            endpoint_base = ""
        full_url = urljoin(hostname, endpoint_base + endpoint)
        admin_password = self._admin_password
        resp = requests.get(
            full_url,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=(self._admin_username, admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def new_person(self, firstname, lastname):
        raise Exception("not implemented yet")
        return Person(conn=self, firstname=firstname, lastname=lastname)

    def get_request(self, endpoint, hostname=None, endpoint_base=None):
        resp = self._get_request(
            endpoint=endpoint, hostname=hostname, endpoint_base=endpoint_base
        )
        if resp.ok:
            data = json.loads(resp.content.decode())
            return data
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        elif resp.status_code == 404:
            raise ValueError("No such user/person/group.")
        else:
            print(resp.status_code)
            try:
                data = json.loads(resp.content.decode())
            except json.decoder.JSONDecodeError:
                raise ValueError(f"received http status: {resp.status_code}")

    def get_person(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = "/usermgr/person/{}".format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = "/usermgr/person?{}".format(args)
        else:
            raise ValueError("please provide an identifier")

        data = self.get_request(endpoint)
        return Person(conn=self, data=data)

    def get_user(self, identifier):
        endpoint = "/usermgr/user/{}".format(identifier)
        data = self.get_request(endpoint=endpoint)
        return User(conn=self, data=data)

    def get_guest(self, username: str) -> Guest:
        data = self.get_request(
            f"/guests/{username}",
            hostname=self.hostname_new,
            endpoint_base=self.endpoint_base_new,
        )
        return Guest(conn=self, data=data)

    def extend_guest(self, username: str, endDate=None, months=None) -> Guest:
        if endDate:
            endDate = to_date(endDate)
        elif months:
            today = date.today()
            endDate = today + relativedelta(months=int(months))
        else:
            today = date.today()
            endDate = today + relativedelta(months=12)
        body = {"endDate": endDate.strftime("%d.%m.%Y")}

        endpoint = f"/guests/{username}"
        resp = self._put_request(
            endpoint,
            body,
            hostname=self.hostname_new,
            endpoint_base=self.endpoint_base_new,
        )
        if resp.ok:
            return Guest(conn=self, data=json.loads(resp.content.decode()))
        else:
            raise ValueError(f"ERROR: {resp.status_code}: {resp.content.decode()}")

    def update_guest(
        self,
        username,
        host=None,
        respAdminRole=None,
        description=None,
        guestTechnicalContact=None,
        notification=None,
        hostOrg=None,
        startDate=None,
        endDate=None,
    ):
        body = {"username": username}
        if host:
            body["host"] = host
        if respAdminRole:
            body["respAdminRole"] = respAdminRole
        if description:
            body["description"] = description
        if guestTechnicalContact:
            body["guestTechnicalContact"] = guestTechnicalContact
        if notification:
            notification = format_notification(notification)
            body["notification"] = notification
        if hostOrg:
            body["hostOrg"] = hostOrg
        if startDate:
            body["startDate"] = startDate
        if endDate:
            body["endDate"] = endDate

        guest = Guest(conn=self, data=body, is_new=False)
        guest.save()
        return guest

    def new_guest(
        self,
        firstName: str,
        lastName: str,
        mail: str,
        host: str,
        respAdminRole: str,
        description=None,
        dateOfBirth=None,
        guestTechnicalContact=None,
        notification=None,
        hostOrg=None,
        startDate=None,
        endDate=None,
        salutation=None,
        ahvNo=None,
        addressLine1=None,
        addressLine2=None,
        addressLine3=None,
        postCode=None,
        place=None,
        countryName=None,
    ):
        if description is None:
            description = f"guest of {host}"
        if dateOfBirth is None:
            dateOfBirth = date(2000, date.today().month, date.today().day)
        else:
            dateOfBirth = to_date(dateOfBirth)
        if startDate is None:
            startDate = date.today()
        else:
            startDate = to_date(startDate)
        if endDate:
            endDate = to_date(endDate)
        else:
            endDate = startDate + relativedelta(months=12)

        if (endDate - startDate).days > 365:
            raise ValueError(
                "Difference between endDate and startDate is more than one year."
            )

        host_person = self.get_person(host)
        if not host_person:
            user = self.get_user(host)
            host_person = self.get_person(user["npid"])
        if not host_person:
            print(f"no such host: {host}")

        if hostOrg is None:
            try:
                for perskat in host_person["perskats"]:
                    if perskat["perskat"] == "Mitarbeiter":
                        hostOrg = perskat["leitzahl"]
                        break
            except Exception:
                pass
        if hostOrg is None:
            raise ValueError(
                "no organization leitzahl for host found. Please provide the hostOrg parameter."
            )
        if guestTechnicalContact is None:
            # import pdb; pdb.set_trace()
            try:
                guestTechnicalContact = host_person["email"]
            except Exception:
                pass
            if not guestTechnicalContact:
                raise ValueError("no mail for guestTechnicalContact found.")
        if notification is None:
            notification = "gh"
        else:
            notification = format_notification(notification)

        body = {
            "firstName": firstName,
            "lastName": lastName,
            "mail": mail,
            "host": host,
            "respAdminRole": respAdminRole,
            "description": description,
            "dateOfBirth": dateOfBirth,
            "guestTechnicalContact": guestTechnicalContact,
            "notification": notification,
            "hostOrg": hostOrg,
            "startDate": startDate,
            "endDate": endDate,
            "salutation": salutation,
            "ahvNo": ahvNo,
            "addressLine1": addressLine1,
            "addressLine2": addressLine2,
            "addressLine3": addressLine3,
            "postCode": postCode,
            "place": place,
            "countryName": countryName,
        }
        guest = Guest(conn=self, data=body, is_new=True)
        return guest

    def new_group(self, name, description, admingroup, targets, members=None):
        """
        name=<Group Name>
        description=<what is the purpose of this group>
        admingroup=<Admin Group>
        targets=['AD', 'LDAPS'] -- specify at least one target system
        members=['username1', 'username2']
        """
        if members is None:
            members = []

        endpoint = "/groupmgr/group"
        body = {
            "name": name,
            "description": description,
            "admingroup": admingroup,
            "targets": targets,
            "members": members,
        }
        resp = self._post_request(endpoint, body)
        if resp.ok:
            data = json.loads(resp.content.decode())
            if VERBOSE:
                print("new group {} was successfully created".format(name))
            return Group(conn=self, data=data)
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])

    def new_group2(self, name, admingroup, description=None, targets=None):
        """Create a new group, using the new iamws endpoint"""

        if targets is None:
            targets = []
        body = {
            "name": name,
            "description": description,
            "admingroup": admingroup,
            "targets": targets,
        }
        endpoint = "/groups"
        resp = self._post_request(
            endpoint=endpoint,
            endpoint_base=self.endpoint_base_new,
            body=body,
            hostname=self.hostname_new,
        )
        if resp.ok:
            data = json.loads(resp.content.decode())
            if VERBOSE:
                print("new group {} was successfully created".format(name))
            return Group(conn=self, data=data)
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        elif resp.status_code == 404:
            raise ValueError(f"Admingroup {admingroup} not found.")
        elif resp.status_code == 409:
            raise ValueError(f"Suuch a group already exists.")
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])

    def del_group(self, name):
        """Deletes a group and removes it from all its target systems."""
        endpoint = "/groupmgr/group/{}".format(name)
        resp = self._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("group {} was successfully deleted".format(name))
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])

    def get_groups(self, **kwargs):
        """
        agroup=<Admin Group>  -- Get all groups of a given admin group
        name=group_name*      -- all groups starting with «group_name*»
        """
        if kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = "/groupmgr/groups?{}".format(args)
        else:
            raise ValueError("please provide a name or agroup parameter (or both)")

        data = self.get_request(endpoint)
        groups = []
        for item in data:
            groups.append(Group(conn=self, data=item))
        return groups

    def get_group(self, identifier=None):
        if identifier is not None:

            if re.search(r"^\d+$", str(identifier)):
                # we searched for a gidNumber
                groups = self.get_groups(gidNumber=identifier)
                if len(groups) == 1:
                    return groups[0]
                else:
                    raise ValueError(
                        "No group found with gidNumber={}".format(identifier)
                    )
            else:
                endpoint = "/groupmgr/group/{}".format(identifier)
        else:
            raise ValueError("please provide an identifier")
        data = self.get_request(endpoint)
        return Group(conn=self, data=data)

    def get_mailinglist(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = "/mailinglists/{}".format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = "/mailinglists/?{}".format(args)
        else:
            raise ValueError("please provide an identifier")
        data = self.get_request(endpoint)
        return Mailinglist(conn=self, data=data)
