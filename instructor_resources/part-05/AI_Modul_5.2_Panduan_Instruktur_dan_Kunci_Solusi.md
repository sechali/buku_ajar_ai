# Panduan Instruktur dan Kunci Solusi
# AI Modul 5.2: Jenis Machine Learning (Supervised, Unsupervised, Reinforcement Learning)

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Berbasis OBE (3 SKS / 150 Menit)

Modul ini membekali mahasiswa Sarjana Sains Data, Kecerdasan Buatan, dan Teknik Pertanian dengan pemahaman komparatif mendalam mengenai tiga pilar fundamental pembelajaran mesin: **Supervised Learning**, **Unsupervised Learning**, dan **Reinforcement Learning**. Instruktur bertugas melatih mahasiswa agar mampu mengenali karakteristik data agribisnis dan memetakan permasalahan lapangan ke dalam paradigma pembelajaran serta formulasi matematika yang tepat.

### 1.1 Matriks Alokasi Waktu Sesi Perkuliahan (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 menit) | **Refleksi & *Problem Framing*:** Studi kasus dilema pelabelan manual citra drone perkebunan kelapa sawit seluas 50.000 hektar vs ketiadaan label. | Presentasi kasus industri, *brainstorming* interaktif. | Memantik diskusi mengenai mahalnya biaya anotasi data dan kapan supervised learning tidak dapat digunakan. | Mahasiswa menyadari bahwa tidak semua masalah perkebunan memiliki label kebenaran dasar (*ground truth*). |
| **00:20 - 00:50** (30 menit) | **Dekonstruksi Teori Tiga Paradigma:** Formulasi matematis $y = f(\mathbf{x})$, pemodelan struktur laten $p(\mathbf{x})$, dan formulasi MDP $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$. | Ceramah teoritis mendalam, bedah diagram alur. | Membedah perbedaan mendasar antara sinyal supervisi instan, ketiadaan supervisi, dan ganjaran tertunda (*delayed rewards*). | Mahasiswa mampu membedakan karakteristik masukan, keluaran, dan fungsi objektif ketiga paradigma. |
| **00:50 - 01:25** (35 menit) | **Praktikum Terbimbing (Hands-on Lab):** Eksekusi naskah kode klasifikasi hara daun (Supervised), zonasi tanah K-Means & PCA (Unsupervised), serta simulasi irigasi Q-Learning (RL). | *Live coding* di Jupyter Notebook. | Mendampingi mahasiswa mengamati konvergensi tabel $Q(s, a)$ dan interpretasi komponen utama PCA. | Mahasiswa berhasil menjalankan tiga representasi paradigma dalam satu alur praktikum terpadu. |
| **01:25 - 02:10** (45 menit) | **Penyelesaian Kasus HOTS Mandiri:** Pengerjaan arsitektur hibrida semi-supervised (8.1), pemodelan MDP pintu air gambut (8.2), dan audit anomali pipa CPO (8.3). | Kerja mandiri berbasis tim (*collaborative inquiry*). | Berkeliling menguji ketepatan perancangan fungsi reward $\mathcal{R}(s, a)$ dan alasan pemilihan unsupervised learning. | Mahasiswa mampu merancang formula sistem cerdas terpadu untuk persoalan agribisnis kompleks. |
| **02:10 - 02:30** (20 menit) | **Evaluasi Formatif & Refleksi:** Pembahasan solusi kunci, sintesis perbandingan komparatif, dan penarikan benang merah menuju Modul 5.3 (Dataset Training & Testing). | Diskusi kelas pleno, *peer review*. | Memberikan umpan balik terukur dan memvalidasi kesiapan mahasiswa memasuki teknik partisi dataset. | Mahasiswa menguasai kriteria pemilihan paradigma dan siap melangkah ke rekayasa dataset. |

---

## 2. Matriks Identifikasi & Remedi Miskonsepsi Umum Mahasiswa

