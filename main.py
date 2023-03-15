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
        self.add_product_window.geometry("500x500")

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
        self.valid_button = tk.Button(self.add_product_window, text="OK")
        self.valid_button.config(command= self.add_product_sql)
        self.state1 = [self.title_name, self.input_name, self.title_description,self.input_description, self.title_prix, self.input_prix, self.title_quantite, self.input_quantite, self.title_categorie, self.input_categorie, self.valid_button]

        for element in self.state1:
            element.pack()

    def add_product_sql(self):
        self.stock.add_product(self.input_name.get(), self.input_description.get(), self.input_prix.get(), self.input_quantite.get(), self.input_categorie.get())
        
        self.render_tree()
        self.add_product_window.destroy()


    def del_product_command(self):
        pass

    def mod_product_command(self):
        self.reset_screen()
        self.state = 3

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





