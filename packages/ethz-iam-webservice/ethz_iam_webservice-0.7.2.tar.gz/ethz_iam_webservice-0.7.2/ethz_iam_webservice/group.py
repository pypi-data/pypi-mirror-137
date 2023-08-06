import os
import json

from .verbose import VERBOSE
from .utils import to_date

class Group:
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        self.name = None
        if data:
            data["cre_date"] = to_date(data["cre_date"]).strftime("%Y-%m-%d")
            data["mod_date"] = to_date(data["mod_date"]).strftime("%Y-%m-%d")
            for key in data:
                setattr(self, key, data[key])

    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))

    def set_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(members, action="", mess="Members group {} set")

    def add_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(
            members, action="add_forgiving", mess="Added members to group {}"
        )

    def del_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(members, action="del", mess="Removed members from group {}")

    def _to_from_group(self, members, action="add", mess="{}"):
        endpoint = "/groupmgr/group/{}/members/{}".format(self.name, action)
        resp = self.conn._put_request(endpoint, members)
        if resp.ok:
            if VERBOSE:
                print(mess.format(self.name))
            self.data = json.loads(resp.content.decode())
            self.members = self.data["members"]
            self.targets = self.data["targets"]
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])

    def delete(self):
        endpoint = "/groupmgr/group/{}".format(self.name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("Group {} deleted.".format(self.name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])