| No | Miskonsepsi Mahasiswa | Realitas Teknis & Konseptual | Pendekatan Remedi Instruktur |
| :--- | :--- | :--- | :--- |
| 1 | "Unsupervised Learning adalah algoritma yang lebih rendah derajatnya dibanding Supervised Learning karena akurasinya tidak bisa dihitung secara pasti." | Unsupervised Learning menyelesaikan masalah yang mustahil disentuh oleh Supervised Learning, yaitu saat label tidak tersedia atau biaya anotasinya terlampau mahal. Ketiadaan label bukan kelemahan, melainkan karakteristik masalah eksplorasi struktur data intrinsik. | Tunjukkan kasus citra satelit ribuan hektar: tidak ada manusia yang mampu melabeli jutaan pohon satu per satu. Unsupervised learning (klastering & PCA) adalah prasyarat mutlak untuk menyaring data sebelum tahap supervisi. |
| 2 | "Reinforcement Learning membutuhkan dataset historis tabel CSV atau Excel yang sangat besar seperti halnya Supervised Learning." | Reinforcement Learning **tidak beroperasi di atas dataset statis tetap**. Agen RL mengumpulkan datanya sendiri secara dinamis melalui interaksi langsung dengan lingkungan (*environment*) atau simulator fisika berbasis prinsip coba-ralat (*trial-and-error*). | Berikan analogi anak kecil yang belajar naik sepeda: tidak ada tabel Excel yang dibaca anak tersebut, ia mencoba mengayuh (aksi), merasakan keseimbangan (status), dan jatuh/berhasil (ganjaran/hukuman). |
| 3 | "Model deteksi anomali pada peralatan pabrik kelapa sawit harus selalu dilatih menggunakan model klasifikasi biner Supervised Learning (Normal vs Rusak)." | Kerusakan mesin atau kebocoran pipa adalah peristiwa yang sangat langka ($< 0.01\%$). Supervised learning akan mengalami kegagalan fatal akibat ketidakseimbangan kelas ekstrem dan ketidakmampuan mendeteksi jenis kerusakan baru yang belum pernah terjadi sebelumnya (*unseen failure modes*). | Jelaskan bahwa **Unsupervised Anomaly Detection** (seperti Isolation Forest) hanya mempelajari pola data operasional normal; setiap titik yang menyimpang dari kerapatan normal otomatis ditandai sebagai anomali tanpa perlu contoh rusak sebelumnya. |
| 4 | "Pada Reinforcement Learning, faktor diskon $\gamma$ sebaiknya selalu diatur bernilai 0 agar agen fokus pada hasil saat ini." | Jika $\gamma = 0$, agen bersifat miopik (*myopic* / berpandangan sangat pendek) dan hanya mengejar imbalan instan $R_{t+1}$ detik ini, mengabaikan konsekuensi bencana di masa depan (misal: menghabiskan seluruh cadangan air irigasi sekarang sehingga besok tanaman mati kekeringan). Nilai $\gamma$ mendekati 1 ($0.90 - 0.99$) mendorong agen membuat perencanaan strategis jangka panjang. | Tunjukkan formula Persamaan Bellman: nilai $\gamma^k$ membobot imbalan langkah ke depan. Tunjukkan eksperimen di mana agen dengan $\gamma = 0$ gagal menjaga kestabilan air gambut. |

---

## 3. Panduan Solusi Lengkap Latihan HOTS (Higher-Order Thinking Skills)

### 3.1 Solusi Tantangan 8.1: Desain Arsitektur Sistem Hibrida Semi-Supervised (Bobot: 35%)

#### 1. Kelemahan Pendekatan Supervised Learning Murni:
- Dari $500.000$ citra pohon mingguan, hanya $2.500$ sampel yang berlabel ($0.5\%$). Melatih model supervised murni pada $0.5\%$ data membuang $99.5\%$ kekayaan variasi spasial dan spektral yang terekam oleh drone.
- Selain itu, pengambilan $2.500$ sampel acak berisiko mengalami bias sampling (hanya mengambil pohon dari afdeling tertentu), sehingga model tidak mampu menggeneralisasi seluruh variasi topografi kebun 20.000 hektar.

#### 2. Desain Arsitektur Pembelajaran Hibrida (*Semi-Supervised Pipeline*):
```
500.000 Citra Spektral Mentah (Tanpa Label)
                   │
                   ▼
┌────────────────────────────────────────────────────────┐
│ TAHAP 1 (Unsupervised): Reduksi Dimensi & Ekstraksi Fitur│
│ PCA / Autoencoder: Mampatkan pita spektral ke fitur laten│
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ TAHAP 2 (Unsupervised): K-Means Klastering Lahan (K=50) │
│ Mengelompokkan seluruh populasi pohon ke 50 profil hara │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ Strategi Sampling Aktif (Active Learning)
Pilih 50 sampel paling representatif per klaster (Total = 2.500 pohon)
                           │
                           ▼ Uji Laboratorium Kimia Daun Aktual
2.500 Sampel Berlabel Presisi Tinggi (Supervised Dataset)
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ TAHAP 3 (Supervised): Pelatihan Klasifikasi Defisiensi  │
│ Random Forest / XGBoost Classifier                     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
Prediksi Status Hara Menyeluruh untuk 500.000 Pohon Kebun
```

