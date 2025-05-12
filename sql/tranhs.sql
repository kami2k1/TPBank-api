-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 12, 2025 at 11:46 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tranhs`
--

-- --------------------------------------------------------

--
-- Table structure for table `api`
--

CREATE TABLE `api` (
  `id` int(11) NOT NULL,
  `key` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_vietnamese_ci;

--
-- Dumping data for table `api`
--

INSERT INTO `api` (`id`, `key`) VALUES
(4, 'kami');

-- --------------------------------------------------------

--
-- Table structure for table `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `amout` int(11) NOT NULL,
  `url` text DEFAULT NULL,
  `d` text NOT NULL,
  `status` int(11) DEFAULT 0,
  `api_id` int(11) NOT NULL,
  `time_st` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_vietnamese_ci;

--
-- Dumping data for table `logs`
--

INSERT INTO `logs` (`id`, `amout`, `url`, `d`, `status`, `api_id`, `time_st`) VALUES
(5, 10000, 'https://google.com', 'kami4wLplv9e', 4, 4, '2025-05-04 01:47:35'),
(6, 10000, 'https://google.com', 'kami-2kS9yIXdJz', 3, 4, '2025-05-04 03:39:07'),
(7, 10000, 'https://google.com', 'kami-lPBJYY7UOG', 3, 4, '2025-05-04 03:50:33'),
(8, 10000, 'https://google.com', 'kami_VsUxLWIFdT', 3, 4, '2025-05-04 03:52:11'),
(9, 20000, 'https://google.com', 'kamij6NB1myRsY', 1, 4, '2025-05-04 03:53:48'),
(10, 500000, 'https://zalo.me/quangz3', 'kamiAP4VprvFJa', 3, 4, '2025-05-11 13:44:24');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `api`
--
ALTER TABLE `api`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `api`
--
ALTER TABLE `api`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
