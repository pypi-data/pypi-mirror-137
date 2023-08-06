import mysql.connector
from Shynatime import ShTime
import os


class ShynaDatabase:
    s_time = ShTime.ClassTime()
    database_user = 'pythoqdx_Shyna'
    default_database = 'pythoqdx_Shyna'
    host = os.environ.get('host')
    passwd = os.environ.get('passwd')
    query = ''
    device_id = os.environ.get('device_id')

    def check_connectivity(self):
        status = False
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            if my_db.is_connected():
                status = True
            else:
                status = False
        except Exception as e:
            print(e)
            status = False
        finally:
            if my_db.is_connected():
                my_db.close()
            return status

    def create_insert_update_or_delete(self):
        """ Insert value in database with no return."""
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            my_db.commit()
        except Exception as e:
            print(e)
        finally:
            my_db.close()

    def select_from_table(self):
        """Select all row using the given query and return the result in dictionary format."""
        result = []
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            cursor = my_cursor.fetchall()
            if len(cursor) > 0:
                for row in cursor:
                    result.append(row)
            else:
                result.append('Empty')
        except Exception as e:
            print("Exception is: \n", e)
            result = "Exception"
        finally:
            my_db.close()
            return result

    def set_date_system(self, process_name):
        print("Device_id", self.device_id)
        self.query = "UPDATE last_run_check SET task_date = '" + str(self.s_time.now_date) \
                            + "' , task_time = '" + self.s_time.now_time + "', from_device = '" \
                            + str(self.device_id) + "' WHERE process_name='" + str(process_name) + "'"
        self.create_insert_update_or_delete()

    def insert_or_update_or_delete_with_status(self):
        insert_status = False
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            my_db.commit()
            insert_status = True
        except mysql.connector.Error as err:
            insert_status = False
            print("error number is", err.errno)
        finally:
            my_db.close()
            return insert_status
