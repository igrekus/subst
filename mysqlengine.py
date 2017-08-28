# from billitem import BillItem
import pymysql
from PyQt5.QtCore import QObject


class MysqlEngine(QObject):
    def __init__(self, parent=None):
        super(MysqlEngine, self).__init__(parent)

        # TODO make properties
        self.engineType = "mysql"
        self._connection = None

    def connectToDatabase(self):
        try:
            f = open("settings.ini")
        except IOError:
            return False, str("Settings.ini not found.")

        lines = f.readlines()
        f.close()

        settings = dict()
        for s in lines:
            # print(s)
            if s.strip() and s[0] != "#":
                sett = s.strip().split("=")
                settings[sett[0]] = sett[1]
            else:
                continue

        try:
            self._connection = pymysql.connect(host=settings['host'],
                                               port=int(settings['port']),
                                               user=settings['username'],
                                               passwd=settings['password'],
                                               db=settings['database'],
                                               charset='utf8mb4')
        except pymysql.MySQLError as e:
            return False, str("DB error: " + str(e.args[0]) + " " + e.args[1])

        return True, "connection established"

    def initEngine(self):
        print("init mysql engine")
        ok, err = self.connectToDatabase()
        print("init", ok, err)

    def execSimpleQuery(self, string):
        with self._connection:
            cur = self._connection.cursor()
            cur.execute(string)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execParametrizedQuery(self, string, param):
        with self._connection:
            cur = self._connection.cursor()
            cur.execute(string, param)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execBulkQuery(self, string, paramlist):
        with self._connection:
            cur = self._connection.cursor()
            cur.executemany(string, paramlist)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def fetchDeviceList(self):
        return self.execSimpleQuery("CALL getDeviceList()").fetchall()

    def fetchSubstMap(self):
        return self.execSimpleQuery("CALL getSubstMap()").fetchall()

    def fetchVendorList(self):
        return self.execSimpleQuery("CAll getVendorList()").fetchall()

    def insertDeviceRecord(self, data, mapping):
        print("mysql engine insert device record:", data, mapping)
        q = " INSERT INTO device" \
            "      ( device_name" \
            "      , device_vendorRef" \
            "      , device_description" \
            "      , device_spec" \
            "      , device_tags" \
            "      , device_origin" \
            "      , archive" \
            "      , device_id)" \
            " VALUES (?, ?, ?, ?, ?, ?, 0, NULL)"
        print(q, [data[:-1]], mapping)

        # cursor = self.execParametrizedQuery(q, data[:-1])
        # rec_id = cursor.lastrowid
        rec_id = 100
        subs = [(rec_id, m) for m in mapping]
        print(subs)

    #     # print("begin insert plan")
    #     cursor = self._connection.execute(" INSERT INTO bill_plan"
    #                                       "           ( plan_id"
    #                                       "           , plan_billRef"
    #                                       "           , plan_year"
    #                                       "           , plan_week"
    #                                       "           , plan_active)"
    #                                       "      VALUES (NULL, ?, 0, 0, 0)", (rec_id, ))
    #         # print("end insert plan")
    #     return rec_id

    def updateDeviceRecord(self, item, mapping):
        print("mysql engine update device:", item)

    def deleteDeviceRecord(self, item):
        print("mysql engine delete device:", item)
    #     with self._connection:
    #         cursor = self._connection.cursor()
    #         cursor.execute("UPDATE bill"
    #                        "   SET archive = 1 "
    #                        " WHERE bill_id = ?", (record.item_id, ))
    #

    # def updatePlanData(self, data):
    #     # TODO error handling
    #     print("sqlite engine update plan data...")
    #     with self._connection:
    #         cursor = self._connection.cursor()
    #         cursor.executemany("UPDATE bill_plan"
    #                            "   SET plan_year = ? "
    #                            "     , plan_week = ? "
    #                            "     , plan_active = ?"
    #                            " WHERE plan_billRef = ?", data)
    #     print("...update end")
    #     return True
    #
    # def insertDictRecord(self, dictName, data):
    #     print("sqlite engine insert dict record:", dictName, data)
    #
    #     with self._connection:
    #         cursor = self._connection.execute(" INSERT INTO " + dictName +
    #                                           "      (" + dictName + "_id" +
    #                                           "      , " + dictName + "_name" + ")"
    #                                           " VALUES (NULL, ?)", data)
    #         rec_id = cursor.lastrowid
    #
    #     return rec_id
    #
    # def updateDictRecord(self, dictName, data):
    #     print("sqlite engine update dict record:", dictName, data)
    #
    #     with self._connection:
    #         cursor = self._connection.execute(" UPDATE " + dictName +
    #                                           "    SET " + dictName + "_name = ?" +
    #                                           "  WHERE " + dictName + "_id = ?", data)
    #
    # def deleteDictRecord(self, dictName, data):
    #     print("sqlite engine delete dict record:", dictName, data)
    #
    #     with self._connection:
    #         cursor = self._connection.execute(" DELETE "
    #                                           "   FROM " + dictName +
    #                                           "  WHERE " + dictName + "_id = ?", data)
