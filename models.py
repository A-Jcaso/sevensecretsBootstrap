
class Services:
    def __init__(self, id,name,description,image,detail):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.detail = detail


    @staticmethod
    def get_all(conn):
        sql = "SELECT * FROM services;"
        cursor = conn.cursor()
        datos = cursor.execute(sql)
        services = []
        for row in datos.fetchall():
            services.append(
                Services(row[0], row[1], row[2], row[3], row[4])
            )
        return services