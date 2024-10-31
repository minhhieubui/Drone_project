import mysql.connector

class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = "123456789"
        self._database = "data_login"
        self.con = None
        self.cursor = None

    def connect_db(self):
        # Establish a database connection      (con = db)
        self.con = mysql.connector.connect(
            host = self._host,
            port = self._port,
            database = self._database,
            user = self._user,
            password = self._password
        )
        # Create a cursor for executing SQL queries
        self.cursor = self.con.cursor(dictionary=True)     #(mycursor = db.cursor())


    def add_info(self, qrcode_id, location, quantity, type, status, date ):
        # Connect to the database
        self.connect_db()

        #Construct SQL query for adding information
        sql = f"""
            INSERT INTO qrcodes_info(qrcode, location, quantity, type, status, date)
                VALUES( {qrcode_id},'{location}', '{quantity}', '{type}', '{status}', '{date}');
        """
        try:
            # Execute the SQL query for adding information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E
        finally:
            # Close the database connection
            self.con.close()

    def update_info(self, qrcode_id, location, quantity, type, status, date):
        self.connect_db()
        if self.con is None or self.cursor is None:
            return "Connection failed"
        sql = f"""
            UPDATE qrcodes_info
            SET location='{location}', quantity='{quantity}', type='{type}', status='{status}', date='{date}'
            WHERE qrcode='{qrcode_id}';
        """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            return str(e)
        finally:
            self.con.close()

    def delete_info(self, qrcode_id):
        self.connect_db()
        if self.con is None or self.cursor is None:
            return "Connection failed"
        sql = f"""
            DELETE FROM qrcodes_info WHERE qrcode='{qrcode_id}';
        """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            return str(e)
        finally:
            self.con.close()

    def search_info(self, qrcode_id=None, location=None, quantity=None, type=None, status=None, date=None):
        # Connect to the databse
        self.connect_db()

        condition = ""
        if qrcode_id:
            condition += f"qrcode LIKE '%{qrcode_id}%'"
        else:
            if location:
                if condition:
                    condition += f" and location LIKE '%{location}%'"
                else:
                    condition += f" location LIKE '%{location}%'"

            if quantity:
                if condition:
                    condition += f" and quantity LIKE '%{quantity}%'"
                else:
                    condition += f" quantity LIKE '%{quantity}%'"

            if type:
                if condition:
                    condition += f" and type ='{type}'"
                else:
                    condition += f" type ='{type}'"

            if status:
                if condition:
                    condition += f" and status ='{status}'"
                else:
                    condition += f" status ='{status}'"

            if date:
                if condition:
                    condition += f" and date LIKE '%{date}%'"
                else:
                    condition += f" date LIKE '%{date}%'"

        if condition:
            # Construct SQL query for searching information with conditions
            sql = f"""
                SELECT * FROM qrcodes_info WHERE {condition};
            """
        else:
            # Construct SQL query for searching all information
            sql = f"""
                SELECT * FROM qrcodes_info;
            """
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()

    # def get_all_types(self):
    #     # Connect to the databse
    #     self.connect_db()
    #
    #     # Construct SQL query for searching all information
    #     sql = f"""
    #         SELECT type FROM qrcodes_info GROUP BY type;
    #     """
    #
    #     try:
    #         # Execute the SQL query for searching information
    #         self.cursor.execute(sql)
    #         result = self.cursor.fetchall()
    #         return result
    #
    #     except Exception as E:
    #         # Rollback the transaction in case of an error
    #         self.con.rollback()
    #         return E
    #
    #     finally:
    #         # Close the database connection
    #         self.con.close()

    # def get_all_status(self):
    #     # Connect to the databse
    #     self.connect_db()
    #
    #     # Construct SQL query for searching all information
    #     sql = f"""
    #         SELECT status FROM qrcodes_info GROUP BY status;
    #     """
    #
    #     try:
    #         # Execute the SQL query for searching information
    #         self.cursor.execute(sql)
    #         result = self.cursor.fetchall()
    #         return result
    #
    #     except Exception as E:
    #         # Rollback the transaction in case of an error
    #         self.con.rollback()
    #         return E
    #
    #     finally:
    #         # Close the database connection
    #         self.con.close()

