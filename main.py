import streamlit as st
import pandas as pd
from algorithm import heap_sort, mergeSort, quick_sort, tim_sort, shell_sort

class StreamlitApp:
    def __init__(self):
        self.title = "Aplikasi Manajemen Data Siswa"
        st.set_page_config(
            page_title=self.title,
            page_icon="💠",
            layout="wide"
        )
        
        if 'page' not in st.session_state:
            st.session_state.page = "Home"

    def render_sidebar(self):
        st.sidebar.title("💠 Navigasi Utama")
        st.sidebar.markdown("---")
        pilihan = st.sidebar.selectbox(
            "Pilih Menu:",
            ["Home", "Siswa", "Perbandingan Algoritma"]
        )
        return pilihan
    
    def baca_file_pengguna(self, file):
        nama_file = file.name.lower()

        if nama_file.endswith(".csv"):
            return pd.read_csv(file)
        elif nama_file.endswith(".xlsx"):
            return pd.read_excel(file)
        else:
            st.error("Format file tidak didukung! Harap gunakan CSV atau XLSX.")
            return None

    def page_home(self):
        st.title("Halaman Beranda")
        st.markdown("---")
        st.write("Selamat datang di aplikasi dashboard utama.")
        st.info("Silakan pilih menu di samping untuk berpindah halaman.")

    def page_siswa(self):
        st.title("Manajemen Data Siswa")
        st.markdown("---")
        
        st.subheader("Unggah Data Siswa")
        masukkan_file = st.file_uploader("Unggah File", type=["csv", "xlsx"])

        if masukkan_file is None:
            st.info("Silahkan unggah file CSV atau Excel terlebih dahulu")
            return
        
        try:
            df = self.baca_file_pengguna(masukkan_file)
            if df is None:
                return
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            return

        kolom_upper = [col.upper() for col in df.columns]
        
        punya_nama = "NAMA SISWA" in kolom_upper or "NAMA" in kolom_upper
        punya_kelas = "KELAS" in kolom_upper
        
        if not (punya_nama and punya_kelas):
            st.error("Struktur file tidak sesuai! kolom Nama Siswa dan Kelas harus ada")
            return
        
        st.subheader("Filter Kelas Siswa")
        daftar_kelas_unik = df["Kelas"].unique().tolist()
        
        kelas_terpilih = st.multiselect(
            "Pilih Kelas yang ingin ditampilkan:",
            options=daftar_kelas_unik,
            default=daftar_kelas_unik
        )
        
        df_filtered = df[df["Kelas"].isin(kelas_terpilih)].copy()
        
        if df_filtered.empty:
            st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
            return

        blacklist_kolom = [kolom.upper() for kolom in ["Nama Siswa", "Kelas", "Nama", "No.", "No", "Nomor", "NIS", "Rata-Rata", "Tahun Ajaran"]]
        mapel_murni = [col for col in df_filtered.columns if col.upper() not in blacklist_kolom]
        ada_rata_rata = "RATA-RATA" in [c.upper() for c in df_filtered.columns]
        
        if mapel_murni:
            if not ada_rata_rata:
                for kolom in mapel_murni:
                    df_filtered[kolom] = pd.to_numeric(df_filtered[kolom], errors='coerce')

                df_filtered["Rata-Rata"] = df_filtered[mapel_murni].mean(axis=1).round(2)

        st.subheader("Data Siswa")
        st.dataframe(df_filtered, width="stretch", hide_index=True)
        
        st.markdown("---")
        
        with st.container(border=True):
            st.subheader("Konfigurasi Pengurutan")
            
            col_setup1, col_setup2, col_setup3 = st.columns(3)
            
            with col_setup1:
                daftar_kolom_nilai = mapel_murni + ["Rata-Rata"]
                kolom_terpilih = st.selectbox("Pilih Mata Pelajaran / Nilai:", daftar_kolom_nilai)
                
            with col_setup2:
                daftar_algo = {
                    "Heap Sort": heap_sort,
                    "Tim Sort": tim_sort,
                    "Merge Sort": mergeSort,
                    "Quick Sort": quick_sort,
                    "Shell Sort": shell_sort
                }
                algo_terpilih = st.selectbox("Pilih Algoritma Sorting:", list(daftar_algo.keys()))
                
            with col_setup3:
                opsi_kelas_hasil = df_filtered["Kelas"].unique().tolist()
                kelas_hasil_terpilih = st.multiselect(
                    "📌 Filter Kelas pada Hasil:",
                    options=opsi_kelas_hasil,
                    default=opsi_kelas_hasil
                )
            
            st.markdown("---")
            col_action1, col_action2 = st.columns([2, 1])
            
            with col_action1:
                opsi = ["Descending", "Ascending"]
                pilihan = st.pills(
                    "Pilih Urutan:",
                    opsi,
                    selection_mode="single"
                )
                tipe_urut = pilihan[0]

            with col_action2:
                st.write("") 
                tombol_mulai = st.button("Mulai Pengurutan", use_container_width=True)

        if tombol_mulai:
            wadah_pesan = st.empty()
            wadah_pesan.info(f"Memproses pengurutan kolom **{kolom_terpilih}** menggunakan **{algo_terpilih}**...")
            
            # Proses sorting data utama
            df_sorted = df_filtered.copy()
            list_nilai = df_sorted[kolom_terpilih].tolist()
            
            fungsi_sorting = daftar_algo[algo_terpilih]
            hasil_sort = fungsi_sorting(list_nilai)
            
            nilai_terurut = hasil_sort if hasil_sort is not None else list_nilai
            
            if tipe_urut == "Descending":
                nilai_terurut.reverse()
                apakah_ascending = False
            else:
                apakah_ascending = True

            df_sorted = df_sorted.sort_values(by=kolom_terpilih, ascending=apakah_ascending)
            
            # --- PENERAPAN FILTER KELAS KEDUA ---
            # Menyaring hasil sorting berdasarkan pilihan multiselect kelas hasil
            df_sorted = df_sorted[df_sorted["Kelas"].isin(kelas_hasil_terpilih)]
            
            kolom_nama_asli = "Nama Siswa" if "Nama Siswa" in df_filtered.columns else "Nama"
            kolom_tampil = [kolom_nama_asli, "Kelas", kolom_terpilih]
            df_sorted = df_sorted[kolom_tampil]
            
            # Tampilkan hasil
            wadah_pesan.success("✅ Pengurutan Berhasil!")
            st.subheader(f"📊 Hasil Pengurutan Berdasarkan: {kolom_terpilih}")
            st.dataframe(df_sorted, width="stretch", hide_index=True)

    def page_algoritma(self):
        st.title("Perbandingan Algoritma")
        st.markdown("---")
        st.write("Analisis performa algoritma sorting dan visualisasi data.")
        st.success("Halaman algoritma siap diisi logika backend.")

    def run(self):
        menu_terpilih = self.render_sidebar()
        
        if menu_terpilih == "Home":
            self.page_home()
        elif menu_terpilih == "Siswa":
            self.page_siswa()
        elif menu_terpilih == "Perbandingan Algoritma":
            self.page_algoritma()

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()