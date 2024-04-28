-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 28 Apr 2024 pada 19.07
-- Versi server: 5.7.33
-- Versi PHP: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pakan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `pembelian_pakan`
--

CREATE TABLE `pembelian_pakan` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `namaPakan` varchar(50) NOT NULL,
  `supplier` varchar(100) NOT NULL,
  `item` varchar(50) NOT NULL,
  `jumlahPakan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `pembelian_pakan`
--

INSERT INTO `pembelian_pakan` (`id`, `tanggal`, `namaPakan`, `supplier`, `item`, `jumlahPakan`) VALUES
(2, '2024-04-24', 'sentrat', 'Mas adi', 'bagus', 111);

-- --------------------------------------------------------

--
-- Struktur dari tabel `penerimaan_pakan`
--

CREATE TABLE `penerimaan_pakan` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `kodePakan` varchar(50) NOT NULL,
  `jenisPakan` varchar(50) NOT NULL,
  `jumlahPakan` int(11) NOT NULL,
  `kondisiPakan` varchar(50) NOT NULL,
  `SumberStokPakan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `penerimaan_pakan`
--

INSERT INTO `penerimaan_pakan` (`id`, `tanggal`, `kodePakan`, `jenisPakan`, `jumlahPakan`, `kondisiPakan`, `SumberStokPakan`) VALUES
(1, '2024-04-05', 'D333', 'Sintetis', 30, 'Baik', 'Stok lama'),
(2, '2024-04-04', 'D331', 'organik', 19, 'Baik', 'Mudah'),
(3, '2024-04-05', 'D335', 'organik', 20, 'Baik', 'bagus'),
(4, '2024-04-05', 'g44', 'organik', 2, 'baik', 'bagus'),
(5, '2024-04-04', 'g46', 'organik', 99, 'baik', 'bagus'),
(8, '2024-04-06', 'g44', 'organik', 2, 'baik', 'Stok lama'),
(9, '2024-04-07', 'g46', 'organik', 5, 'baik', 'bagus'),
(10, '2024-04-22', 'g70', 'organik', 78, 'baik', 'Ordal');

-- --------------------------------------------------------

--
-- Struktur dari tabel `penggunaan_pakan`
--

CREATE TABLE `penggunaan_pakan` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jenisPakan` varchar(50) NOT NULL,
  `nomorKandang` varchar(50) NOT NULL,
  `pagi` int(11) NOT NULL,
  `sore` int(11) NOT NULL,
  `total` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `penggunaan_pakan`
--

INSERT INTO `penggunaan_pakan` (`id`, `tanggal`, `jenisPakan`, `nomorKandang`, `pagi`, `sore`, `total`) VALUES
(1, '2024-04-13', 'organik', '12', 20, 19, 39),
(4, '2024-04-06', 'Organik', '11', 1, 1, 1),
(5, '2024-04-06', 'Organik', '11', 1, 1, 1),
(6, '2024-04-24', 'Organik', '12', 111, 121, 19);

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat`
--

CREATE TABLE `riwayat` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `modelRegresi` varchar(50) NOT NULL,
  `hariMulaiPrediksi` date NOT NULL,
  `jumlahHariDiprediksi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `riwayat`
--

INSERT INTO `riwayat` (`id`, `tanggal`, `modelRegresi`, `hariMulaiPrediksi`, `jumlahHariDiprediksi`) VALUES
(3, '2024-04-28', '1', '2024-04-30', 12);

-- --------------------------------------------------------

--
-- Struktur dari tabel `stok_pakan`
--

CREATE TABLE `stok_pakan` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jenisPakan` varchar(50) NOT NULL,
  `jumlahPakanMasuk` int(11) NOT NULL,
  `jumlahPenggunaanPakan` int(11) NOT NULL,
  `totalStokTersedia` int(11) NOT NULL,
  `kondisiStokPakan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `stok_pakan`
--

INSERT INTO `stok_pakan` (`id`, `tanggal`, `jenisPakan`, `jumlahPakanMasuk`, `jumlahPenggunaanPakan`, `totalStokTersedia`, `kondisiStokPakan`) VALUES
(2, '2024-04-18', 'oganik', 31, 10, 21, 'Baik'),
(4, '2024-04-20', 'Organik', 2, 1, 2, 'baik'),
(5, '2024-04-27', 'Organik', 12, 10, 19, 'baik');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(3, 'somat', 'somat@mail.com', 'gAAAAABmLfZyQmcRgEioJUpumMlwc-ANzR__Y8FPkmEJr0Fu6Z1P5mjR62m5BhUIsf4cYrSnYltExOWI8dxey22iIU4PdPmyAg==');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `pembelian_pakan`
--
ALTER TABLE `pembelian_pakan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `penerimaan_pakan`
--
ALTER TABLE `penerimaan_pakan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `penggunaan_pakan`
--
ALTER TABLE `penggunaan_pakan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `riwayat`
--
ALTER TABLE `riwayat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `stok_pakan`
--
ALTER TABLE `stok_pakan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `pembelian_pakan`
--
ALTER TABLE `pembelian_pakan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `penerimaan_pakan`
--
ALTER TABLE `penerimaan_pakan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `penggunaan_pakan`
--
ALTER TABLE `penggunaan_pakan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `riwayat`
--
ALTER TABLE `riwayat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `stok_pakan`
--
ALTER TABLE `stok_pakan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
