-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 22 Nov 2025 pada 00.02
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_eval_umu`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `lecturers`
--

CREATE TABLE `lecturers` (
  `id` int(11) NOT NULL,
  `nama` varchar(150) NOT NULL,
  `nidn` varchar(20) DEFAULT NULL,
  `fakultas` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `lecturers`
--

INSERT INTO `lecturers` (`id`, `nama`, `nidn`, `fakultas`, `created_at`) VALUES
(3, 'MUNAR', '0117117002', 'Teknik', '2025-11-21 02:05:00'),
(4, 'KHAIRUNI', '1309029901', 'Teknik', '2025-11-21 02:05:00'),
(5, 'IMAM MUSLEM R', '1308069101', 'Teknik', '2025-11-21 02:05:00'),
(6, 'IQBAL', '0124038403', 'Teknik', '2025-11-21 02:05:00'),
(7, 'ISKANDAR ZULKARNAINI', '0121106501', 'Teknik', '2025-11-21 02:05:00'),
(8, 'DASRIL AZMI', '0106077901', 'Teknik', '2025-11-21 02:05:00'),
(9, 'FITRI RIZANI', '1319118701', 'Teknik', '2025-11-21 02:05:00'),
(10, 'SRIWINAR', '0107087502', 'Teknik', '2025-11-21 02:05:00'),
(11, 'T RAFLI ABDILLAH', '1313087301', 'Teknik', '2025-11-21 02:05:00'),
(12, 'ZULKIFLI', '0104126601', 'Teknik', '2025-11-21 02:05:00'),
(13, 'TEUKU MUHAMMAD JOHAN', '9990284814', 'Teknik', '2025-11-21 02:05:00'),
(14, 'DEDY ARMIADY', '0129108601', 'Teknik', '2025-11-21 02:05:00'),
(15, 'RIYADHUL FAJRI', '0118128601', 'Teknik', '2025-11-21 02:05:00'),
(16, 'RIZA MIRZA', '', 'Teknik', '2025-11-21 02:05:00'),
(17, 'MUHAMMAD ERFAN SYAH', '1310089002', 'Teknik', '2025-11-21 02:05:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pending_users`
--

CREATE TABLE `pending_users` (
  `id` int(11) NOT NULL,
  `nim` varchar(15) NOT NULL,
  `nama_lengkap` varchar(150) NOT NULL,
  `prodi` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `hp` varchar(20) DEFAULT NULL,
  `bukti_url` varchar(255) NOT NULL,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  `alasan_penolakan` text DEFAULT NULL,
  `tanggal_pengajuan` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pending_users`
--

INSERT INTO `pending_users` (`id`, `nim`, `nama_lengkap`, `prodi`, `email`, `hp`, `bukti_url`, `status`, `alasan_penolakan`, `tanggal_pengajuan`) VALUES
(1, '235520110141', 'rahmat mulia', 'TI', 'skimatt10@gmail.com', '08223452627', 'placeholder/ktm_krs_dummy.jpg', 'accepted', NULL, '2025-11-20 14:25:38'),
(2, '235520110156', 'rahmat mulia', 'HK', 'rahmatzkk10@gmail.com', '08223452627', 'placeholder/ktm_krs_dummy.jpg', 'accepted', NULL, '2025-11-20 14:40:50'),
(3, '8798798989', 'asep', 'SI', 'rahmatmulia.11@icloud.com', '082239434989777', '/uploads/proofs/8798798989.png', 'accepted', NULL, '2025-11-20 18:10:14'),
(4, '235544667733', 'Budi', 'AK', 'helloworld@gmail.com', '0876372626', '/uploads/proofs/235544667733.png', 'accepted', NULL, '2025-11-21 05:22:12');

-- --------------------------------------------------------

--
-- Struktur dari tabel `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `mahasiswa_id` int(11) NOT NULL,
  `lecturer_id` int(11) NOT NULL,
  `rating_mengajar` decimal(2,1) NOT NULL,
  `rating_tugas` decimal(2,1) NOT NULL,
  `rating_materi` decimal(2,1) NOT NULL,
  `komentar` text DEFAULT NULL,
  `date_submitted` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `ratings`
--

INSERT INTO `ratings` (`id`, `mahasiswa_id`, `lecturer_id`, `rating_mengajar`, `rating_tugas`, `rating_materi`, `komentar`, `date_submitted`) VALUES
(1, 4, 1, 2.0, 5.0, 1.0, 'tidak tau cara nya', '2025-11-20 15:52:56'),
(2, 4, 2, 5.0, 5.0, 5.0, 'skimatt mantap emang', '2025-11-20 15:55:01'),
(3, 4, 3, 5.0, 5.0, 5.0, 'Pak munar sangat Mantap', '2025-11-20 19:06:51'),
(4, 4, 17, 4.0, 3.0, 3.0, 'baik', '2025-11-20 19:07:08'),
(5, 6, 3, 5.0, 5.0, 5.0, 'mantap', '2025-11-21 05:28:12');

-- --------------------------------------------------------

--
-- Struktur dari tabel `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `mahasiswa_id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `deskripsi` text NOT NULL,
  `kategori` enum('Fasilitas','Layanan TU','Perpustakaan','Akademik','Lainnya') NOT NULL,
  `status` enum('Pending','Diproses','Selesai','Arsip') DEFAULT 'Pending',
  `assigned_to_role` enum('akademik','perpustakaan','tu','kebersihan','bem') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `bukti_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `reports`
--

INSERT INTO `reports` (`id`, `mahasiswa_id`, `judul`, `deskripsi`, `kategori`, `status`, `assigned_to_role`, `created_at`, `updated_at`, `bukti_url`) VALUES
(1, 4, 'anjir banget', 'yyyyyyyyyyyyyyyyyyyyyyyyyy', 'Lainnya', 'Pending', '', '2025-11-20 15:07:41', '2025-11-20 15:07:41', 'placeholder/bukti_url_none'),
(2, 4, 'anjir banget', 'eeeeee eeeee eeee eee eeeee', 'Fasilitas', 'Pending', 'kebersihan', '2025-11-20 15:20:53', '2025-11-20 15:20:53', NULL),
(3, 4, 'anjir banget', 'ffffffffffff  fffffffffffffffff ffffffffffffff', 'Akademik', 'Diproses', 'akademik', '2025-11-20 15:35:59', '2025-11-20 15:36:43', '/uploads/proofs/235520110156_report__6'),
(4, 4, 'manusia setengah dea ', 'dosen yang bernama ini itu ', 'Akademik', 'Pending', 'akademik', '2025-11-20 18:00:55', '2025-11-20 18:00:55', NULL),
(5, 4, 'hello world wirfff', 'fffffffffffff fffffffffffffffffff fffffffffffff', 'Akademik', 'Pending', 'akademik', '2025-11-20 18:08:21', '2025-11-20 18:08:21', '/uploads/proofs/235520110156_report__7'),
(6, 5, 'hello world ', 'singkat padat anjai skimatt mulia', 'Akademik', 'Pending', 'akademik', '2025-11-20 18:23:05', '2025-11-20 18:23:05', '/uploads/proofs/8798798989_report_'),
(7, 6, 'ac mati sudah 5 hari di ruang 7', 'ac mati sudah 5 hari di ruang 7 dikarenakan sata nya konslet dll', 'Fasilitas', 'Diproses', 'kebersihan', '2025-11-21 05:25:04', '2025-11-21 05:26:47', '/uploads/proofs/235544667733_report_');

-- --------------------------------------------------------

--
-- Struktur dari tabel `report_comments`
--

CREATE TABLE `report_comments` (
  `id` int(11) NOT NULL,
  `report_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `komentar` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `report_comments`
--

INSERT INTO `report_comments` (`id`, `report_id`, `user_id`, `komentar`, `created_at`) VALUES
(1, 3, 2, 'halo terimakasih yaaaa', '2025-11-20 15:36:43'),
(2, 7, 2, 'ok terimaksih sudah melapor', '2025-11-21 05:26:47');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `nim` varchar(15) DEFAULT NULL,
  `nama_lengkap` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `prodi` varchar(100) DEFAULT NULL,
  `role` enum('admin','mahasiswa','akademik','perpustakaan','tu','kebersihan','bem') NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `nim`, `nama_lengkap`, `email`, `prodi`, `role`, `is_active`, `created_at`) VALUES
