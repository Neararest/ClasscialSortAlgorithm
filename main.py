import streamlit as st
import pandas as pd
import time
import random
import gc
from PIL import Image
import plotly.express as px
from algorithm import heap_sort, mergeSort, quick_sort, tim_sort, shell_sort
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui

class StreamlitApp:
    def __init__(self):
        self.title = "Sortify"
        logo = Image.open("Sortify.png")
        st.set_page_config(
            page_title=self.title,
            page_icon=logo,
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
        st.title("SORTIFY")
        st.markdown("---")
        st.subheader("Sistem Analisis Komparasi Performa Algoritma Klasikal Sorting")
        
        ui.badges(
            badge_list=[
                ("Data Structure Algorithm", "default"), 
                ("Real-Time Analytics", "secondary"), 
            ], 
            class_name="flex gap-1 y-2", 
            key="home_badges"
        )

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            with st.container(border=True):
                st.markdown("### Tim Sort")
                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #333;' />", unsafe_allow_html=True)
                st.caption("Algoritma bawaan python yang membagi data menjadi blok kecil untuk diurutkan lalu digabung secara efisien dan stabil.")
        
        with col_b:
            with st.container(border=True):
                st.markdown("### Quick Sort")
                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #333;' />", unsafe_allow_html=True)
                st.caption("Mempartisi data secara agresif menggunakan elemen pembatas (pivot). Memiliki kecepatan pemrosesan in-place tertinggi pada data acak.")
        
        with col_c:
            with st.container(border=True):
                st.markdown("### Heap Sort")
                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #333;' />", unsafe_allow_html=True)
                st.caption("Memanfaatkan pohon biner (Binary Heap) untuk menyaring nilai ekstrem dari puncak secara berulang tanpa memakan memori tambahan.")
        
        col_d, col_e = st.columns(2)
        with col_d:
            with st.container(border=True):
                st.markdown("### Merge Sort")
                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #333;' />", unsafe_allow_html=True)
                st.caption("Membagi data secara konstan hingga ukuran terkecil lalu menggabungkannya kembali. Runtime dijamin stabil, namun membutuhkan memori tambahan.")
                
        with col_e:
            with st.container(border=True):
                st.markdown("### Shell Sort")
                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #333;' />", unsafe_allow_html=True)
                st.caption("Evolusi Insertion Sort yang membandingkan data berdasarkan jarak indeks (gap). Ringan untuk data kecil, namun melambat tajam pada data raksasa.")

        st.write("")

        st.subheader("Panduan Penggunaan")

        data_panduan = [
            {
                "trigger": "Implementasi Praktis", 
                "content": "Gunakan modul 'Siswa' di sidebar untuk menguji data riil sekolah. Anda dapat mengunggah file Excel nilai siswa, menyaring tingkat kelas, serta menganalisis perbandingan kecepatan komputasi (runtime) secara langsung dalam satuan milidetik (ms)."
            },
            {
                "trigger": "Perbandingan Algoritma", 
                "content": "Gunakan modul 'Perbandingan Algoritma' di sidebar untuk validasi teoretis. Modul ini menggunakan generator data acak dengan volume data yang dapat diatur secara fleksibel melalui slider hingga skala masif (1.000.000+ data)."
            }
        ]

        ui.accordion(data=data_panduan, class_name="w-full", key="panduan")

        with st.bottom:
            st.markdown("""
                <div style="text-align: center; color: #555555; font-size: 12px; padding: 0px 0;">
                    © 2026 Sortify • Project Akhir Struktur Data & Algoritma
                </div>
            """, unsafe_allow_html=True)

    def page_siswa(self):
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

                        opsi_tambahan = list(daftar_algo.keys()) + ["Semua Algoritma"]

                        algo_terpilih = st.selectbox(
                            "Pilih Algoritma Sorting:", 
                            opsi_tambahan, 
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
                    df_sorted = df.copy()
                    df_sorted = df_sorted[df_sorted["Kelas"].isin(kelas_hasil_terpilih)]
                    list_nilai = df_sorted[kolom_terpilih].tolist()

                    if algo_terpilih == "Semua Algoritma":
                        catatan_waktu = {}
                        with st.spinner("Menguji efisiensi seluruh algoritma pada data siswa..."):
                            for nama_algo, fungsi_sort in daftar_algo.items():
                                salinan_data = list_nilai.copy()
                                gc.collect()

                                mulai = time.perf_counter()
                                fungsi_sort(salinan_data)
                                selesai = time.perf_counter()
                                
                                catatan_waktu[nama_algo] = round((selesai - mulai) * 1000, 4)

                                del salinan_data
                        
                        nilai_terurut = list_nilai.copy()
                        tim_sort(nilai_terurut)
                        
                        if pilihan == "Terbesar":
                            nilai_terurut.reverse()
                            apakah_ascending = False
                        else:
                            apakah_ascending = True
                        
                        df_sorted = df_sorted.sort_values(by=kolom_terpilih, ascending=apakah_ascending)

                        if batas_tampil == "Top 5 Nilai":
                            df_sorted = df_sorted.head(5)
                        elif batas_tampil == "Top 10 Nilai":
                            df_sorted = df_sorted.head(10)
                            
                        kolom_nama_asli = "Nama Siswa" if "Nama Siswa" in df.columns else "Nama"
                        kolom_tampil = [kolom_nama_asli, "Kelas", kolom_terpilih]
                        df_sorted = df_sorted[kolom_tampil]

                        # DataFrame untuk Plotly
                        df_komparasi = pd.DataFrame({
                            "Algoritma": list(catatan_waktu.keys()),
                            "Waktu Eksekusi (ms)": list(catatan_waktu.values())
                        })

                        st.session_state["hasil_df_siswa"] = df_sorted
                        st.session_state["hasil_df_komparasi"] = df_komparasi
                        st.session_state["mode_tampil"] = "Semua Algoritma"
                        st.session_state["kolom_terpilih"] = kolom_terpilih
                        st.session_state["batas_tampil"] = batas_tampil
                        st.session_state["total_data"] = len(list_nilai)

                    else:
                        fungsi_sorting = daftar_algo[algo_terpilih]
                        hasil_sort = fungsi_sorting(list_nilai)

                        nilai_terurut = hasil_sort if hasil_sort is not None else list_nilai

                        if pilihan == "Terbesar":
                            nilai_terurut.reverse()
                            apakah_ascending = False
                        else:
                            apakah_ascending = True

                        df_sorted = df_sorted.sort_values(by=kolom_terpilih, ascending=apakah_ascending)

                        if batas_tampil == "Top 5 Nilai":
                            df_sorted = df_sorted.head(5)
                        elif batas_tampil == "Top 10 Nilai":
                            df_sorted = df_sorted.head(10)

                        kolom_nama_asli = "Nama Siswa" if "Nama Siswa" in df.columns else "Nama"
                        kolom_tampil = [kolom_nama_asli, "Kelas", kolom_terpilih]
                        df_sorted = df_sorted[kolom_tampil]

                        st.session_state["hasil_df_siswa"] = df_sorted
                        st.session_state["mode_tampil"] = "Tunggal"
                        st.session_state["algo_terpilih"] = algo_terpilih
                        st.session_state["kolom_terpilih"] = kolom_terpilih
                        st.session_state["batas_tampil"] = batas_tampil

                if "mode_tampil" in st.session_state:
                    if st.session_state["mode_tampil"] == "Semua Algoritma":
                        df_sorted = st.session_state["hasil_df_siswa"]
                        df_komparasi = st.session_state["hasil_df_komparasi"]
                        kolom_terpilih = st.session_state["kolom_terpilih"]
                        batas_tampil = st.session_state["batas_tampil"]
                        total_siswa = st.session_state["total_data"]

                        st.write("")

                        col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([1,1,1,1,1])
                        with col_t3:
                            tab = ui.tabs(
                                options=["Tabel", "Grafik"], 
                                default_value="Tabel", 
                                key="tabs_tabel_grafik"
                            )
                        if tab == "Tabel":
                            st.write("")
                            st.subheader(f"{batas_tampil} Berdasarkan {kolom_terpilih}")
                            st.dataframe(df_sorted, use_container_width=True, hide_index=True)
                            
                        elif tab == "Grafik":
                            st.write("")
                            st.subheader("  Analisis Komparasi Kecepatan Komputasi")

                            fig = px.bar(
                                df_komparasi,
                                x="Algoritma",
                                y="Waktu Eksekusi (ms)",
                                color="Algoritma",
                                text_auto='.4f',
                                title=f"Waktu Proses Pengurutan Kolom {kolom_terpilih} ({total_siswa} Data)"
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                            
                    elif st.session_state["mode_tampil"] == "Tunggal":
                        df_sorted = st.session_state["hasil_df_siswa"]
                        algo_terpilih = st.session_state["algo_terpilih"]
                        kolom_terpilih = st.session_state["kolom_terpilih"]
                        batas_tampil = st.session_state["batas_tampil"]

                        st.write("")
                        st.subheader(f"{batas_tampil} Berdasarkan {kolom_terpilih} (Menggunakan {algo_terpilih})")
                        st.dataframe(df_sorted, use_container_width=True, hide_index=True)
                    
    def page_algoritma(self):
        st.title("Perbandingan Algoritma")
        st.markdown("---")
        with st.container(border=True):
            st.subheader("Parameter Simulasi")
            
            opsi_max_n = st.select_slider(
                "Pilih Batas Maksimal Jumlah Data (N):",
                options=[100, 500, 1000, 5000, 10000, 50000, 100000, 250000, 500000, 1000000, 1500000],
                value=50000
            )
            
            st.write("")
            tombol_simulasi = st.button("Jalankan Pengujian Real-Time", use_container_width=True)

        if tombol_simulasi:

            semua_n = [100, 500, 1000, 5000, 10000, 50000, 100000, 250000, 500000, 1000000, 1500000]
            ukuran_uji = [n for n in semua_n if n <= opsi_max_n]
            
            daftar_algo = {
                "Heap Sort": heap_sort,
                "Tim Sort": tim_sort,
                "Merge Sort": mergeSort,
                "Quick Sort": quick_sort,
                "Shell Sort": shell_sort
            }
            
            random.seed(42) 
            bank_data = {}
            with st.spinner("Menyiapkan dataset acak..."):
                for n in ukuran_uji:
                    bank_data[n] = [random.randint(0, 100) for _ in range(n)]

            baris_hasil = []
            
            with st.spinner("Sedang menguji ke-5 algoritma secara real-time... Harap tunggu."):
                
                total_langkah = len(daftar_algo)
                
                for index, (nama_algo, fungsi_sort) in enumerate(daftar_algo.items()):
                    status_uji = st.caption(f"Sedang berjalan: **{nama_algo}** ({index+1}/{total_langkah})")
                    
                    catatan_algo = {"Algoritma": nama_algo}
                    
                    for n in ukuran_uji:
                        data_acak = bank_data[n].copy()

                        gc.collect()
                        mulai = time.perf_counter()
                        fungsi_sort(data_acak)
                        selesai = time.perf_counter()
                        
                        durasi = selesai - mulai
                        catatan_algo[f"N={n}"] = round(durasi, 6)

                        del data_acak
                        
                    baris_hasil.append(catatan_algo)
                    
                    status_uji.empty()  
            
            pesan = st.success("Pengujian Selesai!")
            time.sleep(0.5)
            pesan.empty()
            
            df_hasil = pd.DataFrame(baris_hasil)

            st.subheader("Tabel Hasil Komparasi Kecepatan (Detik)")
            st.dataframe(df_hasil, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Grafik Tren Pertumbuhan Waktu (Time Complexity)")
            
            df_grafik = df_hasil.set_index("Algoritma").T
            df_grafik.index = [int(idx.split("=")[1]) for idx in df_grafik.index]
            df_grafik.index.name = "Jumlah Data (N)"

            fig = px.line(
                df_grafik,
                labels={"value": "Waktu Eksekusi (Detik)", "variable": "Algoritma"},
                markers=True 
                )
            
            fig.update_layout(
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)
            st.caption("Arahkan kursor ke titik grafik untuk melihat detail waktu. Klik nama algoritma di legenda atas untuk menyembunyikan garis.")

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