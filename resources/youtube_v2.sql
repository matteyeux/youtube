-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: youtube
-- ------------------------------------------------------
-- Server version 5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP DATABASE IF EXISTS youtube;
CREATE DATABASE IF NOT EXISTS youtube;
USE youtube;

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` longtext,
  `user_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comment_user1_idx` (`user_id`),
  KEY `fk_comment_video1_idx` (`video_id`),
  CONSTRAINT `fk_comment_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_video1` FOREIGN KEY (`video_id`) REFERENCES `video` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'pilou pilou poli poli',1,1),(3,'calialicojsfoefo',24,1);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revoked_tokens`
--

DROP TABLE IF EXISTS `revoked_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `revoked_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jti` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revoked_tokens`
--

LOCK TABLES `revoked_tokens` WRITE;
/*!40000 ALTER TABLE `revoked_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `revoked_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(45) NOT NULL,
  `expired_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_UNIQUE` (`code`),
  KEY `fk_token_user1_idx` (`user_id`),
  CONSTRAINT `fk_token_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
INSERT INTO `token` VALUES (1,'e5205a0d-dac3-4d3b-8a33-951a62889d61','2019-05-16 17:09:08',24),(2,'4b79fe77-9088-40ea-b613-d643da9a6286','2019-05-16 20:43:00',24),(3,'2ddea2be-fdab-418f-bdb0-ca85c59f7c76','2019-05-16 20:54:52',24);
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `pseudo` varchar(45) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (0,'matteyeux','matteyeux@0day.cool','matteyeux','bonjour','2019-05-03 11:41:22'),(1,'boris','boris@0day.cool','boris','bonjour','2019-05-03 11:42:10'),(2,'yoann','yoann@0day.cool','yoann','bonjour','2019-05-03 11:43:10'),(3,'atmgscbr','atmgscbr@pornhub','great','ccc','2019-05-11 20:50:24'),(4,'test','test@gmail.com','tteesstt','test','2019-05-12 19:25:01'),(5,'test1','test1@gmail.com','tteesstt1','test1','2019-05-12 19:27:57'),(6,'test2','test2@gmail.com','tteesstt2','$pbkdf2-sha256$29000$r/X.P.d87x1D6L2XkjJGKA$zxMe9J6zr19EmA0LjU7.rc/UvKAqJ.CyJJ3G1UL.IZg','2019-05-12 19:49:29'),(22,'test3','test3@gmail.com','tteesstt3','$pbkdf2-sha256$29000$pjQmxHhvbe09R8h5T4lxTg$KhaxZTBZP/nYo1bsrGmnQ2xVoSeFcM4IDUCYNMCaILA','2019-05-13 13:59:52'),(23,'test4','test4@gmail.com','tteesstt4','$pbkdf2-sha256$29000$8J6ztva.FwJAaG1NKeW8dw$csyKzHQv4VZ0CAfuMGibQG0W2ZHKe1NdYXb6HFRFue4','2019-05-13 14:50:36'),(24,'test5','test5@gmail.com','tteesstt5','$pbkdf2-sha256$29000$5xxDyDmntHZOyTlnrBViDA$wmuXsffnVqi8yayYem2zOctWvwd4xnIalyJ1a/5.n1s','2019-05-13 14:59:13'),(25,'test6','test6@gmail.com','tteesstt6','$pbkdf2-sha256$29000$QChFKEUoRQjBeI9RKqWUUg$XACnAgFznFrpxis2e5Hxqoan8Eky/hZI22dSlnjr.qs','2019-05-13 15:50:41'),(26,'test7','test7@gmail.com','tteesstt7','$pbkdf2-sha256$29000$5VxLSUmJcY4RQmgNoVTK2Q$raFBp6bLxm1ee07pRMV//Ta301K8DyCOHzIg177v37A','2019-05-16 17:07:35');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `duration` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `source` varchar(45) NOT NULL,
  `created_at` datetime NOT NULL,
  `view` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `encoded` boolean() NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_video_user_idx` (`user_id`),
  CONSTRAINT `fk_video_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video`
--

LOCK TABLES `video` WRITE;
/*!40000 ALTER TABLE `video` DISABLE KEYS */;
INSERT INTO `video` VALUES (1,'video1',11,1,'les/fesses/d/alex','2019-05-13 14:59:13',2,1);
/*!40000 ALTER TABLE `video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_format`
--

DROP TABLE IF EXISTS `video_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_format` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(45) NOT NULL,
  `uri` varchar(45) NOT NULL,
  `video_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_video_format_video1_idx` (`video_id`),
  CONSTRAINT `fk_video_format_video1` FOREIGN KEY (`video_id`) REFERENCES `video` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_format`
--

LOCK TABLES `video_format` WRITE;
/*!40000 ALTER TABLE `video_format` DISABLE KEYS */;
/*!40000 ALTER TABLE `video_format` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-16 21:08:30
