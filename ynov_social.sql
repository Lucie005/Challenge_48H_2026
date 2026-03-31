-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 30 mars 2026 à 12:32
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `ynov_social`
--

-- --------------------------------------------------------

--
-- Structure de la table `campus`
--

CREATE TABLE `campus` (
  `id` int(11) NOT NULL,
  `nom` varchar(200) NOT NULL,
  `ville` varchar(100) NOT NULL,
  `pays` varchar(100) DEFAULT 'France'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `campus`
--

INSERT INTO `campus` (`id`, `nom`, `ville`, `pays`) VALUES
(1, 'Paris Ynov Campus', 'Paris', 'France'),
(2, 'Lyon Ynov Campus', 'Lyon', 'France'),
(3, 'Bordeaux Ynov Campus', 'Bordeaux', 'France'),
(4, 'Toulouse Ynov Campus', 'Toulouse', 'France'),
(5, 'Nantes Ynov Campus', 'Nantes', 'France'),
(6, 'Marseille Ynov Campus', 'Marseille', 'France'),
(7, 'Rennes Ynov Campus', 'Rennes', 'France'),
(8, 'Paris Ouest Ynov Campus', 'Nanterre', 'France'),
(9, 'Paris Est Ynov Campus', 'Paris', 'France'),
(10, 'Lyon Ynov Campus', 'Lyon', 'France'),
(11, 'Bordeaux Ynov Campus', 'Bordeaux', 'France'),
(12, 'Toulouse Ynov Campus', 'Toulouse', 'France'),
(13, 'Nantes Ynov Campus', 'Nantes', 'France'),
(14, 'Lille Ynov Campus', 'Lille', 'France'),
(15, 'Montpellier Ynov Campus', 'Montpellier', 'France'),
(16, 'Aix Ynov Campus', 'Aix-en-Provence', 'France'),
(17, 'Rennes Ynov Campus', 'Rennes', 'France'),
(18, 'Rouen Ynov Campus', 'Rouen', 'France'),
(19, 'Sophia Ynov Campus', 'Nice', 'France'),
(20, 'Casablanca Ynov Campus', 'Casablanca', 'Maroc');

-- --------------------------------------------------------

--
-- Structure de la table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `contenu` text NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `comments`
--

INSERT INTO `comments` (`id`, `post_id`, `user_id`, `contenu`, `created_at`) VALUES
(1, 1, 2, 'Moi ! Je suis dispo, envoie moi un message 🙌', '2026-03-30 11:48:13'),
(2, 1, 3, 'Je peux aider depuis Lyon en remote, je commence React !', '2026-03-30 11:48:13'),
(3, 2, 1, 'Elle est vraiment propre ta maquette, chapeau 🔥', '2026-03-30 11:48:13'),
(4, 4, 1, 'Le point 2 m a tué 😂 Tellement vrai', '2026-03-30 11:48:13'),
(5, 5, 3, 'Respect pour la démarche responsable 👏', '2026-03-30 11:48:13'),
(6, 6, 4, 'C est trop bien pour un premier jeu !', '2026-03-30 11:48:13'),
(7, 8, 3, 'On peut venir depuis Lyon ? 😅', '2026-03-30 11:48:13'),
(8, 8, 4, 'Depuis Bordeaux aussi ? 🙏', '2026-03-30 11:48:13'),
(9, 9, 3, 'J y serai ! On a encore le feed à finir non ?', '2026-03-30 11:48:13'),
(10, 9, 2, 'Oui et la page profil aussi... on va pas dormir 😭', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `external_user`
--

CREATE TABLE `external_user` (
  `id` int(11) NOT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `follows`
--

CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `following_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `follows`
--

INSERT INTO `follows` (`follower_id`, `following_id`, `created_at`) VALUES
(1, 5, '2026-03-30 11:48:13'),
(2, 5, '2026-03-30 11:48:13'),
(3, 1, '2026-03-30 11:48:13'),
(3, 2, '2026-03-30 11:48:13'),
(3, 5, '2026-03-30 11:48:13'),
(4, 1, '2026-03-30 11:48:13'),
(4, 2, '2026-03-30 11:48:13'),
(4, 7, '2026-03-30 11:48:13'),
(5, 1, '2026-03-30 11:48:13'),
(6, 1, '2026-03-30 11:48:13'),
(6, 7, '2026-03-30 11:48:13'),
(7, 2, '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `job_offers`
--

CREATE TABLE `job_offers` (
  `id` int(11) NOT NULL,
  `titre` varchar(200) NOT NULL,
  `entreprise` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `type` enum('stage','alternance','CDI','CDD') NOT NULL,
  `lieu` varchar(200) DEFAULT NULL,
  `duree` varchar(100) DEFAULT NULL,
  `lien` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `job_offers`
--

INSERT INTO `job_offers` (`id`, `titre`, `entreprise`, `description`, `type`, `lieu`, `duree`, `lien`, `created_at`) VALUES
(1, 'Développeur web junior', 'Société Générale', 'Stage développement appli interne en React et Node.js', 'stage', 'Paris 9ème', '6 mois', 'https://ymatch.ynov.com', '2026-03-30 11:48:13'),
(2, 'UX/UI Designer', 'BNP Paribas', 'Refonte de l expérience utilisateur de l appli mobile', 'alternance', 'Paris 13ème', '1 an', 'https://ymatch.ynov.com', '2026-03-30 11:48:13'),
(3, 'Analyste Cybersécurité', 'Thales', 'Analyse des vulnérabilités et tests de pénétration', 'stage', 'Toulouse', '6 mois', 'https://ymatch.ynov.com', '2026-03-30 11:48:13'),
(4, 'Motion Designer', 'Ubisoft', 'Création d assets visuels pour jeux vidéo AAA', 'alternance', 'Lyon', '1 an', 'https://ymatch.ynov.com', '2026-03-30 11:48:13'),
(5, 'Community Manager', 'Decathlon', 'Gestion des réseaux sociaux et stratégie de contenu', 'stage', 'Lille', '4 mois', 'https://ymatch.ynov.com', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `likes`
--

INSERT INTO `likes` (`id`, `user_id`, `post_id`) VALUES
(6, 1, 2),
(10, 1, 5),
(13, 1, 6),
(16, 1, 7),
(19, 1, 8),
(26, 1, 9),
(1, 2, 1),
(11, 2, 5),
(14, 2, 6),
(17, 2, 7),
(20, 2, 8),
(27, 2, 9),
(2, 3, 1),
(7, 3, 2),
(15, 3, 6),
(21, 3, 8),
(28, 3, 9),
(3, 4, 1),
(12, 4, 5),
(22, 4, 8),
(29, 4, 9),
(4, 5, 1),
(8, 5, 2),
(18, 5, 7),
(23, 5, 8),
(5, 6, 1),
(24, 6, 8),
(9, 7, 2),
(25, 7, 8);

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `body` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `sent_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `news_ynov`
--

CREATE TABLE `news_ynov` (
  `id` int(11) NOT NULL,
  `campus_id` int(11) DEFAULT NULL,
  `titre` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `date_event` date DEFAULT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `news_ynov`
--

INSERT INTO `news_ynov` (`id`, `campus_id`, `titre`, `description`, `date_event`, `categorie`, `created_at`) VALUES
(1, 1, 'Challenge 48h — Réseau Social', 'Hackathon inter-filières B1 et B2 Paris Ouest. Créez le réseau social du campus !', '2026-03-31', 'Challenge', '2026-03-30 11:48:13'),
(2, 3, 'Hackathon IA Lyon', 'Compétition de dev IA au campus de Lyon. Propulsé par Google Gemini !', '2026-04-05', 'Challenge', '2026-03-30 11:48:13'),
(3, 4, 'Rise of the Algomancer', 'Coding Challenge algorithmique à Bordeaux Ynov Campus', '2026-04-08', 'Challenge', '2026-03-30 11:48:13'),
(4, 1, 'Tournoi FIFA BDS Paris', 'Tournoi FIFA inter-promos Paris Ouest. Inscriptions ouvertes !', '2026-04-10', 'BDS', '2026-03-30 11:48:13'),
(5, 5, 'YGame Jam Toulouse', 'Game Jam 72h ouverte aux étudiants Animation 3D et Informatique', '2026-04-15', 'Challenge', '2026-03-30 11:48:13'),
(6, NULL, 'Journée nationale Ynov', 'Événement commun à TOUS les campus Ynov de France ! Save the date 🇫🇷', '2026-05-15', 'National', '2026-03-30 11:48:13'),
(7, NULL, 'Forum Entreprises Ynov', 'Rencontrez +100 entreprises partenaires pour votre stage ou alternance', '2026-04-22', 'Career', '2026-03-30 11:48:13'),
(8, 6, 'Concours Court Metrage Nantes', 'Compétition de courts métrages entre étudiants Audiovisuel', '2026-05-01', 'BDE', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `contenu` text DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `portfolio`
--

CREATE TABLE `portfolio` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `titre` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `lien` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `technos` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `portfolio`
--

INSERT INTO `portfolio` (`id`, `user_id`, `titre`, `description`, `lien`, `image`, `technos`, `created_at`) VALUES
(1, 1, 'Appli météo temps réel', 'Appli météo avec API OpenWeather, géolocalisation et mode sombre', NULL, NULL, 'JavaScript, CSS, API REST', '2026-03-30 11:48:13'),
(2, 2, 'Redesign appli RATP', 'Refonte complète de l appli RATP pour la rendre intuitive et accessible', NULL, NULL, 'Figma, Adobe XD, Maze', '2026-03-30 11:48:13'),
(3, 5, 'Détecteur de fake news', 'Modèle IA qui analyse un texte et détecte les fake news avec 87% de précision', NULL, NULL, 'Python, Machine Learning, NLP', '2026-03-30 11:48:13'),
(4, 6, 'Platformer 2D Unity', 'Premier jeu vidéo complet avec système de vies, score et 3 niveaux', NULL, NULL, 'Unity, C#, Blender', '2026-03-30 11:48:13'),
(5, 7, 'Court métrage Nantes', 'Court métrage de 6 minutes tourné sur le campus de Nantes', NULL, NULL, 'Premiere Pro, After Effects, DaVinci', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `content` text DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `media_type` enum('text','image','video') DEFAULT 'text',
  `is_reel` tinyint(1) DEFAULT 0,
  `is_projet` tinyint(1) DEFAULT 0,
  `is_recherche` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `posts`
--

INSERT INTO `posts` (`id`, `author_id`, `content`, `media_url`, `media_type`, `is_reel`, `is_projet`, `is_recherche`, `created_at`) VALUES
(1, 1, 'Je cherche un designer pour mon appli de covoiturage entre campus Ynov 🚗 On est sur Paris Ouest mais on code pour toute la France !', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13'),
(2, 2, 'Ma maquette Figma pour le Challenge 48h est prête ! Interface inspirée de Dribbble 🎨', NULL, 'image', 0, 1, 0, '2026-03-30 11:48:13'),
(3, 3, 'Salut depuis Lyon ! Quelqu un connait des bons spots pour coder la nuit ? 🧑‍💻', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13'),
(4, 4, 'TOP 3 des erreurs marketing que font les étudiants sur leur CV 👇 Thread :', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13'),
(5, 5, 'J ai trouvé une faille XSS sur un site public et je l ai signalée responsablement 🔐 La cybersécurité c est pas que l attaque !', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13'),
(6, 6, 'Mon premier jeu Unity est jouable ! C est un platformer 2D basique mais je suis trop fier 🎮', NULL, 'video', 1, 1, 0, '2026-03-30 11:48:13'),
(7, 7, 'Mon court-métrage tourné au campus de Nantes est en ligne ! 6 minutes, 3 jours de tournage 🎬', NULL, 'video', 0, 1, 0, '2026-03-30 11:48:13'),
(8, 8, 'La soirée BDE de fin d année est confirmée ! Save the date : 15 juin 🎉 Tous les campus sont invités !', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13'),
(9, 1, 'Rappel : réunion équipe Challenge 48h ce soir 20h sur Discord ! On finalise la démo 🎯', NULL, 'text', 0, 0, 0, '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `titre` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `competences` text DEFAULT NULL,
  `nb_personnes` int(11) DEFAULT 1,
  `statut` enum('ouvert','complet','terminé') DEFAULT 'ouvert',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `projects`
--

INSERT INTO `projects` (`id`, `user_id`, `titre`, `description`, `competences`, `nb_personnes`, `statut`, `created_at`) VALUES
(1, 1, 'CampusRide — Covoiturage Ynov', 'Appli pour organiser les trajets entre tous les campus Ynov de France. Fini les galères de transport !', 'React, Node.js, MySQL', 3, 'ouvert', '2026-03-30 11:48:13'),
(2, 5, 'YnovBot — Assistant IA campus', 'Chatbot qui répond aux questions sur le campus, les cours et les events. Propulsé par Gemini API.', 'Python, API Gemini, SQL', 2, 'ouvert', '2026-03-30 11:48:13'),
(3, 2, 'PortfolioGen — CV automatique', 'Générez votre portfolio pro en 5 minutes depuis votre profil Ynov Social. Compatible toutes filières.', 'Figma, HTML, CSS', 2, 'complet', '2026-03-30 11:48:13'),
(4, 6, 'YGame Jam — Jam de jeux Ynov', 'Créer une game jam inter-campus où les étudiants en jeux vidéo s opposent à distance.', 'Unity, Blender, HTML', 4, 'ouvert', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `project_members`
--

CREATE TABLE `project_members` (
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role` varchar(100) DEFAULT NULL,
  `joined_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `project_members`
--

INSERT INTO `project_members` (`project_id`, `user_id`, `role`, `joined_at`) VALUES
(1, 1, 'Dev back-end', '2026-03-30 11:48:13'),
(1, 2, 'Designer UX/UI', '2026-03-30 11:48:13'),
(2, 3, 'Dev junior', '2026-03-30 11:48:13'),
(2, 5, 'Dev IA', '2026-03-30 11:48:13'),
(3, 2, 'Lead designer', '2026-03-30 11:48:13'),
(4, 6, 'Game designer', '2026-03-30 11:48:13'),
(4, 7, 'Motion designer', '2026-03-30 11:48:13');

-- --------------------------------------------------------

--
-- Structure de la table `skills`
--

CREATE TABLE `skills` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `niveau` enum('débutant','intermédiaire','avancé') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `skills`
--

INSERT INTO `skills` (`id`, `user_id`, `nom`, `niveau`) VALUES
(1, 1, 'JavaScript', 'avancé'),
(2, 1, 'Node.js', 'intermédiaire'),
(3, 1, 'SQL', 'avancé'),
(4, 1, 'React', 'intermédiaire'),
(5, 2, 'Figma', 'avancé'),
(6, 2, 'Adobe XD', 'intermédiaire'),
(7, 2, 'CSS', 'avancé'),
(8, 2, 'Illustrator', 'avancé'),
(9, 3, 'HTML/CSS', 'intermédiaire'),
(10, 3, 'Python', 'débutant'),
(11, 4, 'Community Management', 'avancé'),
(12, 4, 'Canva', 'avancé'),
(13, 4, 'SEO', 'intermédiaire'),
(14, 5, 'Python', 'avancé'),
(15, 5, 'Cybersécurité', 'avancé'),
(16, 5, 'API Gemini', 'avancé'),
(17, 6, 'Unity', 'intermédiaire'),
(18, 6, 'Blender', 'débutant'),
(19, 7, 'Premiere Pro', 'avancé'),
(20, 7, 'After Effects', 'avancé');

-- --------------------------------------------------------

--
-- Structure de la table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `campus_id` int(11) DEFAULT NULL,
  `role_title` varchar(100) DEFAULT NULL,
  `can_moderate` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `staff`
--

INSERT INTO `staff` (`id`, `campus_id`, `role_title`, `can_moderate`) VALUES
(8, 1, 'Président BDE Paris Ouest', 1),
(9, 1, 'Administrateur Ynov National', 1);

-- --------------------------------------------------------

--
-- Structure de la table `student`
--

CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `campus_id` int(11) DEFAULT NULL,
  `filiere` varchar(100) DEFAULT NULL,
  `is_searching_job` tinyint(1) DEFAULT 0,
  `skills` text DEFAULT NULL,
  `edt` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `student`
--

INSERT INTO `student` (`id`, `campus_id`, `filiere`, `is_searching_job`, `skills`, `edt`) VALUES
(1, 1, 'Informatique B2', 0, NULL, NULL),
(2, 1, 'Création & Digital Design B2', 0, NULL, NULL),
(3, 3, 'Informatique B1', 0, NULL, NULL),
(4, 4, 'Marketing & Communication Digitale B1', 1, NULL, NULL),
(5, 1, 'Cybersécurité B2', 0, NULL, NULL),
(6, 5, 'Animation 3D & Jeux Vidéo B1', 1, NULL, NULL),
(7, 6, 'Audiovisuel B2', 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `user_type` enum('student','staff') DEFAULT 'student',
  `bio` text DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `user_type`, `bio`, `photo`, `created_at`) VALUES
(1, 'axel.moreau', 'axel@ynov.com', 'hash123', 'student', 'Dev full-stack passionné à Paris Ouest 🚀 Je cherche toujours un projet cool', 'axel.jpg', '2026-03-30 11:48:13'),
(2, 'lea.chen', 'lea@ynov.com', 'hash456', 'student', 'UX/UI designer, je transforme vos idées en interfaces qui claquent ✨', 'lea.jpg', '2026-03-30 11:48:13'),
(3, 'youssef.diallo', 'youssef@ynov.com', 'hash789', 'student', 'Etudiant à Lyon, nouveau sur le campus, je cherche une équipe 👋', 'youssef.jpg', '2026-03-30 11:48:13'),
(4, 'camille.petit', 'camille@ynov.com', 'hash000', 'student', 'Community manager en devenir à Bordeaux 📈', 'camille.jpg', '2026-03-30 11:48:13'),
(5, 'thomas.nguyen', 'thomas@ynov.com', 'hashabc', 'student', 'Passionné de sécu et d IA à Paris Ouest 🤖 Je code même le week-end', 'thomas.jpg', '2026-03-30 11:48:13'),
(6, 'sofia.martin', 'sofia@ynov.com', 'hashsof', 'student', 'Game designer en herbe à Toulouse 🎮 Je crée mes premiers jeux Unity', 'sofia.jpg', '2026-03-30 11:48:13'),
(7, 'hugo.bernard', 'hugo@ynov.com', 'hashhug', 'student', 'Réalisateur en devenir à Nantes 🎬 Spécialisé motion design', 'hugo.jpg', '2026-03-30 11:48:13'),
(8, 'president.bde', 'bde@ynov.com', 'hashbde', 'staff', NULL, 'bde.jpg', '2026-03-30 11:48:13'),
(9, 'admin.ynov', 'admin@ynov.com', 'hashadm', 'staff', NULL, 'admin.jpg', '2026-03-30 11:48:13');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `campus`
--
ALTER TABLE `campus`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `external_user`
--
ALTER TABLE `external_user`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follower_id`,`following_id`),
  ADD KEY `following_id` (`following_id`);

--
-- Index pour la table `job_offers`
--
ALTER TABLE `job_offers`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`post_id`),
  ADD KEY `post_id` (`post_id`);

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Index pour la table `news_ynov`
--
ALTER TABLE `news_ynov`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campus_id` (`campus_id`);

--
-- Index pour la table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `portfolio`
--
ALTER TABLE `portfolio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`);

--
-- Index pour la table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `project_members`
--
ALTER TABLE `project_members`
  ADD PRIMARY KEY (`project_id`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campus_id` (`campus_id`);

--
-- Index pour la table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campus_id` (`campus_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `campus`
--
ALTER TABLE `campus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT pour la table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `job_offers`
--
ALTER TABLE `job_offers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `news_ynov`
--
ALTER TABLE `news_ynov`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `portfolio`
--
ALTER TABLE `portfolio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `skills`
--
ALTER TABLE `skills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `external_user`
--
ALTER TABLE `external_user`
  ADD CONSTRAINT `external_user_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`);

--
-- Contraintes pour la table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `news_ynov`
--
ALTER TABLE `news_ynov`
  ADD CONSTRAINT `news_ynov_ibfk_1` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`id`);

--
-- Contraintes pour la table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `portfolio`
--
ALTER TABLE `portfolio`
  ADD CONSTRAINT `portfolio_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `project_members`
--
ALTER TABLE `project_members`
  ADD CONSTRAINT `project_members_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  ADD CONSTRAINT `project_members_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `skills`
--
ALTER TABLE `skills`
  ADD CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`id`);

--
-- Contraintes pour la table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `student_ibfk_2` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,       -- Celui qui ajoute
    contact_id INT NOT NULL,    -- Celui qui est ajouté
    status ENUM('pending', 'accepted') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_friendship (user_id, contact_id) -- Évite les doublons
);