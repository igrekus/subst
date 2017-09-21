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
        # try:
            cur = self._connection.cursor()
            cur.execute(string, param)

        # except Exception as e:
        #     print(e)

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

    def fetchDevtypeList(self):
        return self.execSimpleQuery("CALL getDevtypeList()").fetchall()

    def insertDeviceRecord(self, data, mapping):
        print("mysql engine insert device record:", data, mapping)

        q = "CALL insertDevice(%s, %s, %s, %s, %s, %s, %s)"
        # print(q, data[:-1])
        cursor = self.execParametrizedQuery(q, data[:-1])
        rec_id = cursor.fetchone()[0]

        q = "CALL insertMapping(%s, %s)"
        # print(q, (rec_id, mapping,))
        self.execParametrizedQuery(q, (rec_id, mapping, ))

        return rec_id

    def appendDeviceMapping(self, mappings):
        q = "CALL appendDeviceMapping(%s, %s)"
        for m in mappings:
            self.execParametrizedQuery(q, m)

    def updateDeviceRecord(self, item):
        print("mysql engine update device:", item)
        q = "CALL updateDevice(%s, %s, %s, %s, %s, %s, %s, %s)"
        self.execParametrizedQuery(q, item)

    def updateDeviceMappings(self, mappings):
        print("mysql engine update device mappings:", mappings)
        q = "CALL updateDeviceMapping(%s, %s)"
        for m in mappings:
            self.execParametrizedQuery(q, m)

    def deleteDeviceRecord(self, item):
        print("mysql engine delete device:", item)
        q = "CALL deleteDevice(%s)"
        self.execParametrizedQuery(q, item[-1])

    def insertVendorRecord(self, data: list):
        print("mysql engine insert vendor record", data)
        q = "CALL insertVendorRecord(%s, %s)"
        # print(q, data)
        cursor = self.execParametrizedQuery(q, data)
        rec_id = cursor.fetchone()[0]
        return rec_id

    def insertDictRecord(self, dictName, data):
        print("mysql engine insert dict record:", dictName, data)
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute(" INSERT INTO " + dictName +
                           "      (" + dictName + "_id" +
                           "      , " + dictName + "_name" + ")"
                           " VALUES (NULL, %s)", data)
            rec_id = cursor.lastrowid
        return rec_id

    def updateDictRecord(self, dictName, data):
        print("mysql engine update dict record:", dictName, data)
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute(" UPDATE " + dictName +
                           "    SET " + dictName + "_name = %s" +
                           "  WHERE " + dictName + "_id = %s", data)

    def deleteDictRecord(self, dictName, data):
        print("mysql engine delete dict record:", dictName, data)
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute(" DELETE "
                           "   FROM " + dictName +
                           "  WHERE " + dictName + "_id = %s", data)

    def checkDictRef(self, dictName, data):
        print("mysql engine check dict reference:", dictName, data)
        q = "CALL check" + dictName + "Ref(%s)"
        cur = self.execParametrizedQuery(q, (data, ))
        return bool(cur.fetchone()[0])
