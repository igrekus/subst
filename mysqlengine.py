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

    def execSimpleQuery(self, string):
        cur = self._connection.cursor()
        cur.execute(string)
        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur.fetchall()

    def fetchDeviceList(self):
        return self.execSimpleQuery("CALL getDeviceList()")

    def fetchSubstMap(self):
        return self.execSimpleQuery("CALL getSubstMap()")

    # def fetchDicts(self, dict_list: list):
    #     print("sqlite engine fetch dicts")
    #     def fetchDict(connection, dict_name: str):
    #         cursor = connection.execute("SELECT " + dict_name + "_id, " + dict_name + "_name"
    #                                     "  FROM " + dict_name + " "
    #                                     " WHERE " + dict_name + "_id > 0")
    #         return cursor.fetchall()
    #
    #     return [fetchDict(self._connection, d) for d in dict_list]
    #
    # def fetchAllPlanRecrods(self):
    #     print("sqlite engine fetch raw plan data")
    #     with self._connection:
    #         cursor = self._connection.execute("SELECT main.bill_plan.plan_id"
    #                                           ", main.bill_plan.plan_billRef"
    #                                           ", main.bill_plan.plan_year"
    #                                           ", main.bill_plan.plan_week"
    #                                           ", main.bill_plan.plan_active"
    #                                           "  FROM main.bill_plan"
    #                                           " WHERE main.bill_plan.plan_id > 0")
    #                                           # "   AND main.bill.archive = 0")
    #         # print(cursor.fetchall())
    #         return cursor.fetchall()
    #
    # def shutdownEngine(self):
    #     self._connection.close()
    #
    # def updateBillRecord(self, data: list):
    #     print("sqlite engine update bill record:", data)
    #     with self._connection:
    #         cursor = self._connection.cursor()
    #         cursor.execute("UPDATE bill "
    #                        "   SET bill_date = ?"
    #                        "     , bill_name = ?"
    #                        "     , bill_category = ?"
    #                        "     , bill_vendor = ?"
    #                        "     , bill_cost = ?"
    #                        "     , bill_project = ?"
    #                        "     , bill_desc = ?"
    #                        "     , bill_shipment_time = ?"
    #                        "     , bill_status = ?"
    #                        "     , bill_priority = ?"
    #                        "     , bill_shipment_date = ?"
    #                        "     , bill_shipment_status = ?"
    #                        "     , bill_week = ?"
    #                        "     , bill_note = ?"
    #                        "     , archive = 0"
    #                        " WHERE bill_id = ?", data)
    #
    # def insertBillRecord(self, data: list):
    #     print("sqlite engine insert bill record:", data)
    #     with self._connection:
    #     # try:
    #     #     print("begin insert bill")
    #         cursor = self._connection.execute(" INSERT INTO bill "
    #                                           "      ( bill_date"
    #                                           "      , bill_name"
    #                                           "      , bill_category"
    #                                           "      , bill_vendor"
    #                                           "      , bill_cost"
    #                                           "      , bill_project"
    #                                           "      , bill_desc"
    #                                           "      , bill_shipment_time"
    #                                           "      , bill_status"
    #                                           "      , bill_priority"
    #                                           "      , bill_shipment_date"
    #                                           "      , bill_shipment_status"
    #                                           "      , bill_week"
    #                                           "      , bill_note"
    #                                           "      , archive"
    #                                           "      , bill_id)"
    #                                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)", data[:-1])
    #     # except sqlite3.Error as e:
    #     #     print(e.args[0])
    #     #     print("end insert bill")
    #     rec_id = cursor.lastrowid
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
    #
    # def deleteBillRecord(self, record: BillItem):
    #     # TODO make list of tuples with facade, only write here
    #     print("sqlite engine delete bill record:", record)
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
