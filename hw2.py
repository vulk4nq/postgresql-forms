import sys
import psycopg2
from psycopg2 import Error
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import time


class db():
    def __init__(self, username,password,host,port,database_name,table):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.table_name = table
        self.counter = 1
    def TableIsChosen(self):
        if self.table_name != "":
            return True
        else:
            return False
    def DatabaseIsChosen(self):
        if self.database_name != "":
            return True
        else:
            return False
    def refresh_db_name(self):
        self.database_name = ""
        self.counter = 1
    def refresh_table_name(self):
        self.table_name = ""
        self.counter = 1
test_db = db(username="postgres",password="",database_name="",host="localhost",port="5432",table="")
def destroy_window(root):
    root.destroy()

def chooseTable():
    
        def to_main():
            test_db.table_name = comboTbl.get()
            destroy_window(chooseTb)
            main()

        connection = psycopg2.connect(user=test_db.username,
                                    # пароль, который указали при установке PostgreSQL
                                    password=test_db.password,
                                    host=test_db.host,
                                    port=test_db.port,
                                    database=test_db.database_name)
        cursor = connection.cursor()
        cursor.execute("select * from information_schema.tables where table_schema='public';")
        chooseTb = tk.Toplevel(root)
        
        labelToTable = tk.Label(chooseTb,text = "Выберите таблицу:")
        labelToTable.grid(column = 0, row = 0)
        chooseTb.title("Выберите Базу данных")
        btn_to_Tbl = tk.Button(chooseTb,text = "Просмотреть",command=to_main)
        # Создается новая рамка `frm_form` для ярлыков с текстом и
        # Однострочных полей для ввода информации о данных для подключения.
        
        list_of_table_temp = cursor.fetchall()
        if list_of_table_temp:
            list_of_tables = []
            
            
            for i in range(0,len(list_of_table_temp)):
                list_of_tables.append(list_of_table_temp[i][2])
            
            
            

            

             
            

            comboTbl = ttk.Combobox(chooseTb, values=list_of_tables)
            comboTbl.current(0)
            # Использует менеджер геометрии grid для размещения ярлыка и
            # однострочного поля для ввода текста в первый и второй столбец
            # первой строки сетки.
            comboTbl.grid(row = 1, column=1,columnspan=3)
            btn_to_Tbl.grid(row=2,column=0)
        else:
            messagebox.showinfo("ВНИМАНИЕ!","Нет таблиц доступных для просмотра")
            destroy_window(chooseTb)
            chooseDatabase()
def chooseDatabase():
        def to_main():
            test_db.database_name = combo.get()
            destroy_window(chooseDb)
            main()

        connection = psycopg2.connect(user=test_db.username,
                                    # пароль, который указали при установке PostgreSQL
                                    password=test_db.password,
                                    host=test_db.host,
                                    port=test_db.port,)
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database;")
        chooseDb = tk.Toplevel(root)
        
        labeltop = tk.Label(chooseDb,text = "Выберите Базу Данных:")
        labeltop.grid(column = 0, row = 0)
        chooseDb.title("Выберите Базу данных")
        btn_to_db = tk.Button(chooseDb,text = "Подключиться",command=to_main)
        # Создается новая рамка `frm_form` для ярлыков с текстом и
        # Однострочных полей для ввода информации о данных для подключения.
        
        list_of_database = cursor.fetchall()
        if  list_of_database:
        
            key = True
            i = 0
            while key:
                try:
                    list_of_database.remove(('template'+str(i),))
                    i+=1
                except:
                    key = False

             
            

            combo = ttk.Combobox(chooseDb, values=list_of_database)
            combo.current(1)
            # Использует менеджер геометрии grid для размещения ярлыка и
            # однострочного поля для ввода текста в первый и второй столбец
            # первой строки сетки.
            combo.grid(row = 1, column=1,columnspan=3)
            btn_to_db.grid(row=2,column=0)
        else:
            messagebox.showinfo("ВНИМАНИЕ!","Нет баз данных доступных для подключения")
            destroy_window(chooseDb)
            connect_to_db() 