#### 3. Strategi Sampling Aktif (*Active Learning Sampling*):
Alih-alih mengambil sampel daun secara acak, staf kebun mengambil sampel pohon yang posisinya paling dekat dengan pusat massa (*centroid*) dari masing-masing klaster K-Means serta pohon yang berada di perbatasan antar klaster (*boundary samples* dengan ketidakpastian tertinggi). Hal ini menjamin bahwa $2.500$ uji laboratorium memberikan representasi statistik maksimal bagi seluruh 20.000 hektar kebun.

---

### 3.2 Solusi Tantangan 8.2: Formulasi Matematika MDP pada Irigasi Gambut (Bobot: 35%)

#### 1. Ruang Status ($\mathcal{S}$):
Status pada waktu $t$ direpresentasikan oleh vektor observasi kontinu multi-sensor:
$$\mathbf{s}_t = [h_t, \Delta h_t, \theta_t, T_t, P_t^{\text{forecast}}]^T \in \mathcal{S}$$
Di mana:
- $h_t$: Tinggi muka air gambut saat ini (cm, misal $-55 \text{ cm}$).
- $\Delta h_t = h_t - h_{t-1}$: Laju perubahan muka air per jam (cm/jam).
- $\theta_t$: Kelembaban volumetrik tanah gambut lapisan atas (%).
- $T_t$: Suhu udara kanopi perkebunan ($^\circ\text{C}$).
- $P_t^{\text{forecast}}$: Estimasi probabilitas curah hujan dalam 6 jam ke depan.

#### 2. Ruang Aksi ($\mathcal{A}$):
Himpunan aksi kontrol diskrit aktuator pompa dan pintu air:
$$\mathcal{A} = \{a_0: \text{Buka Pintu Drainase}, a_1: \text{Kondisi Pasif (Katup Tertutup)}, a_2: \text{Nyalakan Pompa Suplai Rendah}, a_3: \text{Nyalakan Pompa Penuh}\}$$

#### 3. Perancangan Fungsi Ganjaran / *Reward Function* ($\mathcal{R}(s, a)$):
Fungsi ganjaran dirancang bertingkat dengan penalti asimetris:
$$\mathcal{R}(\mathbf{s}_t, a_t) = 
\begin{cases} 
+15 - 0.5 \cdot |h_t - (-50)| - c(a_t), & \text{jika } -60 \le h_t \le -40 \quad (\text{Zona Aman Optimal}) \\
-50 - 2.0 \cdot |h_t - (-60)|, & \text{jika } h_t < -60 \quad (\text{Bahaya Kekeringan \& Kebakaran Gambut}) \\
-30 - 1.5 \cdot (h_t - (-40)), & \text{jika } h_t > -40 \quad (\text{Bahaya Genangan \& Busuk Akar})
\end{cases}$$
Di mana $c(a_t)$ adalah biaya energi operasional listrik/solar pompa untuk mencegah pemborosan energi.

#### 4. Peran Faktor Diskon ($\gamma = 0.95$):
Faktor diskon $\gamma = 0.95$ memberikan pembobotan signifikan pada imbalan jangka panjang:
$$G_t = R_{t+1} + 0.95 R_{t+2} + (0.95)^2 R_{t+3} + \dots$$
Pada lahan gambut, dinamika peresapan air tanah berlangsung lambat (memiliki inersia hidrologis beberapa jam). Dengan $\gamma = 0.95$, agen belajar bahwa jika prakiraan cuaca menunjukkan cuaca panas terik 12 jam lagi ($P^{\text{forecast}} = 0$), tindakan menyalakan pompa pengisian pelan saat ini ($a_2$) akan mencegah penalti katastropik kebakaran gambut $(-50)$ di masa depan, melatih agen untuk bertindak **preventif proaktif**, bukan reaktif.

