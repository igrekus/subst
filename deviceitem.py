import const


class DeviceItem:
    # TODO: make DB-aware orm?
    # TODO: make properties
    def __init__(self, id_=None, name=None, vendor=None, devtype=None, desc=None, spec=None, tags=None, origin=None):
        self.item_id = id_
        self.item_name = name
        self.item_vendor = vendor
        self.item_devtype = devtype
        self.item_desc = desc
        self.item_spec = spec
        self.item_tags = tags
        self.item_origin = origin

    def __str__(self):
        return "DeviceItem(" + "id:" + str(self.item_id) + " " \
               + "name:" + str(self.item_name) + " " \
               + "vend:" + str(self.item_vendor) + " " \
               + "type:" + str(self.item_devtype) + " " \
               + "desc:" + str(self.item_desc) + " " \
               + "spec:" + str(self.item_spec) + " " \
               + "tags:" + str(self.item_tags) + " " \
               + "orig:" + str(self.item_origin) + ")"

    @classmethod
    def fromSqlTuple(cls, sql_tuple):
        return cls(id_=sql_tuple[0],
                   name=sql_tuple[1],
                   vendor=sql_tuple[2],
                   devtype=sql_tuple[3],
                   desc=sql_tuple[4],
                   spec=sql_tuple[5],
                   tags=sql_tuple[6],
                   origin=sql_tuple[7])

    def toTuple(self):
        return tuple([self.item_name,
                      self.item_vendor,
                      self.item_devtype,
                      self.item_desc,
                      self.item_spec,
                      self.item_tags,
                      self.item_origin,
                      self.item_id])
