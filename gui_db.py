import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import date
import shif


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='img/add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Новый заказ', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='img/update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='img/delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='img/search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='img/refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'code', 'data', 'status', 'user_id', 'product_id'), height=15, show='headings')

        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('code', width=365, anchor=tk.CENTER)
        self.tree.column('data', width=150, anchor=tk.CENTER)
        self.tree.column('status', width=100, anchor=tk.CENTER)
        self.tree.column('user_id', width=100, anchor=tk.CENTER)
        self.tree.column('product_id', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID заказа')
        self.tree.heading('code', text='Код')
        self.tree.heading('data', text='Дата')
        self.tree.heading('status', text='Статус')
        self.tree.heading('user_id', text='Пользователь')
        self.tree.heading('product_id', text='Продукты')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, code, data, status, user_id, product_id):
        self.db.insert_data(code, data, status, user_id, product_id)
        self.view_records()
    
    def update_record(self, code, data, status, user_id, product_id):
        self.db.c.execute('''UPDATE orders SET code=?, data=?, status=?, user_id= ?, product_id = ? WHERE ID=?''',
                          (code, data, status, user_id, product_id, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM orders''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM orders WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM orders WHERE user_id LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Оформление заказа')
        self.geometry('400x220+1100+600')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Пользователь:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Товар:')
        label_select.place(x=50, y=80)
        label_select = tk.Label(self, text='Статус заказа:')
        label_select.place(x=50, y=120)
  
        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.combobox = ttk.Combobox(self, values=[u'Пицца', u'Мороженное'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        self.combobox2 = ttk.Combobox(self, values=[u'0', u'1'])
        self.combobox2.current(0)
        self.combobox2.place(x=200, y=120)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Оформить')
        self.btn_ok.place(x=220, y=170)
        
        self.shifr = shif.crypto()

        """code, data, status, user_id, product_id"""
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(shif.crypto(),
                                                                       date.today(),
                                                                       self.combobox2.get(),
                                                                       self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       ))

        self.grab_set()
        self.focus_set()


class Update(Child):
    
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать заказ')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.shifr,
                                                                       date.today(),
                                                                       self.combobox2.get(),
                                                                       self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       ))

        self.btn_ok.destroy()
    
    
    def default_data(self):
        try:
            self.db.c.execute('''SELECT * FROM orders WHERE id=?''',
                            (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
            row = self.db.c.fetchone()
            self.entry_description.insert(0, row[4])
            if row[5] != 'Пицца':
                self.combobox.current(1)
            if row[3] != '0':
                self.combobox2.current(1)
        except IndexError:
            print('Поймана ошибка!')


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+1100+600')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('diplom.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS orders (id integer primary key, code text, data text, status integer, user_id integer, product_id integer)''')
        self.conn.commit()

    def insert_data(self, code, data, status,user_id, product_id):
        self.c.execute('''INSERT INTO orders(code, data, status, user_id, product_id) VALUES (?, ?, ?, ?, ?)''',
                       (code, data, status, user_id, product_id))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("KGTA delivery")
    root.geometry("1100x500+800+400")
    root.resizable(False, False)
    root.mainloop()