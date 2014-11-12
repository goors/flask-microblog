-- phpMyAdmin SQL Dump
-- version 4.2.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 12, 2014 at 02:31 AM
-- Server version: 5.5.38-log
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `pregmatch`
--

-- --------------------------------------------------------

--
-- Table structure for table `Comment`
--

CREATE TABLE IF NOT EXISTS `Comment` (
`Id` int(11) NOT NULL,
  `Comment` varchar(128) NOT NULL,
  `Post` int(11) NOT NULL,
  `Nick` varchar(45) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `DateCreated` datetime DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `Comment`
--

-- --------------------------------------------------------

--
-- Table structure for table `Post`
--

CREATE TABLE IF NOT EXISTS `Post` (
`Id` int(11) NOT NULL,
  `Title` varchar(128) NOT NULL,
  `DateCreated` datetime NOT NULL,
  `DateModified` varchar(6) DEFAULT NULL,
  `Content` text NOT NULL,
  `Photo` varchar(45) NOT NULL,
  `User` int(11) NOT NULL,
  `Slug` varchar(45) NOT NULL,
  `NoOfViews` int(11) NOT NULL,
  `PostStatus` enum('0','1') NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `Post`
--


-- --------------------------------------------------------

--
-- Table structure for table `PostTag`
--

CREATE TABLE IF NOT EXISTS `PostTag` (
  `Tag` int(11) NOT NULL,
  `Post` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `PostTag`
--



-- --------------------------------------------------------

--
-- Table structure for table `Tag`
--

CREATE TABLE IF NOT EXISTS `Tag` (
`Id` int(11) NOT NULL,
  `TagName` varchar(45) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

--
-- Dumping data for table `Tag`
--



-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE IF NOT EXISTS `User` (
`Id` int(11) NOT NULL,
  `Nick` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `Role` varchar(6) NOT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`Id`, `Nick`, `Email`, `Role`, `Password`) VALUES
(7, 'Admin', 'admin@blog.com', 'Admin', 'pbkdf2:sha1:1000$RdRBS3jZ$42a1e2046eb318a6fba8dd8b8708b0be40bc464d');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Comment`
--
ALTER TABLE `Comment`
 ADD PRIMARY KEY (`Id`), ADD KEY `Post_idx` (`Post`);

--
-- Indexes for table `Post`
--
ALTER TABLE `Post`
 ADD PRIMARY KEY (`Id`), ADD KEY `User_idx` (`User`);

--
-- Indexes for table `PostTag`
--
ALTER TABLE `PostTag`
 ADD PRIMARY KEY (`Tag`,`Post`), ADD KEY `fk_Tags_has_Post_Post1_idx` (`Post`), ADD KEY `fk_Tags_has_Post_Tags1_idx` (`Tag`);

--
-- Indexes for table `Tag`
--
ALTER TABLE `Tag`
 ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
 ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Comment`
--
ALTER TABLE `Comment`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `Post`
--
ALTER TABLE `Post`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `Tag`
--
ALTER TABLE `Tag`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=9;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `Comment`
--
ALTER TABLE `Comment`
ADD CONSTRAINT `Post` FOREIGN KEY (`Post`) REFERENCES `Post` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Post`
--
ALTER TABLE `Post`
ADD CONSTRAINT `User` FOREIGN KEY (`User`) REFERENCES `User` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `PostTag`
--
ALTER TABLE `PostTag`
ADD CONSTRAINT `fk_Tags_has_Post_Post1` FOREIGN KEY (`Post`) REFERENCES `Post` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_Tags_has_Post_Tags1` FOREIGN KEY (`Tag`) REFERENCES `Tag` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
