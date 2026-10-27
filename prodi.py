import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "siswa.db"
selected_id = None      


def create_query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    hasil = cursor.fetchall()
    conn.commit()
    conn.close()
    return hasil


def init_db():
    create_query("""CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER NOT NULL,
        fisika INTEGER NOT NULL,
        inggris INTEGER NOT NULL,
        prediksi_fakultas TEXT NOT NULL)""")


def predict_fakultas(biologi, fisika, inggris):
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika >= inggris:
        return "Teknik"
    else:
        return "Bahasa"


def add_nilai(nama, biologi, fisika, inggris):
    prediksi = predict_fakultas(biologi, fisika, inggris)
    create_query("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, "
              "prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
              (nama, biologi, fisika, inggris, prediksi))
    return prediksi


def get_nilai():
    return create_query("SELECT id, nama_siswa, biologi, fisika, inggris, "
                     "prediksi_fakultas FROM nilai_siswa ORDER BY id")

init_db()
root = tk.Tk()
root.title("Prediksi Fakultas")

entries = {}
for i, field in enumerate(["Nama Siswa", "Biologi", "Fisika", "Inggris"]):
    tk.Label(root, text=field).grid(row=i, column=0)
    entries[field] = tk.Entry(root, width=30)
    entries[field].grid(row=i, column=1, pady=4)

label_hasil = tk.Label(root, text="Hasil Prediksi: -",
                       font=("Arial", 11, "bold"))
label_hasil.grid(row=5, column=0, columnspan=2, pady=4)

cols = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=cols, show="headings")
lebar = {"id": 40, "nama_siswa": 140, "biologi": 70, "fisika": 70,
         "inggris": 70, "prediksi_fakultas": 120}
for c in cols:
    tree.heading(c, text=c.replace("_", " ").title())
    tree.column(c, width=lebar[c], anchor="center")
tree.grid(row=6, column=0, columnspan=2, padx=8, pady=8)


# ===== fungsi GUI: semua ditulis SEBELUM tombol dibuat =====
def read_form():
    nama = entries["Nama Siswa"].get().strip()
    teks = [entries[f].get().strip() for f in ("Biologi", "Fisika", "Inggris")]
    if not nama or not all(teks):
        messagebox.showwarning("Missing data", "Semua kolom harus diisi.")
        return None
    try:
        nilai = [int(t) for t in teks]
    except ValueError:
        messagebox.showwarning("Invalid nilai", "Nilai harus bilangan bulat.")
        return None
    if not all(0 <= n <= 100 for n in nilai):
        messagebox.showwarning("Invalid nilai", "Nilai harus 0 sampai 100.")
        return None
    return nama, nilai[0], nilai[1], nilai[2]


def refresh():
    tree.delete(*tree.get_children())
    for row in get_nilai():
        tree.insert("", tk.END, values=row)


def clear_form():
    global selected_id
    selected_id = None
    for e in entries.values():
        e.delete(0, tk.END)


def on_add():
    data = read_form()
    if data:
        hasil = add_nilai(*data)
        label_hasil.config(text="Hasil Prediksi: " + hasil)
        clear_form()
        refresh()

def on_clear():
    tree.selection_remove(tree.selection())
    clear_form()


def on_select(event):
    global selected_id
    sel = tree.selection()
    if not sel:
        return
    sid, nama, biologi, fisika, inggris, prediksi = tree.item(sel[0], "values")
    clear_form()
    selected_id = int(sid)
    entries["Nama Siswa"].insert(0, nama)
    entries["Biologi"].insert(0, biologi)
    entries["Fisika"].insert(0, fisika)
    entries["Inggris"].insert(0, inggris)

btns = tk.Frame(root)
btns.grid(row=4, column=0, columnspan=2, pady=4)
for text, cmd in [("Submit", on_add), ("Clear", on_clear)]:
    tk.Button(btns, text=text, width=8, command=cmd).pack(side="left", padx=4)

tree.bind("<<TreeviewSelect>>", on_select)

refresh()
root.mainloop()          