import tkinter as tk, sys, random, json, mysql.connector
import tkinter.ttk as ttk

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

    def mod_product(self, id, nom, description, prix, quantite, categorie):
        sql = "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE id = %s;"
        self.cursor.execute(sql, (nom, description, prix, quantite, categorie, id,))
        self.database.commit()
        

class Main:
    def __init__(self):
        self.stock = Stock("localhost", "root", "root", "boutique")
        self.window  = tk.Tk()
        self.window.title("Gestion De Stock")
        self.window.geometry("1500x500")
        self.current_screen = []
        self.state = 0
        # state
            # 0 = main window
            # 1 = add produit window
            # 2 = supprimer produit window
            # 3 = mod produit window
            # 4 = import csv window
        # State 1
        self.add_product = tk.Button(self.window, text="Ajouter un produit")
        self.del_product = tk.Button(self.window, text="Supprimer un produit")
        self.mod_product = tk.Button(self.window, text="Modifier un produit")
        self.import_csv = tk.Button(self.window, text="Importer en CSV")
        self.state0 = [self.add_product, self.del_product, self.mod_product, self.import_csv]
        self.tree_produit =  ttk.Treeview(self.window, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
        self.tree_produit.heading("col1", text="ID")
        self.tree_produit.heading("col2", text="Nom")
        self.tree_produit.heading("col3", text="Description")
        self.tree_produit.heading("col4", text="Prix")
        self.tree_produit.heading("col5", text="Quantité")
        self.tree_produit.heading("col6", text="Catégorie")
        self.render_tree()
        self.add_product.config(command=self.add_product_command)
        self.del_product.config(command=self.del_product_command)
        self.mod_product.config(command=self.mod_product_command)
        self.import_csv.config(command=self.import_csv_command)

    def render_tree(self):
        self.tree_produit.delete(*self.tree_produit.get_children())
        for element in self.stock.load_table("produit"):
            self.tree_produit.insert("", "end", values=element)
        
    def add_product_command(self):
        self.add_product_window = tk.Toplevel(self.window)
        self.add_product_window.title("Ajouter un produit")
        self.add_product_window.geometry("200x300")

        self.title_name = tk.Label(self.add_product_window, text="Nom :")
        self.input_name = tk.Entry(self.add_product_window)
        self.title_description = tk.Label(self.add_product_window, text="Description :")
        self.input_description = tk.Entry(self.add_product_window)
        self.title_prix = tk.Label(self.add_product_window, text="Prix :")
        self.input_prix = tk.Entry(self.add_product_window)
        self.title_quantite = tk.Label(self.add_product_window, text="Quantité :")
        self.input_quantite = tk.Entry(self.add_product_window)
        self.title_categorie = tk.Label(self.add_product_window, text="Categorie")
        self.input_categorie = tk.Entry(self.add_product_window)
        self.valid_state1 = tk.Button(self.add_product_window, text="OK")
        self.valid_state1.config(command= self.add_product_sql)
        self.state1 = [self.title_name, self.input_name, self.title_description,self.input_description, self.title_prix, self.input_prix, self.title_quantite, self.input_quantite, self.title_categorie, self.input_categorie, self.valid_state1]
        for element in self.state1:
            element.pack()

    def add_product_sql(self):
        self.stock.add_product(self.input_name.get(), self.input_description.get(), self.input_prix.get(), self.input_quantite.get(), self.input_categorie.get())
        self.render_tree()
        self.add_product_window.destroy()

    def del_product_command(self):
        self.del_product_window = tk.Toplevel(self.window)
        self.del_product_window.title("Supprimer un produit")
        self.del_product_window.geometry("200x100")
        self.aff_id = tk.Label(self.del_product_window, text="ID")
        self.input_id = tk.Entry(self.del_product_window)
        self.valid_state2 = tk.Button(self.del_product_window, text="OK")
        self.valid_state2.config(command=self.del_product_sql)
        self.state2 = [self.aff_id, self.input_id, self.valid_state2]
        for element in self.state2:
            element.pack()

    def del_product_sql(self):
        self.stock.del_product(self.input_id.get())
        self.render_tree()
        self.del_product_window.destroy()

    def mod_product_command(self): 
        self.mod_product_window = tk.Toplevel(self.window)
        self.mod_product_window.title("Modifier un produit")
        self.mod_product_window.geometry("200x300")
        self.aff_id_n3 = tk.Label(self.mod_product_window, text="ID")
        self.input_id_n3 = tk.Entry(self.mod_product_window)
        self.title_name_n3 = tk.Label(self.mod_product_window, text="Nom :")
        self.input_name_n3 = tk.Entry(self.mod_product_window)
        self.title_description_n3 = tk.Label(self.mod_product_window, text="Description :")
        self.input_description_n3 = tk.Entry(self.mod_product_window)
        self.title_prix_n3 = tk.Label(self.mod_product_window, text="Prix :")
        self.input_prix_n3 = tk.Entry(self.mod_product_window)
        self.title_quantite_n3 = tk.Label(self.mod_product_window, text="Quantité :")
        self.input_quantite_n3 = tk.Entry(self.mod_product_window)
        self.title_categorie_n3 = tk.Label(self.mod_product_window, text="Categorie")
        self.input_categorie_n3 = tk.Entry(self.mod_product_window)
        self.valid_state_n3 = tk.Button(self.mod_product_window, text="OK")
        self.valid_state_n3.config(command= self.mod_product_sql)
        self.state3 = [self.aff_id_n3, self.input_id_n3, self.title_name_n3, self.input_name_n3, self.title_description_n3,self.input_description_n3, self.title_prix_n3, self.input_prix_n3, self.title_quantite_n3, self.input_quantite_n3, self.title_categorie_n3, self.input_categorie_n3, self.valid_state_n3]
        for element in self.state3:
            element.pack()

    def mod_product_sql(self):
        self.stock.mod_product(self.input_id_n3.get(), self.input_name_n3.get(), self.input_description_n3.get(), self.input_prix_n3.get(), self.input_quantite_n3.get(), self.input_categorie_n3.get())
        self.render_tree()
        self.mod_product_window.destroy()

    def import_csv_command(self):
        self.reset_screen()
        self.state = 4
    




    def render(self):
        self.current_screen = []
        self.tree_produit.pack()
        self.current_screen.append(self.tree_produit)
        for element in self.state0:
            element.pack()
            self.current_screen.append(element)
        self.window.mainloop()

main = Main()
main.render()
 




