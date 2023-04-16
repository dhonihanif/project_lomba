-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 16, 2023 at 01:40 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lomba`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `title` varchar(50) NOT NULL,
  `images` varchar(500) NOT NULL,
  `price` int(11) NOT NULL,
  `purchase_amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`title`, `images`, `price`, `purchase_amount`) VALUES
('Sate (satay) varieties', '/static/assets/img/shop/bali/satay_varieties.png', 50000, 1);

-- --------------------------------------------------------

--
-- Table structure for table `food`
--

CREATE TABLE `food` (
  `title` varchar(50) NOT NULL,
  `describe` varchar(500) NOT NULL,
  `image` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `stock` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `food`
--

INSERT INTO `food` (`title`, `describe`, `image`, `price`, `destination`, `stock`) VALUES
('Bebek and ayam betutu', 'Betutu is the slow-cooked equivalent of Bali’s babi guling (roast suckling pig). Suitable for those who don’t eat pork, this iconic Balinese dish consists of a whole chicken (ayam) or duck (bebek) stuffed with traditional spices, wrapped in banana leaves, then enveloped tight in the bark of a banana trunk. The entire thing is baked or buried in a coal fire for 6 to 7 hours, resulting in a rich and juicy meat that easily separates from the bones.', '/static/assets/img/shop/bali/bebek_and_ayam_betutu.png', 30000, 'bali', 12),
('Nasi ayam and nasi campur', 'Bali’s take on chicken rice, nasi ayam and nasi campur are served at many warungs (small eateries) and restaurants throughout the island. A plate of white rice comes with different elements of Balinese food, such as a portion of babi guling (roast suckling pig) or betutu (spiced chicken or duck), mixed vegetables, and a dab of spicy sambal matah (Balinese sauce).', '/static/assets/img/shop/bali/nasi_ayam.png', 35000, 'bali', 12),
('Sate (satay) varieties', 'Sate (or satay) are marinated, skewered and grilled meats served with spicy sauce. The meat usually consists of diced or sliced chicken, goat, mutton, beef and pork, but you\'ll also find satay that\'s made with fish, tofu, eggs or minced blends.', '/static/assets/img/shop/bali/satay_varieties.png', 50000, 'bali', 15);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(35) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `tempat_tinggal` varchar(20) DEFAULT NULL,
  `usia` int(2) DEFAULT NULL,
  `telp` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `name`, `tempat_tinggal`, `usia`, `telp`) VALUES
('dhonihanif354@gmail.com', 'twinet354', 'dhonihanif', 'Indonesia', 21, '+62895326168335');

-- --------------------------------------------------------

--
-- Table structure for table `posting`
--

CREATE TABLE `posting` (
  `title` varchar(30) NOT NULL,
  `sub_title` varchar(100) NOT NULL,
  `image` varchar(30) NOT NULL,
  `location` varchar(100) NOT NULL,
  `source` varchar(30) NOT NULL,
  `destination` varchar(20) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `username` varchar(35) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posting`
--

INSERT INTO `posting` (`title`, `sub_title`, `image`, `location`, `source`, `destination`, `content`, `username`) VALUES
('Kuta', 'Kuta is known as the party capital of Bali', 'static/assets/img/destination/', 'Kabupaten Badung, Bali', 'Cazzy Magennis', 'bali', 'When I first visited years ago, there was no beach shopping mall with designer stores, a range of fabulous beachfront restaurants, no no, and when I visited in 2019, I was actually shocked by just how “not Bali” that Kuta is! \r\n\r\nBut saying that, if you’re craving something more Americanized, or you want to go clubbing, then Kuta is a good place to be. ', 'dhonihanif354@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`title`);

--
-- Indexes for table `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`title`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `posting`
--
ALTER TABLE `posting`
  ADD PRIMARY KEY (`title`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
