from database.DB_connect import DBConnect
from model.state import State


class DAO:
    @staticmethod
    def read_all_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct YEAR(s_datetime) as year FROM sighting """

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct shape 
                    FROM sighting 
                    WHERE shape !='' """

        cursor.execute(query)

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_states():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id,name,lat,lng,neighbors
                    FROM state
                    """

        cursor.execute(query)

        for row in cursor:
            result[row['id']]=(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_avvistamenti():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  st.id, YEAR(s_datetime) AS year, si.shape, count(*) as peso
                            FROM state st, sighting si
                            WHERE st.id = si.state
                            group by st.id, year, si.shape
                    
                            """

        cursor.execute(query)

        for row in cursor:
            result[(row['id'],row['year'], row['shape'])] = (row['peso'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_negh():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM neighbor
                    WHERE state1<state2
                        """

        cursor.execute(query)

        for row in cursor:
            result.append([row['state1'],row['state2']])

        cursor.close()
        conn.close()
        return result