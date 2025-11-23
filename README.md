<div align="center">
  <a href="https://github.com/skimatt/smarteval-umu">
    <img src="https://cdn-icons-png.flaticon.com/512/2997/2997309.png" alt="SmartEval Logo" width="120" height="120">
  </a>

  <h1 align="center">🎓 SmartEval UMU</h1>

  <p align="center">
    <strong>Sistem Pelaporan & Evaluasi Kampus Terintegrasi</strong><br>
    Universitas Almuslim
  </p>

  <p align="center">
    <b>Transparansi</b> • <b>Kecepatan</b> • <b>Kualitas Mutu</b>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-2.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind">
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
    <img src="https://img.shields.io/badge/Chart.js-F5788D?style=for-the-badge&logo=chart.js&logoColor=white" alt="Charts">
  </p>
</div>

<br>

<p align="center">
  <img src="https://images.unsplash.com/photo-1531403009284-440f080d1e12?q=80&w=2070&auto=format&fit=crop" alt="Dashboard Preview" width="100%" style="border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
</p>

---

## 📖 Tentang Proyek

**SmartEval UMU** adalah platform digital terpadu yang dikembangkan khusus untuk **Universitas Almuslim**. Sistem ini bertujuan untuk meningkatkan kualitas layanan kampus, transparansi administrasi, serta mutu akademik melalui pelibatan aktif seluruh civitas akademika.

Platform ini berfungsi sebagai **jembatan komunikasi aman, rahasia, dan real-time** antara mahasiswa dan pihak manajemen kampus, menghilangkan birokrasi yang berbelit dalam penyampaian aspirasi.

### 💡 Konsep Utama
Sistem ini berdiri di atas dua pilar utama:
1.  📢 **Pelaporan Masalah (Aduan):** Sarana pelaporan fasilitas & layanan.
2.  ⭐ **Evaluasi Mutu Akademik:** Sistem penilaian kinerja dosen secara objektif.

---

## ✨ Fitur Unggulan

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>📢 Pelaporan Terintegrasi</h3>
      <p>Mahasiswa dapat melaporkan:</p>
      <ul>
        <li>Kerusakan Fasilitas (AC, Proyektor, dll).</li>
        <li>Kebersihan Lingkungan Kampus.</li>
        <li>Layanan Administrasi & Birokrasi.</li>
        <li>Pelanggaran Etika / Bullying.</li>
      </ul>
      <p><em>Sistem routing otomatis meneruskan laporan ke unit terkait.</em></p>
    </td>
    <td width="50%" valign="top">
      <h3>📊 Evaluasi Dosen (EDOM)</h3>
      <p>Penilaian mutu akademik yang mencakup:</p>
      <ul>
        <li><strong>Anonimitas Terjamin:</strong> Identitas mahasiswa disembunyikan.</li>
        <li><strong>Multi-kriteria:</strong> Pedagogik, Profesional, Kepribadian.</li>
        <li><strong>Real-time Stats:</strong> Hasil langsung diolah menjadi grafik.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🛡️ Keamanan & Verifikasi</h3>
      <ul>
        <li><strong>Verifikasi KTM:</strong> Admin memvalidasi setiap pendaftar.</li>
        <li><strong>Enkripsi Password:</strong> Menggunakan Bcrypt hashing.</li>
        <li><strong>Role-Based Access:</strong> Akses terpisah antara Mahasiswa, Dosen, dan Admin.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>📈 Dashboard Eksekutif</h3>
      <ul>
        <li>Visualisasi data aduan (Selesai vs Pending).</li>
        <li>Top 10 Dosen Terbaik.</li>
        <li>Heatmap area kampus dengan keluhan terbanyak.</li>
        <li>Export laporan ke PDF/Excel.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🔄 Alur Pengguna (User Flow)

<div align="center">

### 👨‍🎓 Mahasiswa
`Registrasi` ➔ `Verifikasi Admin` ➔ `Login` ➔ `Buat Laporan / Isi Kuesioner` ➔ `Monitoring Status`

### 👨‍💼 Administrator
`Validasi Akun` ➔ `Disposisi Laporan` ➔ `Update Status Penanganan` ➔ `Analisis Statistik`

</div>

---

## 🛠️ Teknologi yang Digunakan

Kami menggunakan *Tech Stack* modern untuk menjamin performa dan kemudahan pengembangan:

| Komponen | Teknologi | Deskripsi |
| :--- | :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) | Framework utama yang cepat dan skalabel. |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | Penyimpanan data relasional dengan ORM yang handal. |
| **Frontend** | ![Tailwind](https://img.shields.io/badge/Tailwind-38B2AC?logo=tailwind-css&logoColor=white) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) | Desain antarmuka modern dan responsif (Mobile First). |
| **Analitik** | ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white) | Pengolahan data statistik dan visualisasi grafik interaktif. |
| **Keamanan** | **Flask-Bcrypt** | Hashing password standar industri. |

---

## 🚀 Instalasi Lokal

Ingin menjalankan proyek ini di komputer Anda? Ikuti langkah berikut:

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/username/smarteval-umu.git](https://github.com/username/smarteval-umu.git)
    cd smarteval-umu
    ```

2.  **Buat Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Mac/Linux
    venv\Scripts\activate     # Untuk Windows
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Database**
    * Buat database baru di MySQL bernama `smarteval_db`.
    * Edit file `.env` atau `config.py` sesuai kredensial database Anda.

5.  **Jalankan Aplikasi**
    ```bash
    flask run
    ```
    Buka browser dan akses: `http://127.0.0.1:5000`

---

## 📸 Galeri Aplikasi

| Halaman Login | Dashboard Mahasiswa |
| :---: | :---: |
| <img src="https://placehold.co/600x400/38B2AC/ffffff?text=Login+Page" width="100%"> | <img src="https://placehold.co/600x400/3776AB/ffffff?text=Dashboard" width="100%"> |

| Form Pengaduan | Statistik Admin |
| :---: | :---: |
| <img src="https://placehold.co/600x400/F5788D/ffffff?text=Form+Aduan" width="100%"> | <img src="https://placehold.co/600x400/4479A1/ffffff?text=Statistik" width="100%"> |

---

## 📄 Lisensi

Proyek ini dikembangkan untuk kepentingan akademik **Universitas Almuslim**.
Didistribusikan di bawah Lisensi MIT.

---

<div align="center">
  <p>Dibuat dengan ❤️ dan ☕ oleh <strong>Tim Pengembang SmartEval UMU</strong></p>
  <p><em>Fakultas Ilmu Komputer - Universitas Almuslim</em></p>
</div>