---

### 3.3 Solusi Tantangan 8.3: Evaluasi Kritis Paradigma pada Kebocoran Pipa CPO (Bobot: 30%)

#### 1. Analisis Kegagalan Supervised Learning:
- **Ketidakseimbangan Kelas Ekstrem (*Extreme Imbalance*):** Rasio kelas bocor hanya $2 : 10.000.000$ ($0.00002\%$). Model klasifikasi biner standar akan mengalami *majority class collapse*: model selalu memprediksi status "NORMAL" dan tetap memperoleh akurasi $99.99998\%$, namun sama sekali tidak berguna karena gagal mendeteksi kebocoran.
- **Ketiadaan Variasi Data Kerusakan (*Narrow Training Distribution*):** Dua kali insiden masa lalu hanya mewakili satu jenis kebocoran (misal retak sambungan las flens). Jika di masa depan pipa mengalami kebocoran jenis baru (misal korosi asam lemak di siku pipa atau penyumbatan katup), model supervised tidak akan mengenalinya karena pola tersebut tidak ada dalam data latih.

#### 2. Keunggulan Paradigma Unsupervised Learning (Deteksi Anomali):
- Unsupervised Anomaly Detection hanya membutuhkan data kondisi operasional pipa saat berjalan normal (yang tersedia dalam jumlah jutaan data).
- Algoritma memodelkan batas kerapatan manifold normal (*boundary of normality*). Setiap kali kombinasi tekanan dan laju alir fluida melompat keluar dari batas normalitas tersebut, sistem langsung memicu alarm tanda bahaya tanpa memerlukan label kegagalan historis.

#### 3. Algoritma Rekomendasi: *Isolation Forest*:
- **Mekanisme Kerja:** Algoritma mengisolasi titik data dengan memilih fitur secara acak lalu membagi partisi nilai secara acak antara nilai minimum dan maksimum.
- **Prinsip Deteksi:** Titik data anomali (kebocoran pipa) memiliki sifat "sedikit dan berbeda" (*few and different*), sehingga titik anomali membutuhkan jauh lebih sedikit partisi percabangan pohon (*shorter average path length*) untuk diisolasi dibandingkan titik data operasional normal. Nilai skor anomali dihitung berdasarkan kedalaman rata-rata pohon isolasi tersebut.

---

## 4. Rubrik Penilaian Portofolio Praktikum Berbasis OBE

| Kriteria Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Kurang Memuaskan (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Ketepatan Pemetaan Masalah ke Tiga Paradigma** | 25% | Mengklasifikasikan persoalan agribisnis ke dalam Supervised, Unsupervised, atau RL dengan argumentasi matematis dan sinyal supervisi yang sangat presisi. | Mampu membedakan paradigma secara umum namun masih keliru membedakan deteksi anomali dengan klasifikasi biner. | Salah memetakan paradigma pembelajaran (misal memaksakan supervised learning pada data tanpa label). |
| **Implementasi Model Supervised & Unsupervised** | 25% | Sukses mengeksekusi klasifikasi hara daun (Random Forest) dan segmentasi lahan (K-Means & PCA) dengan analisis metrik evaluasi mendalam. | Model berhasil dijalankan di notebook namun analisis interpretasi komponen PCA atau silhouette score masih dangkal. | Kode mengalami galat eksekusi atau parameter model tidak dikonfigurasi dengan benar. |
| **Pemodelan Formal Markov Decision Process (RL)** | 25% | Mampu merumuskan tupel $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$, mendesain fungsi reward proporsional, dan menganalisis tabel $Q(s, a)$ secara logis. | Merumuskan status dan aksi namun fungsi reward masih kurang memperhitungkan penalti ekstrim atau peran diskon $\gamma$. | Gagal memformulasikan elemen MDP; tidak memahami konsep agen, lingkungan, dan pembaruan Bellman. |
| **Arsitektur Sistem Hibrida Semi-Supervised** | 25% | Merancang pipeline hibrida (PCA + Klasifikasi) yang terbukti memangkas dimensi fitur dengan tetap mempertahankan akurasi prima pada notebook praktikum. | Menggabungkan model namun belum menerapkan standarisasi sebelum reduksi dimensi sehingga akurasi terdegradasi. | Tidak mampu mengintegrasikan unsupervised dan supervised learning dalam satu alur terpadu. |
