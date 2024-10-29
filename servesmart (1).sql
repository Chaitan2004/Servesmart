-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 29, 2024 at 04:16 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `servesmart`
--

-- --------------------------------------------------------

--
-- Table structure for table `meals`
--

CREATE TABLE `meals` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `qrcode` blob NOT NULL,
  `meal_type` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `entry` varchar(20) DEFAULT NULL,
  `qr_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `meals`
--

INSERT INTO `meals` (`id`, `username`, `qrcode`, `meal_type`, `date`, `entry`, `qr_id`) VALUES
(35, '2022BCD0038', 0x89504e470d0a1a0a0000000d4948445200000172000001720100000000c05f6ca4000001ba4944415478daed9b4b6ec3300c4489fa003a92afae23f90002188b1f5171bb09d0a220315a04a93dab3c0c399454e28f5627e8a1871e7ae8a187fe97f464ebd0a774f2982fe6c7e5ef4ed17fd1670bfaffd593039deb9a7c2f613914289d573007dfbc7c85eacd524cec7cc5bff10c7c0bf00db45da8826f31bef737eecd7a32fc5bacff6ad78d40c5e8bf15f8aefcec268e0fe4e7fc7c63d9d366863513c73c85df336fffd5f9573bb141f6f9f700dff4fe55d72a550eb4427aa03e27efbf07eb40642c87f9b737ff06ff66f6afc6e4e159ca8b74181b7c53fb770dbc9d82f4f474db8724f04d3cff4a69decaf5666746ffcdefdf28d2b78989b62118f9397fff0d274fbe12b2b6ed68f4dfdc7c275071adf55fd984963fd70bf04d9faf3c26fbd6959f0fa2ffe6cf5783f64d2c7eabcf988fd2f3f55b1b7e2b6745abc6f06f8df9c80ef41db238f95b9fc6ef99333f33f383b415e9d59de1dfccf98abcf55a88267adcd9817fd3d767bd8bd36cfefd69630b7c53e7abe7ad0defbf27f69f8bf18d3d0f1d8d909febf0f55dabb8ee8efa5ca6ffdafccbe36de303f9aa4a7ef693e0631d0713e1fcb7cefc8bffbf831e7ae8a1871efabfd7bf00c4c2b1adf08c3cda0000000049454e44ae426082, 'lunch', '2024-10-30', 'filled', 'restricted'),
(36, '2022BCD0020', 0x89504e470d0a1a0a0000000d4948445200000172000001720100000000c05f6ca4000001c04944415478daed9b4d6e03210c85ade6001c69ae3e47e200482ee31f6cd255a45695d163314a98b7ca27e3679b107fb46e821e7ae8a1871e7ae87f494fb65e73a7cdaf178fe7c5f3e8feee12fd177db6a0ff5fbdf11578dc85ef20e14bd47c2f24e05b94ef13a6d76439a91a5f0d5ddd9b810dbe87f0d5bd4146157c0f8c5f399a6f790bbe47e55f41bb8147fe3d80eff2cf1ac4f901ff5c9f6f2cdb4d45d25e4fe1f7ac9b7fa5fe7d5cb33e6eff6a2fc0b772fc8aab1a4e952d7eed90964fe05b38ff362b7803ad74b26c75c46ff1f895fac8c3d45c738f7625fc737d7f254958ce67ef4fee9530f8d6e56b67b1014d4eeb563b8dfc5b9caf8c8e96b5dafb1bd1e400dfb2feca1e3a3f52bb158d2df8e703f85aaddb98d3a4e1d69a09f9b7385f3d9ac7f25716b5da93d6e903f816ee5ff1702f45361f8c748cfe647dbeabd64d4386b0d30d7c0fe0cba917e9f37d595747feaddfdfd84eea3cf5f57112f816f65744ded57869c32adde9884921f856f557bcce674e97ecbcf50cbed5f3ef8ad59ea7be39b0c1f71cbe6f5511facfc7f08d4ed68f9a187cebe75f9f34ac4bd071dd1d7c0ff0cf511f51be8e85fc7b48fd8bffdf410f3df4d0430ffddfebbf01ca3cbf0ca1e70a770000000049454e44ae426082, 'lunch', '2024-10-31', 'filled', 'restricted'),
(37, '2022BCD0020', 0x89504e470d0a1a0a0000000d4948445200000172000001720100000000c05f6ca4000001b14944415478daed9b418ec3200c45d1e4001c2957e7483940244a8c8d6977956634b2f558446df2577dfaf8dba4a57fb55a418f1e3d7af4e8d1ff92bee83ac69d7a3ff7d6e5b267a7e87fca770bfdffea95afc0eb97f095aff77854ed9e4be01b94ef63d373b014aa93efbcc8bd616cf866e1ab68c7defd50856f2ebe136dd59a2cfb337cf3d45fb3ae052aea6f0abe2b3fab89b70bf9393e5f5f82d18bb09ad8fb297ecfb8f577f5bffe757b00dfc0fe7d02d5445be67c43965562b5337c03efcf9eaa6c74d5ca5bb4c2bfa1f3f372a850fd4cd2f837b87f2fed7505e8e65f194737ea6ff8fe68edc5db40e3d690a5334bf826f1afaeaab8cdd3f00dcdd7816a88be8ef77618bec1f3d532b1d8595cdb8c34fe8dcd579be00fe69ea4f16f68be3eb0daec7c6c9ff06f0eff9e865b9ba44afd4de25f8bced629cdd648e61bf8377a7e5ee747e25585acaef50b7cc3ce37ccbaf3a4613dd67107fd6f82fadbed54dfbb22ef7fe11b3e3ffb0b1bfe2625f53719dfad264be6aa7dabc4f08defdfae87fcb667171b6cc13741fdb537397c267daf337ff8c6cfcff35f29de09b752983f27ea7ff9ff1d7af4e8d1a347fff7fa17ffc7afca82af21fe0000000049454e44ae426082, 'dinner', '2024-10-30', 'filled', 'restricted');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `type`) VALUES
(1, '2022BCD0038', '160M269W', 'operator'),
(2, 'admin', 'admin', 'admin'),
(3, '2022BCD0020', '123', 'operator');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `meals`
--
ALTER TABLE `meals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `meals`
--
ALTER TABLE `meals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `meals`
--
ALTER TABLE `meals`
  ADD CONSTRAINT `meals_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
