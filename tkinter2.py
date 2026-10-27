import tkinter as tk
import tkinter.messagebox as msg
import sqlite3

top = tk.Tk()
top.title("My Tkinter Window")
top.geometry("400x300")
top.configure(bg="blue")

E1 = tk.Entry(top, bd=5)
E1.pack()
E2 = tk.Entry(top, bd=5)
E2.pack()

def simpanData():
    nama = E1.get()
    umur = E2.get()
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY,"
                " name TEXT, age INTEGER)")
    cur.execute("INSERT INTO students (name, age) VALUES (?, ?)", (nama, umur))
    con.commit()
    con.close()
    msg.showinfo("Sukses", "Data berhasil disimpan!")

tombolSimpan = tk.Button(top, text="Simpan Data", command=simpanData)
tombolSimpan.pack()

top.mainloop()