def main():
    def check_value(example,number):
        cursor.execute("select data_type from information_schema.columns where table_name = 'Анкета';")
        rows = cursor.fetchall()
        if rows[i][0] == 'integer':
            try:
                int(example)
                return True
            except:
                return False

    def return_y(y):
        
        if y =="":
            return ',NULL'
        elif (isinstance(y,str)):
            return ','+"'"+y+"'"
        
    def delete_from_db():

        cursor.execute("DELETE FROM "+test_db.table_name+" WHERE "+types[0][0]+" = "+str(test_db.counter)+";")
        connection.commit()
        clear_forms()

    def apply_to_db():
        all_is_good = True
        types_temp = types[0][0]
        values_temp = ents[0].get()
        if check_value(ents[0].get(),0) == False:
           all_is_good = False
        for i in range(len(ents)):
            y = ents[i].get()
            
            if i!=0:
                types_temp += ","+types[i][0]
                values_temp += return_y(y)
        if all_is_good:
            cursor.execute("INSERT INTO "+test_db.table_name+" ("+types_temp+") VALUES ("+values_temp+");")
            connection.commit()
            print("SQL-запрос выполнен!")
        else:
            print("SQL-запрос не выполнен")
    def goto_db_choose():
        test_db.refresh_db_name()
        test_db.refresh_table_name()
        destroy_window(mainWindow)
        main()
    def goto_tbl_choose():
        test_db.refresh_table_name()
        destroy_window(mainWindow)
        main()
    def next_recording():

        cursor.execute("SELECT MAX("+types[0][0]+") FROM "+test_db.table_name+";")
        f = cursor.fetchone()
        
        if f[0]:    
            if test_db.counter < f[0]+1:
                if test_db.counter == f[0]:
                    test_db.counter += 1
                    lbl_counter.config(text = str(test_db.counter))
                    clear_forms()
                    ents[0].insert(0,str(f[0]+1))
                else:
                    clear_forms()
                    test_db.counter += 1
                    lbl_counter.config(text = str(test_db.counter))
                    cursor.execute("SELECT * FROM "+test_db.table_name+" WHERE "+types[0][0]+" = "+str(test_db.counter)+";")
                    fill_up_forms()
        else:
            messagebox.showinfo("ВНИМАНИЕ!","В таблице нет данных")
        
    def last_recording():
        cursor.execute("SELECT MAX("+types[0][0]+") FROM "+test_db.table_name+";")
        f = cursor.fetchone()
        if f[0]:
            if test_db.counter > 1:
                clear_forms()
                test_db.counter -= 1
                lbl_counter.config(text = str(test_db.counter))
                cursor.execute("SELECT * FROM "+test_db.table_name+" WHERE "+types[0][0]+" = "+str(test_db.counter)+";")
                fill_up_forms()
        else:
            messagebox.showinfo("ВНИМАНИЕ!","В таблице нет данных")
    def fill_up_forms():
        row = cursor.fetchone()
        if row:
            for j in range(len(row)):
                try:

                    ents[j].insert(0,row[j])
                except:
                    pass
        else:
            pass
    def clear_forms():
        for j in range(len(types)):
            ents[j].delete(0, 'end')
    fontStyle = tkFont.Font(family="Lucida Grande", size=30)


    if test_db.DatabaseIsChosen() == False:
        chooseDatabase()
    else:

        if test_db.TableIsChosen() == False:
            chooseTable()
        else:
            
            mainWindow = tk.Toplevel(root)
            mainWindow.geometry('900x900')
            mainWindow.title(test_db.table_name)
            connection = psycopg2.connect(user=test_db.username,
                                    # пароль, который указали при установке PostgreSQL
                                    password=test_db.password,
                                    host=test_db.host,
                                    port=test_db.port,
                                    database=test_db.database_name)
            cursor = connection.cursor()
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name ="+"'"+test_db.table_name+"'"+";")

            types = cursor.fetchall()
            
            frames = []
            labels = []
            ents = []
            maxlength_type = 0
            for i in range(len(types)):
                frames.append(tk.Frame(master=mainWindow,relief = tk.RAISED, borderwidth=3))
                frames[i].grid(row=i,column=0,padx=5,pady=3,sticky="W")
                if len(types[i][0])>maxlength_type:
                    maxlength_type = len(types[i][0])
                labels.append(tk.Label(master=frames[i],text =types[i], font= ('Helvetica 18'),width= 20))
                labels[i].pack(side=tk.LEFT,fill=tk.BOTH)
                ents.append(tk.Entry(master=frames[i],width=50))
                ents[i].pack(side=tk.LEFT,fill=tk.BOTH)
            for i in range(len(types)):
                labels[i].config(width= maxlength_type+2)
                
            frames.append(tk.Frame(master=mainWindow,relief = tk.RAISED, borderwidth=5))
            frames[-1].grid(row=len(types)+9,column= 2 ,columnspan=2)
            btn_next = tk.Button(master=frames[-1],text = ">",command=next_recording)
            btn_last = tk.Button(master=frames[-1],text = "<",command=last_recording)
            lbl_counter = tk.Label(master=frames[-1],text=str(test_db.counter))
            btn_last.pack(side=tk.LEFT,fill=tk.BOTH)
            lbl_counter.pack(side=tk.LEFT,fill=tk.BOTH)
            btn_next.pack(side=tk.LEFT,fill=tk.BOTH)

            frames.append(tk.Frame(master=mainWindow,relief = tk.RAISED, borderwidth=10))
            frames[-1].grid(row=len(types)+12,column=0,sticky="W")
            btn_to_db_from_main = tk.Button(master=frames[-1],text = "Выбрать Базу Данных",command=goto_db_choose,width = 24)
            btn_to_tbl_from_main = tk.Button(master=frames[-1],text = "Выбрать Таблицу",command=goto_tbl_choose,width = 24)
            
            btn_to_db_from_main.pack(side=tk.LEFT,fill=tk.BOTH)
            btn_to_tbl_from_main.pack(side=tk.LEFT,fill=tk.BOTH)
            
            frames.append(tk.Frame(master=mainWindow,relief = tk.RAISED, borderwidth=10))
            frames[-1].grid(row=len(types)+9,column=0,columnspan=2,pady=10,sticky="W")
            
            btn_to_write_to_db = tk.Button(master=frames[-1],text = "Записать в БД",command=apply_to_db,width = 24,bg= '#0dda4a')
            btn_to_write_to_db.pack(side=tk.LEFT,fill=tk.BOTH)
            btn_to_delete_from_db = tk.Button(master=frames[-1],text = "Удалить запись из БД",command=delete_from_db,width = 24,bg = '#ec8484')
            btn_to_delete_from_db.pack(side=tk.LEFT,fill=tk.BOTH)
            cursor.execute("select * from "+test_db.table_name+";")
            
            i = 0
            
            row = cursor.fetchone()
            if row:
                for j in range(len(row)):
                    ents[j].insert(0,row[j])
                    
                else:
                    pass

    
        

        
        
        
        
        
