import sqlitedict
from .file_watcher import watch_file_change


init_data={
    "*":{
        "admin":{
            "password":"admin",
            "roles":["admin"],
        }
    },
    "/u1":{
        "u1":{
            "password":"u1"
        }
    },
    "/u2":{
        "u2": {
            "password":"u2"
        }
    },
    "/assets": True,
    "/:dir_browser": True
}


class RealAccessService:
    def __init__(self,data_source):
        self.data_source=data_source
        self.data_dict = self.load_from_disk()
        self.data_dict.update(init_data)
        watch_file_change(data_source,self.load_from_disk)
    def load_from_disk(self):
        self.data_dict=sqlitedict.SqliteDict(self.data_source, autocommit=True)
        return self.data_dict
    def get(self,realm):
        res=self.data_dict.get(realm)
        return res
    def get_realm_access_entry(self,realm,user_name=None):
        realm_entry = self.data_dict.get(realm)
        if realm_entry is None:
            realm_entry = self.data_dict.get("*")
        if user_name is None or realm_entry is None:
            return realm_entry
        return realm_entry.get(user_name)