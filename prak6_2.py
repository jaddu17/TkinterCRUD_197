import sqlite3          # Mengimpor sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk # Mengimpor beberapa elemen yang akan digunakan

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database SQLite
    cursor = conn.cursor()  # Membuat objek cursor agar bisa mengexecute query SQL
    #Membuat tabel jika belum ada
    cursor.execute('''  
            CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER, 
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        ) 
    ''')
    conn.commit()  # Menyimpan perubahan pada database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan hasil query dalam bentuk list
    conn.close()  # Menutup koneksi ke database
    return rows  # Mengembalikan hasil query

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor
    # Menyisipkan data baru ke tabel
    cursor.execute('''  
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menggunakan placeholder untuk menghindari SQL injection
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk memperbarui data yang sudah ada berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute('''  # Memperbarui data berdasarkan ID
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  # Mencari data berdasarkan ID
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Mamasukan data baru ke tabel
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghapus data berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Jika nilai biologi lebih tinggi dari fisika dan inggris
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Jika nilai fisika lebih tinggi dari biologi dan inggris
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Jika nilai inggris lebih tinggi dari biologi dan fisika
    else:
        return "Tidak Diketahui"  # Jika tidak ada nilai yang paling tinggi

# Fungsi untuk menambahkan data ke database
def submit():
    try:
        nama = nama_var.get()  # Mengambil nilai nama dari input
        biologi = int(biologi_var.get())  # Mengambil nilai biologi dan mengkonversinya ke integer
        fisika = int(fisika_var.get())  # Mengambil nilai fisika dan mengkonversinya ke integer
        inggris = int(inggris_var.get())  # Mengambil nilai inggris dan mengkonversinya ke integer

        if not nama:  # Jika nama kosong, tampilkan pesan error
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Tampilkan pesan sukses
        clear_inputs()  # Kosongkan input
        populate_table()  # Perbarui tabel data
    except ValueError as e:  # Menangani jika ada input yang tidak valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data siswa yang sudah ada
def update():
    try:
        if not selected_record_id.get():  # Memastikan ada record yang dipilih untuk diupdate
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
        nama = nama_var.get()  # Mengambil nilai nama dari input
        biologi = int(biologi_var.get())  # Mengambil nilai biologi dan mengkonversinya ke integer
        fisika = int(fisika_var.get())  # Mengambil nilai fisika dan mengkonversinya ke integer
        inggris = int(inggris_var.get())  # Mengambil nilai inggris dan mengkonversinya ke integer

        if not nama:  # Jika nama kosong, tampilkan pesan error
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Tampilkan pesan sukses
        clear_inputs()  # Kosongkan input
        populate_table()  # Perbarui tabel data
    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data siswa yang dipilih
def delete():
    try:
        if not selected_record_id.get():  # Memastikan ada record yang dipilih untuk dihapus
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
        delete_database(record_id)  # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Tampilkan pesan sukses
        clear_inputs()  # Kosongkan input
        populate_table()  # Perbarui tabel data
    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan input form
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama
    biologi_var.set("")  # Mengosongkan input nilai biologi
    fisika_var.set("")  # Mengosongkan input nilai fisika
    inggris_var.set("")  # Mengosongkan input nilai inggris
    selected_record_id.set("")  # Mengosongkan ID record yang dipilih

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua baris di tabel
        tree.delete(row)
    for row in fetch_data():  # Mengambil data dari database
        tree.insert('', 'end', values=row)  # Menambahkan data ke tabel

# Fungsi untuk mengisi form input dengan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan item yang dipilih di tabel
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari item yang dipilih

        selected_record_id.set(selected_row[0])  # Menyimpan ID record yang dipilih
        nama_var.set(selected_row[1])  # Mengisi input nama
        biologi_var.set(selected_row[2])  # Mengisi input nilai biologi
        fisika_var.set(selected_row[3])  # Mengisi input nilai fisika
        inggris_var.set(selected_row[4])  # Mengisi input nilai inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menampilkan error jika tidak ada data yang dipilih

# Membuat database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Label dan input form untuk nama siswa dan nilai
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Button untuk menambahkan, memperbarui, atau menghapus data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Mengisi form dengan data yang dipilih di tabel

# Mengisi tabel dengan data dari database
populate_table()

root.mainloop()