-- Database: `fakenews`
CREATE DATABASE fakenews;
-- --------------------------------------------------------

-- Table structure for table `search_results`

CREATE TABLE `search_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `search_query` varchar(255) NOT NULL,
  `verdict` enum('True','False','Inconclusive') NOT NULL,
  `explanation` text NOT NULL,
  `relevant_links` text,
  `search_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
