-- phpMyAdmin SQL Dump
-- version 4.0.10.12
-- http://www.phpmyadmin.net
--
-- Machine: 127.2.104.2:3306
-- Genereertijd: 13 apr 2017 om 08:17
-- Serverversie: 5.5.52
-- PHP-versie: 5.3.3

-- NOTE: Only run this after the tables are created by django migration by starting the server

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Databank: `refugive`
--

--
-- Gegevens worden uitgevoerd voor tabel `supdem_category`
--

INSERT INTO `supdem_category` (`id`, `name_en`) VALUES
(1, 'Child clothes'),
(2, 'Adult clothes'),
(4, 'Shoes'),
(5, 'Services and activities'),
(6, 'Toiletries'),
(7, 'Toys, books, etc.'),
(8, 'Telecommunication'),
(9, 'Other');

--
-- Gegevens worden uitgevoerd voor tabel `supdem_categoryquestion`
--

INSERT INTO `supdem_categoryquestion` (`id`, `name_en`, `category_id`) VALUES
(3, 'Sex', 1),
(4, 'Age', 1),
(5, 'Sex', 2),
(6, 'Size', 2),
(7, 'Size', 4),
(8, 'Kind', 5);

--
-- Gegevens worden uitgevoerd voor tabel `supdem_categoryquestionoption`
--

INSERT INTO `supdem_categoryquestionoption` (`id`, `name_en`, `order`, `categoryquestion_id`) VALUES
(17, 'Boy', 1, 3),
(18, 'Girl', 2, 3),
(19, 'Unisex', 3, 3),
(20, '0', 0, 4),
(21, '1', 1, 4),
(22, '2', 2, 4),
(23, '3', 3, 4),
(24, '4', 4, 4),
(25, '5', 5, 4),
(26, '6 and 7', 6, 4),
(27, '8 and 9', 7, 4),
(28, '10 and 11', 8, 4),
(29, '12 and 13', 9, 4),
(30, '14 and older', 10, 4),
(31, 'Female', 1, 5),
(32, 'Male', 2, 5),
(33, 'Unisex', 3, 5),
(34, 'Extra small', 1, 6),
(35, 'Small', 2, 6),
(36, 'Medium', 3, 6),
(37, 'Large', 4, 6),
(38, 'Extra large', 5, 6),
(39, 'Extra extra large', 6, 6),
(40, 'One size', 7, 6),
(41, 'baby', 1, 7),
(42, '18', 2, 7),
(43, '19', 3, 7),
(44, '20', 4, 7),
(45, '21', 5, 7),
(46, '22', 6, 7),
(47, '23', 7, 7),
(48, '24', 8, 7),
(49, '25', 9, 7),
(50, '26', 10, 7),
(51, '27', 11, 7),
(52, '28', 12, 7),
(53, '29', 13, 7),
(54, '30', 14, 7),
(55, '31', 15, 7),
(56, '32', 16, 7),
(57, '33', 17, 7),
(58, '34', 18, 7),
(59, '35', 19, 7),
(60, '36', 20, 7),
(61, '37', 21, 7),
(62, '38', 22, 7),
(63, '39', 23, 7),
(64, '40', 24, 7),
(65, '41', 25, 7),
(66, '42', 26, 7),
(67, '43', 27, 7),
(68, '44', 28, 7),
(69, '45', 29, 7),
(70, '46', 30, 7),
(71, '47', 31, 7),
(72, '48', 32, 7),
(73, 'Language lessons', 1, 8),
(74, 'Other lessons', 2, 8),
(75, 'Sports', 3, 8),
(76, 'Social', 4, 8),
(77, 'Dinner', 5, 8),
(78, 'Other', 6, 8);

--
-- Gegevens worden uitgevoerd voor tabel `supdem_centre`
--

INSERT INTO `supdem_centre` (`id`, `name`, `slug`, `address`, `city`, `countrycode`, `latitude`, `longitude`, `show_message_for_locals`, `show_message_for_refugees`, `is_active`) VALUES
(1, 'rijswijk', 'rijswijk', 'Lange Kleiweg 80', 'Rijswijk', 'nl', 0, 0, 0, 0, 1);

--
-- Gegevens worden uitgevoerd voor tabel `supdem_myuser`
--

INSERT INTO `supdem_myuser` (`id`, `password`, `last_login`, `email`, `username`, `is_active`, `is_admin`, `languagecode`, `creationdate`) VALUES
(1, 'pbkdf2_sha256$20000$93YGGz567Ntc$F90OYy0DdS5F9uSc8/OyBS20zHjOHyBi8m0kDKiL1mg=', '2017-04-11 18:43:47', 'jasper@cram.nl', 'jasper', 1, 1, 'nl', '2017-04-11 18:43:25');
