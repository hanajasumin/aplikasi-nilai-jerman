import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ==========================================
# 1. KONFIGURASI KONEKSI GOOGLE SHEETS
# ==========================================
def hubungkan_ke_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    # Mengambil kredensial dari file JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    # Membuka Google Sheets berdasarkan nama filenya
    sheet = client.open("Nilai_Bahasa_Jerman_Fase_F").sheet1
    return sheet

# Menginisialisasi koneksi ke spreadsheet
try:
    sheet_koneksi = hubungkan_ke_sheets()
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets. Pastikan 'credentials.json' sudah benar. Error: {e}")
    st.stop()

# ==========================================
# 2. SISTEM KEAMANAN (HALAMAN LOGIN)
# ==========================================
# Parameter variabel password yang bisa Ibu sesuaikan sendiri
PASSWORD_RAHASIA = "Jerman62" 

# Menginisialisasi status login di memori browser (session state)
if "terlogin" not in st.session_state:
    st.session_state["terlogin"] = False

# Tampilan Halaman Login jika pengguna belum sukses login
if not st.session_state["terlogin"]:
    st.title("Gembok Keamanan Aplikasi")
    st.subheader("SMA Negeri 62 Maluku Tengah")
    
    # Kolom input untuk memasukkan kata sandi
    input_password = st.text_input("Masukkan Password Aplikasi:", type="password")
    tombol_login = st.button("Masuk")
    
    if tombol_login:
        if input_password == PASSWORD_RAHASIA:
            st.session_state["terlogin"] = True
            st.rerun() # Memuat ulang halaman untuk menampilkan form nilai
        else:
            st.error("Password salah! Silakan coba lagi.")
            
    st.stop() # Menghentikan kode di sini agar form nilai di bawah tidak terbuka

# ==========================================
# 3. TAMPILAN ANTARMUKA FORM NILAI (JIKA LOGIN BERHASIL)
# ==========================================
st.title("Aplikasi Input Nilai Bahasa Jerman Fase F")
st.subheader("SMA Negeri 62 Maluku Tengah")
st.write("Silakan isi formulir di bawah ini untuk menginput nilai formatif atau sumatif.")

# Tombol Keluar (Logout) untuk keamanan tambahan
if st.button("Keluar dari Aplikasi"):
    st.session_state["terlogin"] = False
    st.rerun()

# Membuat formulir input
with st.form("form_nilai", clear_on_submit=True):
    kelas = st.selectbox("Pilih Kelas:", ["Kelas XI", "Kelas XII"])
    jenis_nilai = st.radio("Jenis Nilai:", ["Formatif", "Sumatif"])
    tujuan_pembelajaran = st.text_input("Tujuan Pembelajaran (Contoh: TP 1.1 Memahami teks deskriptif pendek):")
    nama_siswa = st.text_input("Nama Siswa:")
    nilai = st.number_input("Nilai Siswa (0-100):", min_value=0, max_value=100, step=1)
    tombol_simpan = st.form_submit_button("Simpan ke Google Sheets")

# ==========================================
# 4. PROSES PENYIMPANAN DATA
# ==========================================
if tombol_simpan:
    if not tujuan_pembelajaran or not nama_siswa:
        st.warning("Mohon lengkapi kolom Tujuan Pembelajaran dan Nama Siswa sebelum menyimpan!")
    else:
        tanggal_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        baris_baru = [tanggal_sekarang, kelas, jenis_nilai, tujuan_pembelajaran, nama_siswa, nilai]
        
        try:
            sheet_koneksi.append_row(baris_baru)
            st.success(f"Data nilai untuk {nama_siswa} berhasil disimpan!")
        except Exception as e:
            st.error(f"Gagal menyimpan data ke Google Sheets. Terjadi kesalahan: {e}")