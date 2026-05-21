import streamlit as st
import pandas as pd
import time
import random
from algorithm import heap_sort, mergeSort, quick_sort, tim_sort, shell_sort
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui

class StreamlitApp:
    def __init__(self):
        self.title = "Aplikasi testing algoritma "
        st.set_page_config(
            page_title=self.title,
            page_icon="💠",
            layout="wide"
        )
        
        if 'page' not in st.session_state:
            st.session_state.page = "Home"

    def render_sidebar(self):
        with st.sidebar:
            pilihan_sidebar = option_menu(
                menu_title="Main menu",
                options=["Home", "Siswa", "Perbandingan Algoritma"],
                icons=["house-door-fill", "person-lines-fill", "arrows-angle-contract"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {
                        "padding": "0px!", 
                        "background-color": "transparent" 
                    },
                    "menu-title": {
                        "font-size": "22px",
                        "font-weight": "bold",
                        "text-align": "left",
                        "margin": "0px",
                        "padding-bottom": "10px"
                    },
                    "icon": {
                        "font-size": "16px" 
                    }, 
                    "nav-link": {
                        "font-size": "14px", 
                        "text-align": "left", 
                        "margin": "0px",
                        "transition": "color 0.2s ease, background-color 0.2s ease"
                    },
                    "nav-link:hover": {
                        "background-color": "#2E4A3F", 
                        "color": "#A3E635",            
                    },
                    "nav-link-selected": {
                        "background-color": "green",
                        "color": "#FFFFFF"
                    },
                }
            )
        return pilihan_sidebar
    
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

        blacklist_kolom = [kolom.upper() for kolom in ["Nama Siswa", "Kelas", "Nama", "No.", "No", "Nomor", "NIS", "Rata-Rata", "Tahun Ajaran"]]
        mapel_murni = [col for col in df.columns if col.upper() not in blacklist_kolom]
        
        kolom_rata_asli = "Rata-rata"
        for col in df.columns:
            if col.upper() == "RATA-RATA":
                kolom_rata_asli = col
                break

        if mapel_murni and "RATA-RATA" not in [c.upper() for c in df.columns]:
            for kolom in mapel_murni:
                df[kolom] = pd.to_numeric(df[kolom], errors='coerce')
            df["Rata-rata"] = df[mapel_murni].mean(axis=1).round(2)
            kolom_rata_asli = "Rata-rata"

        st.write("")
        st.write("") 
        with st.container():
            col_tab1, col_tab2, col_tab3 = st.columns([1, 1, 1])
            with col_tab2:
                tab = ui.tabs(
                    options=["Data Siswa", "Konfigurasi Sorting"], 
                    default_value="Data Siswa", 
                    key="tabs_manajemen_siswa"
                )

            st.write("")

            if tab == "Data Siswa":
                daftar_kelas_unik = df["Kelas"].unique().tolist()
                kelas_terpilih = st.multiselect(
                    "Filter Kelas",
                    options=daftar_kelas_unik,
                    default=daftar_kelas_unik,
                    key="multiselect_kelas"
                )

                df_tab1 = df[df["Kelas"].isin(kelas_terpilih)].copy()

                if df_tab1.empty:
                    st.warning("Tidak ada data yang cocok dengan filter kelas.")
                    return

                st.write("") 

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    ui.metric_card(
                        title="Total Siswa", 
                        content=f"{len(df_tab1)} Anak", 
                        description="Jumlah siswa lolos filter",
                        key="card_total"
                    )
                with col_m2:
                    max_val = df_tab1[kolom_rata_asli].max() if len(df_tab1) > 0 else 0
                    ui.metric_card(
                        title="Rata-Rata Tertinggi", 
                        content=f"{max_val}", 
                        description="Nilai rapor tertinggi",
                        key="card_max"
                    )
                with col_m3:
                    min_val = df_tab1[kolom_rata_asli].min() if len(df_tab1) > 0 else 0
                    ui.metric_card(
                        title="Rata-Rata Terendah", 
                        content=f"{min_val}", 
                        description="Nilai rapor terendah",
                        key="card_min"
                    )

                st.markdown("---")
                st.dataframe(df_tab1, width="stretch", hide_index=True)

            elif tab == "Konfigurasi Sorting":
                with st.form(key="form_sorting_siswa"):

                    col_header = st.columns(3)
                    
                    with col_header[1]:
                        st.subheader("Konfigurasi Sorting")

                    st.write("")

                    col_setup1, col_setup2 = st.columns(2)

                    with col_setup1:
                        daftar_kolom_nilai = mapel_murni + [kolom_rata_asli]
                        kolom_terpilih = st.selectbox(
                            "Pilih Mata Pelajaran / Nilai:", 
                            daftar_kolom_nilai, 
                            key="sb_kolom"
                        )

                    with col_setup2:
                        daftar_algo = {
                            "Heap Sort": heap_sort,
                            "Tim Sort": tim_sort,
                            "Merge Sort": mergeSort,
                            "Quick Sort": quick_sort,
                            "Shell Sort": shell_sort
                        }
                        algo_terpilih = st.selectbox(
                            "Pilih Algoritma Sorting:", 
                            list(daftar_algo.keys()), 
                            key="sb_algo"
                        )
                    
                    st.write("") 
                    
                    col_action1, col_action2 = st.columns(2)

                    with col_action1:
                        opsi_kelas_hasil = df["Kelas"].unique().tolist()
                        kelas_hasil_terpilih = st.multiselect(
                            "Filter Kelas: ",
                            options=opsi_kelas_hasil,
                            default=opsi_kelas_hasil,
                            key="ms_kelas"
                        )

                    with col_action2:
                        opsi_limit = ["Tampilkan Semua", "Top 5 Nilai", "Top 10 Nilai"]
                        batas_tampil = st.selectbox(
                            "Jumlah Tampilan:", 
                            opsi_limit,
                            key="sb_limit"
                        )

                    st.write("") 

                    opsi_urut = ["Terbesar", "Terkecil"]
                    pilihan = st.pills(
                        "Pilih Arah Urutan:",
                        opsi_urut,
                        selection_mode="single",
                        default="Terbesar",
                        key="pills_urut"
                    )

                    st.markdown("---")
                    st.write("") 
                    
                    tombol_mulai = st.form_submit_button(
                        label="Mulai Proses Sorting Data", 
                        use_container_width=True
                    )

                if tombol_mulai:
                    # wadah_pesan = st.empty()

                    df_sorted = df.copy()
                    list_nilai = df_sorted[kolom_terpilih].tolist()

                    fungsi_sorting = daftar_algo[algo_terpilih]
                    hasil_sort = fungsi_sorting(list_nilai)

                    nilai_terurut = hasil_sort if hasil_sort is not None else list_nilai

                    if pilihan == "Terbesar":
                        nilai_terurut.reverse()
                        apakah_ascending = False
                    else:
                        apakah_ascending = True

                    df_sorted = df_sorted.sort_values(by=kolom_terpilih, ascending=apakah_ascending)

                    df_sorted = df_sorted[df_sorted["Kelas"].isin(kelas_hasil_terpilih)]

                    if batas_tampil == "Top 5 Nilai":
                        df_sorted = df_sorted.head(5)
                    elif batas_tampil == "Top 10 Nilai":
                        df_sorted = df_sorted.head(10)

                    kolom_nama_asli = "Nama Siswa" if "Nama Siswa" in df.columns else "Nama"
                    kolom_tampil = [kolom_nama_asli, "Kelas", kolom_terpilih]
                    df_sorted = df_sorted[kolom_tampil]

                    st.write("")
                    st.subheader(f"{batas_tampil} Berdasarkan {kolom_terpilih}")
                    st.dataframe(df_sorted, width="stretch", hide_index=True)

    def page_algoritma(self):
        st.title("Perbandingan Algoritma")
        st.markdown("---")
        with st.container(border=True):
            st.subheader("Parameter Simulasi")
            
            opsi_max_n = st.select_slider(
                "Pilih Batas Maksimal Jumlah Data (N):",
                options=[100, 250, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000],
                value=25000
            )
            
            st.write("")
            tombol_simulasi = st.button("Jalankan Pengujian Real-Time", use_container_width=True)

        if tombol_simulasi:

            semua_n = [100, 250, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
            ukuran_uji = [n for n in semua_n if n <= opsi_max_n]
            
            daftar_algo = {
                "Heap Sort": heap_sort,
                "Tim Sort": tim_sort,
                "Merge Sort": mergeSort,
                "Quick Sort": quick_sort,
                "Shell Sort": shell_sort
            }
            
            baris_hasil = []
            
            progress_bar = st.progress(0, text="Memulai simulasi...")
            total_langkah = len(daftar_algo)
            
            for index, (nama_algo, fungsi_sort) in enumerate(daftar_algo.items()):
                progress_bar.progress((index + 1) / total_langkah, text=f"Menguji algoritma: {nama_algo}")
                
                catatan_algo = {"Algoritma": nama_algo}
                
                for n in ukuran_uji:
                    
                    data_acak = [random.randint(0, 100) for _ in range(n)]
                    
                    mulai = time.perf_counter()
                    fungsi_sort(data_acak)
                    selesai = time.perf_counter()
                    
                    durasi = selesai - mulai
                    
                    catatan_algo[f"N={n}"] = round(durasi, 6)
                    
                baris_hasil.append(catatan_algo)
                
            progress_bar.empty()
            st.success("Simulasi Pengujian Selesai!")
            
            df_hasil = pd.DataFrame(baris_hasil)
            
            st.subheader("Tabel Hasil Komparasi Kecepatan (Detik)")
            st.dataframe(df_hasil, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Grafik Tren Pertumbuhan Waktu (Time Complexity)")
            
            df_grafik = df_hasil.set_index("Algoritma").T
            df_grafik.index = [int(idx.split("=")[1]) for idx in df_grafik.index]
            
            st.line_chart(df_grafik)
            st.caption("Sumbu X: Jumlah Data (N) | Sumbu Y: Waktu Eksekusi (Detik). Semakin landai garisnya, semakin efisien algoritmanya.")

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