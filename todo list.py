#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplikasi To-Do List Sederhana
Fitur: Simpan, Edit, Lihat, dan Tandai Status Tugas
"""

NAMA_FILE = "data_tugas.txt"

def muat_data():
    """Memuat data tugas dari file"""
    tugas_list = []
    try:
        with open(NAMA_FILE, "r", encoding="utf-8") as file:
            for baris in file:
                baris = baris.strip()
                if baris:
                    tugas_list.append(baris)
    except FileNotFoundError:
        pass
    return tugas_list

def simpan_data(tugas_list):
    """Menyimpan data tugas ke file"""
    with open(NAMA_FILE, "w", encoding="utf-8") as file:
        for tugas in tugas_list:
            file.write(tugas + "\n")

def parse_tugas(tugas_string):
    """Parse string tugas menjadi dictionary"""
    bagian = tugas_string.split("|")
    if len(bagian) >= 3:
        return {
            "id": int(bagian[0]),
            "judul": bagian[1],
            "deskripsi": bagian[2],
            "status": bagian[3] if len(bagian) > 3 else "Belum Selesai"
        }
    return None

def format_tugas(id_tugas, judul, deskripsi, status):
    """Format tugas menjadi string untuk penyimpanan"""
    return f"{id_tugas}|{judul}|{deskripsi}|{status}"

def tampilankan_tugas_list(tugas_list):
    """Menampilkan semua tugas dengan format rapi"""
    if not tugas_list:
        print("\n❌ Tidak ada tugas.\n")
        return
    
    print("\n" + "="*80)
    print("📋 DAFTAR TUGAS".center(80))
    print("="*80)
    
    for tugas_str in tugas_list:
        tugas = parse_tugas(tugas_str)
        if tugas:
            status_simbol = "✅" if tugas["status"] == "Selesai" else "⏳"
            print(f"\n{status_simbol} ID: {tugas['id']}")
            print(f"   Judul: {tugas['judul']}")
            print(f"   Deskripsi: {tugas['deskripsi']}")
            print(f"   Status: {tugas['status']}")
    
    print("\n" + "="*80 + "\n")

def tambah_tugas(tugas_list):
    """Menambahkan tugas baru"""
    print("\n" + "="*40)
    print("➕ TAMBAH TUGAS BARU")
    print("="*40)
    
    # Tentukan ID baru
    id_baru = 1
    if tugas_list:
        id_terakhir = int(tugas_list[-1].split("|")[0])
        id_baru = id_terakhir + 1
    
    judul = input("📝 Masukkan judul tugas: ").strip()
    if not judul:
        print("❌ Judul tidak boleh kosong!\n")
        return tugas_list
    
    deskripsi = input("📝 Masukkan deskripsi tugas: ").strip()
    
    tugas_baru = format_tugas(id_baru, judul, deskripsi, "Belum Selesai")
    tugas_list.append(tugas_baru)
    
    print(f"✅ Tugas berhasil ditambahkan dengan ID: {id_baru}\n")
    return tugas_list

def edit_tugas(tugas_list):
    """Mengedit tugas yang ada"""
    if not tugas_list:
        print("\n❌ Tidak ada tugas untuk diedit.\n")
        return tugas_list
    
    print("\n" + "="*40)
    print("✏️  EDIT TUGAS")
    print("="*40)
    
    tampilankan_tugas_list(tugas_list)
    
    try:
        id_edit = int(input("Masukkan ID tugas yang ingin diedit: "))
        
        indeks = -1
        for i, tugas_str in enumerate(tugas_list):
            tugas = parse_tugas(tugas_str)
            if tugas and tugas["id"] == id_edit:
                indeks = i
                break
        
        if indeks == -1:
            print("❌ Tugas dengan ID tersebut tidak ditemukan.\n")
            return tugas_list
        
        tugas_lama = parse_tugas(tugas_list[indeks])
        
        print("\nPilihan Edit:")
        print("1. Edit Judul")
        print("2. Edit Deskripsi")
        print("3. Edit Keduanya")
        pilihan = input("Pilih opsi (1-3): ").strip()
        
        judul_baru = tugas_lama["judul"]
        deskripsi_baru = tugas_lama["deskripsi"]
        
        if pilihan in ["1", "3"]:
            judul_baru = input(f"Judul baru (saat ini: '{tugas_lama['judul']}'): ").strip()
            if not judul_baru:
                judul_baru = tugas_lama["judul"]
        
        if pilihan in ["2", "3"]:
            deskripsi_baru = input(f"Deskripsi baru (saat ini: '{tugas_lama['deskripsi']}'): ").strip()
            if not deskripsi_baru:
                deskripsi_baru = tugas_lama["deskripsi"]
        
        tugas_list[indeks] = format_tugas(
            tugas_lama["id"],
            judul_baru,
            deskripsi_baru,
            tugas_lama["status"]
        )
        
        print("✅ Tugas berhasil diubah.\n")
    
    except ValueError:
        print("❌ ID harus berupa angka.\n")
    
    return tugas_list

def tandai_selesai(tugas_list):
    """Menandai tugas sebagai selesai"""
    if not tugas_list:
        print("\n❌ Tidak ada tugas untuk ditandai.\n")
        return tugas_list
    
    print("\n" + "="*40)
    print("✔️  TANDAI TUGAS SELESAI")
    print("="*40)
    
    tampilankan_tugas_list(tugas_list)
    
    try:
        id_selesai = int(input("Masukkan ID tugas yang selesai: "))
        
        ditemukan = False
        for i, tugas_str in enumerate(tugas_list):
            tugas = parse_tugas(tugas_str)
            if tugas and tugas["id"] == id_selesai:
                tugas["status"] = "Selesai"
                tugas_list[i] = format_tugas(
                    tugas["id"],
                    tugas["judul"],
                    tugas["deskripsi"],
                    tugas["status"]
                )
                ditemukan = True
                print(f"✅ Tugas '{tugas['judul']}' ditandai sebagai selesai.\n")
                break
        
        if not ditemukan:
            print("❌ Tugas dengan ID tersebut tidak ditemukan.\n")
    
    except ValueError:
        print("❌ ID harus berupa angka.\n")
    
    return tugas_list

def hapus_tugas(tugas_list):
    """Menghapus tugas"""
    if not tugas_list:
        print("\n❌ Tidak ada tugas untuk dihapus.\n")
        return tugas_list
    
    print("\n" + "="*40)
    print("🗑️  HAPUS TUGAS")
    print("="*40)
    
    tampilankan_tugas_list(tugas_list)
    
    try:
        id_hapus = int(input("Masukkan ID tugas yang ingin dihapus: "))
        
        ditemukan = False
        for i, tugas_str in enumerate(tugas_list):
            tugas = parse_tugas(tugas_str)
            if tugas and tugas["id"] == id_hapus:
                tugas_list.pop(i)
                ditemukan = True
                print(f"✅ Tugas '{tugas['judul']}' berhasil dihapus.\n")
                break
        
        if not ditemukan:
            print("❌ Tugas dengan ID tersebut tidak ditemukan.\n")
    
    except ValueError:
        print("❌ ID harus berupa angka.\n")
    
    return tugas_list

def menu_utama():
    """Menampilkan menu utama"""
    while True:
        print("\n" + "="*50)
        print("📌 APLIKASI TO-DO LIST 📌".center(50))
        print("="*50)
        print("\n1️⃣  Lihat Semua Tugas")
        print("2️⃣  Tambah Tugas Baru")
        print("3️⃣  Edit Tugas")
        print("4️⃣  Tandai Tugas Selesai")
        print("5️⃣  Hapus Tugas")
        print("6️⃣  Keluar")
        print("\n" + "="*50)
        
        pilihan = input("Pilih menu (1-6): ").strip()
        
        tugas_list = muat_data()
        
        if pilihan == "1":
            tampilankan_tugas_list(tugas_list)
        elif pilihan == "2":
            tugas_list = tambah_tugas(tugas_list)
            simpan_data(tugas_list)
        elif pilihan == "3":
            tugas_list = edit_tugas(tugas_list)
            simpan_data(tugas_list)
        elif pilihan == "4":
            tugas_list = tandai_selesai(tugas_list)
            simpan_data(tugas_list)
        elif pilihan == "5":
            tugas_list = hapus_tugas(tugas_list)
            simpan_data(tugas_list)
        elif pilihan == "6":
            print("\n👋 Terima kasih telah menggunakan Aplikasi To-Do List!")
            print("📁 Data Anda telah disimpan di file: data_tugas.txt\n")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == "__main__":
    menu_utama()