(2, 'admin_smart', '$2b$12$MJlCseiyJw24fp9b3jJ6luu0ej3NFSS8AIrzOtni7qX18QgaXDffu', '9999999999', 'Super Admin Umu', 'admin@umu.ac.id', 'Umum', 'admin', 1, '2025-11-16 13:20:58'),
(3, '235520110141', '$2b$12$JrRGX0Onxn4rPSB.5iXhr.i7og3JRDwolsTKaRbbfwILEGWfQSFXa', '235520110141', 'rahmat mulia', 'skimatt10@gmail.com', 'TI', 'mahasiswa', 1, '2025-11-20 14:25:56'),
(4, '235520110156', '$2b$12$3h7k1QL6zYwSKEdzBZaogeGl8q9ydzTP2s6Fb5uR8.ZuvxC0azDwm', '235520110156', 'rahmat mulia', 'rahmatzkk10@gmail.com', 'HK', 'mahasiswa', 1, '2025-11-20 14:41:12'),
(5, '8798798989', '$2b$12$wpPafPfyUyU.2GSr.53zTOSoJJjttu4zUZwE3UXKqBFvFyfqK9qrC', '8798798989', 'asep', 'rahmatmulia.11@icloud.com', 'SI', 'mahasiswa', 1, '2025-11-20 18:21:42'),
(6, '235544667733', '$2b$12$RFzoS6kcNdSjqhOK7.mnFOw9qkRulh/Hm9aD7xnAJslt8xny/Owf6', '235544667733', 'Budi', 'helloworld@gmail.com', 'AK', 'mahasiswa', 1, '2025-11-21 05:22:33');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `lecturers`
--
ALTER TABLE `lecturers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nidn` (`nidn`);

--
-- Indeks untuk tabel `pending_users`
--
ALTER TABLE `pending_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nim` (`nim`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indeks untuk tabel `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uc_mahasiswa_dosen` (`mahasiswa_id`,`lecturer_id`),
  ADD KEY `lecturer_id` (`lecturer_id`);

--
-- Indeks untuk tabel `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mahasiswa_id` (`mahasiswa_id`);

--
-- Indeks untuk tabel `report_comments`
--
ALTER TABLE `report_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `report_id` (`report_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `nim` (`nim`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `lecturers`
--
ALTER TABLE `lecturers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT untuk tabel `pending_users`
--
ALTER TABLE `pending_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `report_comments`
--
ALTER TABLE `report_comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`mahasiswa_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`mahasiswa_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `report_comments`
--
ALTER TABLE `report_comments`
  ADD CONSTRAINT `report_comments_ibfk_1` FOREIGN KEY (`report_id`) REFERENCES `reports` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `report_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
