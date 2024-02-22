"""
Fernando Rivera #34
12 BTP
Main File
https://www.asterki.com
"""

import sqlite3
import os


class VideoClubManagementSystem:
    def __init__(self):
        # Conectarse a la base de datos
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()

    def menu(self):
        while True:  # Mostrar un menú que se repite hasta que el usuario decida salir
            print("1. Añadir Película")
            print("2. Borrar Película")
            print("3. Actualizar Película")
            print("4. Mostrar Todas Las Películas")
            print("5. Buscar Películas")
            print("6. Mostrar películas con <5 stock")
            print("7. Salir")
            choice = int(input("Ingrese su opción:: "))

            self.clean_screen()

            # Añadir película
            if choice == 1:
                while True:
                    name = input("Ingrese el nombre de la película: ")
                    genre = input("Ingrese el género de la película: ")
                    year = int(input("Ingrese el año de la película:"))
                    price = int(input("Ingrese el precio de la película: "))
                    stock = int(input("Ingrese el stock de la película: "))

                    # Llamar a la función para añadir la película
                    self.add_movie(name, genre, year, price, stock)
                    print("Película añadida exitosamente")

                    # Permitir al usuario añadir otra película
                    a = input("¿Desea añadir otra película? (s/n): ")
                    if a.lower() == "n":
                        break
                    else:
                        self.clean_screen()
                        continue

            # Eliminar película
            elif choice == 2:
                while True:
                    # Pedir al usuario el id de la película a eliminar
                    movie_id = None
                    knows = input("Conoces el id de la película? (s/n): ")

                    if knows.lower() == "s":
                        movie_id = int(input("Ingrese el id de la película: "))
                    else:
                        # En caso de que el usuario no sepa el id, buscar la película por otro campo
                        field = input("Ingrese el campo a buscar (name, genre, year, price, stock): ")
                        name = input("Ingrese el valor a buscar dado ese campo: ")
                        data = self.search_movie(field, name)
                        for i in data:
                            print(i)

                        # Preguntar al usuario si la película que quiere eliminar está en la lista
                        there = input("Encontraste el id de la película (s/n): ")
                        if there.lower() == "s":
                            movie_id = int(input("Ingrese el id de la película: "))

                    if movie_id is not None:
                        # Si se pudo encontrar el id, se llama a la función para eliminar la película
                        self.delete_movie(movie_id)
                        print("Película eliminada exitosamente")
                    else:
                        print("Película no encontrada")

                    a = input("Quieres eliminar otra película (s/n): ")
                    if a.lower() == "n":
                        break
                    else:
                        self.clean_screen()
                        continue

            # Actualizar película
            elif choice == 3:
                while True:
                    movie_id = None
                    knows = input("Do you know the id of the movie? (y/n): ")

                    if knows.lower() == "y":
                        movie_id = int(input("Enter the id of the movie: "))
                    else:
                        field = input("Ingrese el campo a buscar (name, genre, year, price, stock): ")
                        name = input("Ingrese el valor a buscar dado ese campo: ")
                        data = self.search_movie(field, name)
                        for i in data:
                            print(i)

                        there = input("Encontraste el id de la película (s/n): ")
                        if there.lower() == "s":
                            movie_id = int(input("Ingrese el id de la película: "))

                    if movie_id is not None:
                        # Imprimir los valores actuales de la película
                        data = self.search_movie("id", movie_id)
                        for i in data:
                            print(i)

                        name = input("Ingrese el nuevo nombre de la película: ")
                        genre = input("Ingrese el nuevo género de la película: ")
                        year = int(input("Ingrese el nuevo año de la película: "))
                        price = int(input("Ingrese el nuevo precio de la película: "))
                        stock = int(input("Ingrese el nuevo stock de la película: "))
                        self.update_movie(id, name, genre, year, price, stock)

                        print("Película actualizada exitosamente")
                    else:
                        print("Película no encontrada")

                    a = input("¿Desea actualizar otra película? (s/n): ")
                    if a.lower() == "n":
                        break
                    else:
                        self.clean_screen()
                        continue


            # Mostrar todas las películas
            elif choice == 4:
                data = self.show_movies()
                for i in data:
                    print(i)

            # Buscar películas por campo
            elif choice == 5:
                while True:
                    field = input("Ingrese el campo a buscar (name, genre, year, price, stock): ")
                    name = input("Ingrese el valor a buscar dado ese campo: ")
                    data = self.search_movie(field, name)
                    for i in data:
                        print(i)

                    a = input("¿Desea buscar otra película? (s/n): ")
                    if a.lower() == "n":
                        break
                    else:
                        self.clean_screen()
                        continue

            # Mostrar películas con stock < 5
            elif choice == 6:
                data = self.show_movies()
                for i in data:
                    if i[-1] < 5:
                        print(i)

            # Salir del programa
            if choice == 7:
                self.__del__()
                break

            input("Press Enter to continue...")

    def clean_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla usando el comando cls o clear

    def create_table(self):
        # Crea la tabla si no existe
        self.cursor.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, name TEXT, genre TEXT, "
                            "year INTEGER, price INTEGER, stock INTEGER)")
        self.con.commit()

    def add_movie(self, name, genre, year, price, stock):
        # Añadir una película a la base de datos dado su nombre, género, año, precio y stock
        self.cursor.execute("INSERT INTO movies (name, genre, year, price, stock) VALUES (?, ?, ?, ?, ?)",
                            (name, genre, year, price, stock))
        self.con.commit()

    def delete_movie(self, id):
        # Elimina una película de la base de datos dado su id
        self.cursor.execute("DELETE FROM movies WHERE id=?", (id,))
        self.con.commit()

    def update_movie(self, id, name, genre, year, price, stock):
        # Actualiza una película de la base de datos dado su id
        self.cursor.execute("UPDATE movies SET name=?, genre=?, year=?, price=?, stock=? WHERE id=?",
                            (name, genre, year, price, stock, id))
        self.con.commit()

    def show_movies(self):
        # Devuelve todas las películas de la base de datos
        self.cursor.execute("SELECT * FROM movies")
        data = self.cursor.fetchall()
        return data

    def search_movie(self, field, name):
        # Busca una película en la base de datos dado un campo y un valor
        self.cursor.execute(f"SELECT * FROM movies WHERE {field}=?", (name,))
        data = self.cursor.fetchall()
        return data

    def __del__(self):
        try:
            self.con.close()
            print("Conexión cerrada exitosamente")
        except Exception as e:
            print("Error al intentar cerrar la conexión:", e)

        print("Gracias por usar este sistema")


if __name__ == "__main__":
    v = VideoClubManagementSystem()
    v.menu()
