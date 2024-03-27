import getpass
from prettytable import PrettyTable
import locale
import math

locale.setlocale(locale.LC_ALL, '')

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_after(self, prev_node, data):
        if not prev_node:
            print("Node sebelumnya tidak ditemukan.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key):
        current_node = self.head

        if current_node and current_node.data == key:
            self.head = current_node.next
            current_node = None
            return

        prev_node = None
        while current_node and current_node.data != key:
            prev_node = current_node
            current_node = current_node.next

        if current_node is None:
            print("Data tidak ditemukan.")
            return

        prev_node.next = current_node.next
        current_node = None

    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

    def merge_sort(self, key, reverse=False):
        if not self.head:
            return
        
        data = []
        current_node = self.head
        while current_node:
            data.append(current_node.data)
            current_node = current_node.next

        sorted_data = merge_sort_helper(data, key, reverse)

        self.head = None
        for item in sorted_data:
            self.append(item)

def merge_sort_helper(data, key, reverse=False):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = data[:mid]
    right = data[mid:]

    left = merge_sort_helper(left, key, reverse)
    right = merge_sort_helper(right, key, reverse)

    return merge(left, right, key, reverse)

def merge(left, right, key, reverse):
    result = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):
        if (getattr(left[left_idx], key) < getattr(right[right_idx], key)) ^ reverse:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left_idx < len(left):
        result.extend(left[left_idx:])
    if right_idx < len(right):
        result.extend(right[right_idx:])

    return result

class ActionFigure:
    def __init__(self, name, brand, price, quantity, description=""):
        self.name = name
        self.brand = brand
        self.price = float(price)
        self.quantity = int(quantity)
        self.description = description

    def to_dict(self):
        return {
            "Name": self.name,
            "Brand": self.brand,
            "Price": locale.currency(self.price, grouping=True),
            "Quantity": self.quantity,
            "Description": self.description
        }

class ActionFigureStore:
    def __init__(self):
        self.action_figures = LinkedList()
        self.cart = LinkedList()
        self.balance = 1000000
        self.add_default_action_figures()

    def add_default_action_figures(self):
        default_figures = [
            ActionFigure("Iron Man", "Marvel", 1500000, 10, "Baju besi keren untuk bertarung melawan penjahat."),
            ActionFigure("Batman", "DC", 1200000, 8, "Pahlawan gelap yang melawan kejahatan di Gotham City."),
            ActionFigure("Goku", "Dragon Ball", 1000000, 15, "Pahlawan Saiyan yang bertarung untuk melindungi bumi dari kejahatan.")
        ]
        for figure in default_figures:
            self.action_figures.append(figure)

    def add_action_figure(self, action_figure):
        self.action_figures.append(action_figure)

    def update_action_figure(self, name, field, value):
        current_node = self.action_figures.head
        while current_node:
            if current_node.data.name == name:
                if hasattr(current_node.data, field):
                    if field == "price":
                        current_node.data.price = float(value)
                    elif field == "quantity":
                        current_node.data.quantity = int(value)
                    elif field == "description":
                        current_node.data.description = value
                    print(f"{field} untuk {name} diperbarui.")
                    return
                else:
                    print(f"{field} tidak valid.")
                    return
            current_node = current_node.next
        print(f"{name} tidak ditemukan.")

    def delete_action_figure(self, name):
        current_node = self.action_figures.head
        prev_node = None
        while current_node:
            if current_node.data.name == name:
                if prev_node is None:
                    self.action_figures.head = current_node.next
                else:
                    prev_node.next = current_node.next
                print(f"{name} dihapus dari toko.")
                return
            prev_node = current_node
            current_node = current_node.next
        print(f"{name} tidak ditemukan.")

    def display_action_figures(self):
        current_node = self.action_figures.head
        while current_node:
            print(f"Name: {current_node.data.name}")
            print(f"Brand: {current_node.data.brand}")
            print(f"Price: {current_node.data.price}")
            print(f"Quantity: {current_node.data.quantity}")
            print(f"Description: {current_node.data.description}")
            print("-------------------------")
            current_node = current_node.next

    def search_action_figure(self, key, value):
        current_node = self.action_figures.head
        while current_node:
            if getattr(current_node.data, key) == value:
                print(f"Name: {current_node.data.name}")
                print(f"Brand: {current_node.data.brand}")
                print(f"Price: {current_node.data.price}")
                print(f"Quantity: {current_node.data.quantity}")
                print(f"Description: {current_node.data.description}")
                print("-------------------------")
                return
            current_node = current_node.next
        print(f"{key} dengan nilai {value} tidak ditemukan.")

def admin_login(store):
    username = input("Masukkan username: ")
    password = getpass.getpass("Masukkan password: ")
    if username == "admin" and password == "password":
        print("Login berhasil!")
        admin_menu(store)
    else:
        print("Login gagal. Coba lagi.")

def admin_menu(store):
        while True:
            print("\nPilih tindakan Admin:")
            print("1. Tambah Action Figure")
            print("2. Perbarui Action Figure")
            print("3. Hapus Action Figure")
            print("4. Tampilkan Semua Action Figure")
            print("5. Sorting Action Figure")
            print("6. Cari Action Figure")
            print("7. Keluar ke Menu Utama")

            choice = input("Masukkan pilihan (1/2/3/4/5/6/7): ")

            if choice == '1':
                name = input("Masukkan name Action Figure: ")
                brand = input("Masukkan brand Action Figure: ")
                price = locale.atof(input("Masukkan harga Action Figure: "))
                quantity = int(input("Masukkan jumlah Action Figure: "))
                description = input("Masukkan deskripsi Action Figure (opsional): ")
                action_figure = ActionFigure(name, brand, price, quantity, description)
                store.add_action_figure(action_figure)
            elif choice == '2':
                name = input("Masukkan name Action Figure yang ingin diperbarui: ")
                field = input("Masukkan bidang yang ingin diperbarui (brand/price/quantity/description): ")
                value = input("Masukkan nilai baru: ")
                store.update_action_figure(name, field, value)
            elif choice == '3':
                name = input("Masukkan name Action Figure yang ingin dihapus: ")
                store.delete_action_figure(name)
            elif choice == '4':
                store.display_action_figures()
            elif choice == '5':
                key = input("Masukkan atribut untuk sorting (name/brand/price/quantity): ")
                order = input("Masukkan urutan sorting (asc/desc): ")
                reverse = order.lower() == "desc"
                store.action_figures.merge_sort(key, reverse)
                print("Sorting berhasil dilakukan.")
            elif choice == '6':
                key = input("Masukkan atribut untuk pencarian (name/brand/price/quantity): ")
                value = input("Masukkan nilai untuk pencarian: ")
                store.search_action_figure(key, value)
            elif choice == '7':
                print("Kembali ke Menu Utama.")
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")

def main():
    store = ActionFigureStore()
    while True:
        print("\nWELCOME TO ADMIN PANEL")
        print("\nPilih tindakan:")
        print("1. Login sebagai Admin")
        print("2. Keluar")

        choice = input("Masukkan pilihan (1/2): ")

        if choice == '1':
            admin_login(store)
        elif choice == '2':
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")

if __name__ == "__main__":
    main()

