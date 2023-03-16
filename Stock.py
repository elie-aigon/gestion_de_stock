import mysql.connector

class Stock:
    def __init__(self, host, user, password, database):
        self.database = mysql.connector.connect(
            host=str(host),
            user=str(user),
            password=str(password),
            database=str(database),
        )
        self.cursor = self.database.cursor()


    def load_table(self, table):
        self.cursor.execute("SELECT *FROM " + str(table))
        self.results = self.cursor.fetchall()
        return self.results


    def close_connection(self):
        self.database.close()

    def add_product(self, nom, description, prix, quantite, categorie):
        sql = "INSERT produit (id, nom, description, prix, quantite, id_categorie) VALUES(NULL, %s, %s, %s, %s, %s);"
        self.cursor.execute(sql, (nom, description, prix, quantite, categorie))
        self.database.commit()
    

    
    def del_product(self, id):
        sql = "DELETE FROM produit WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.database.commit()

s = Stock("localhost", "root", "root", "boutique")
s.del_product(15)