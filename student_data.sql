-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 10, 2025 at 12:46 PM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `student_data`
--

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE IF NOT EXISTS `data` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `fees` decimal(10,2) NOT NULL,
  `course` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `data`
--

INSERT INTO `data` (`id`, `name`, `phone`, `fees`, `course`, `gender`) VALUES
(1, 'Rohan', '0987654321', '37500.00', 'BCA', 'Male'),
(2, 'Ridhi', '9203948394', '20000.00', 'BBA', 'Female'),
(3, 'Rily', '3049587345', '37483.00', 'BCA', 'Male'),
(4, 'ashis', '9384932934', '23883.00', 'BBA', 'Male'),
(5, 'Rehan', '2938382932', '22222.00', 'BBA', 'Male'),
(6, 'Rondu', '3849334893', '39000.00', 'BBA', 'Male'),
(7, 'sir', '8293829322', '150000.00', 'MCA', 'Male'),
(8, 'Mam', '8293827382', '150000.00', 'MCA', 'Female'),
(9, 'Ashis', '8293762738', '50000.00', 'MCA', 'Male'),
(10, 'Ashush', '2783662738', '50000.00', 'MBA', 'Male'),
(11, 'Digvi', '8293762563', '60000.00', 'MBA', 'Male'),
(12, 'ri', '9382378127', '78299.00', 'BBA', 'Male'),
(13, 'reee', '8374627382', '20000.00', 'BBA', 'Male'),
(14, 'rish', '9283723626', '50000.00', 'BCA', 'Male');

-- --------------------------------------------------------

--
-- Table structure for table `operation_logs`
--

CREATE TABLE IF NOT EXISTS `operation_logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` varchar(255) NOT NULL,
  `operation_type` varchar(50) NOT NULL,
  `student_id_affected` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `operation_logs`
--

INSERT INTO `operation_logs` (`log_id`, `teacher_id`, `operation_type`, `student_id_affected`, `timestamp`) VALUES
(6, '1', 'add', '11', '2025-04-30 11:49:51'),
(7, '3', 'add', '12', '2025-04-30 14:59:29'),
(8, '4', 'add', '13', '2025-05-08 11:17:50'),
(9, '5', 'add', '14', '2025-05-08 11:21:41');

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE IF NOT EXISTS `teachers` (
  `teacher_id` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`teacher_id`, `password`) VALUES
('1', 'nohna'),
('2', 'nohna@'),
('3', 'nonsu@'),
('4', 'rohan@'),
('5', 'rishabh@');