def connect_to_db():
  test_db.username = ent_user_name.get()
  test_db.password = ent_password.get()
  test_db.host = ent_host.get()
  test_db.port = ent_port.get()
  test_db.database_name = ent_db_name.get()
  try:
      # Подключение к существующей базе данных
      connection = psycopg2.connect(user=test_db.username,
                                    # пароль, который указали при установке PostgreSQL
                                    password=test_db.password,
                                    host=test_db.host,
                                    port=test_db.port,
                                    database=test_db.database_name)
      # Курсор для выполнения операций с базой данных
      cursor = connection.cursor()
      # Распечатать сведения о PostgreSQL
      print("Информация о сервере PostgreSQL")
      print(connection.get_dsn_parameters(), "\n")
      # Выполнение SQL-запроса
      cursor.execute("SELECT version();")
      # Получить результат
      record = cursor.fetchone()
      print("Вы подключены к - ", record, "\n")

      messagebox.showinfo("Вы подключены", "Подключение к базе данных прошло успешно!")
      destroy_window(window_first)
      main()
  except (Exception, Error) as error:
      messagebox.showinfo("Ошибка при работе с PostgreSQL", error)
      
  finally:
      if connection:
          cursor.close()
          connection.close()
          print("Соединение с PostgreSQL закрыто")

root = tk.Tk()
root.withdraw()
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=16)

root.option_add('*Font', default_font)
window_first = tk.Toplevel(root)


window_first.title("Подключение к БД Postgres")


# Создается новая рамка `frm_form` для ярлыков с текстом и
# Однострочных полей для ввода информации о данных для подключения.
frm_form = tk.Frame(window_first,relief=tk.SUNKEN, borderwidth=3)
# Помещает рамку в окно приложения.
frm_form.pack()
 
# Создает ярлык и текстовок поле для ввода имени.
lbl_user_name = tk.Label(master=frm_form, text="User:")
ent_user_name = tk.Entry(master=frm_form, width=50)
ent_user_name.insert(0,"postgres")
# Использует менеджер геометрии grid для размещения ярлыка и
# однострочного поля для ввода текста в первый и второй столбец
# первой строки сетки.
lbl_user_name.grid(row=0, column=0, sticky="e")
ent_user_name.grid(row=0, column=1)
 
# Создает ярлык и текстовок поле для ввода фамилии.
lbl_password = tk.Label(master=frm_form, text="Password:")
ent_password = tk.Entry(master=frm_form, width=50)

# Размещает виджеты на вторую строку сетки
lbl_password.grid(row=1, column=0, sticky="e")
ent_password.grid(row=1, column=1)
 
# Создает ярлык и текстовок поле для ввода первого адреса.
lbl_host = tk.Label(master=frm_form, text="Host:")
ent_host = tk.Entry(master=frm_form, width=50)
ent_host.insert(0,"localhost")
# Размещает виджеты на третьей строке сетки.
lbl_host.grid(row=2, column=0, sticky="e")
ent_host.grid(row=2, column=1)
 
# Создает ярлык и текстовок поле для ввода второго адреса.
lbl_port = tk.Label(master=frm_form, text="Port:")
ent_port = tk.Entry(master=frm_form, width=50)
ent_port.insert(0,"5432")
# Размещает виджеты на четвертой строке сетки.
lbl_port.grid(row=3, column=0, sticky=tk.E)
ent_port.grid(row=3, column=1)
 

lbl_db_name = tk.Label(master=frm_form, text="Database name:")
ent_db_name = tk.Entry(master=frm_form, width=50)

lbl_db_name.grid(row=4, column=0, sticky=tk.E)
ent_db_name.grid(row=4, column=1)

frm_buttons = tk.Frame(window_first)
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

btn_connect = tk.Button(master=frm_buttons, text="Подключиться!", command=connect_to_db)
btn_connect.pack(side=tk.RIGHT, padx=10, ipadx=10)


def close(event):
    connection.close()
    sys.exit()

root.bind('<Escape>',close)

root.mainloop()

