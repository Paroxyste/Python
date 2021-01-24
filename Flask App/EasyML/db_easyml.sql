-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : Dim 24 jan. 2021 à 09:40
-- Version du serveur :  10.4.17-MariaDB-cll-lve
-- Version de PHP : 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db_easyml`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name_en` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `name_fr` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `tag` char(4) CHARACTER SET utf8mb4 NOT NULL,
  `icon` varchar(30) CHARACTER SET utf8mb4 NOT NULL,
  `description_en` text CHARACTER SET utf8mb4 NOT NULL,
  `description_fr` text CHARACTER SET utf8mb4 NOT NULL,
  `link` varchar(35) CHARACTER SET utf8mb4 NOT NULL,
  `wiki_link_en` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `wiki_link_fr` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id`, `name_en`, `name_fr`, `tag`, `icon`, `description_en`, `description_fr`, `link`, `wiki_link_en`, `wiki_link_fr`) VALUES
(1, 'Dashboard', 'Tableau de bord', 'HOME', 'feather icon-home', 'Dashboard', 'Tableau de bord', 'main.home', NULL, NULL),
(2, 'Exploratory Analysis', 'Analyse Exploratoire', 'AE', 'feather icon-search', 'Exploratory Analysis', 'Analyse Exploratoire', 'exp.exploratory_analysis', NULL, NULL),
(3, 'Regression Analysis', 'Analyse de Régression', 'REG', 'feather icon-trending-down', 'Regression analysis is a set of statistical methods used for the estimation of relationships between a dependent variable and one or more independent variables. It can be utilized to assess the strength of the relationship between variables and for modeling the future relationship between them. Regression analysis includes several variations, such as linear, multiple linear, and nonlinear. The most common models are simple linear and multiple linear. Nonlinear regression analysis is commonly used for more complicated data sets in which the dependent and independent variables show a nonlinear relationship. Regression analysis offers numerous applications in various disciplines, including finance. ', 'L\'analyse de régression est un ensemble de méthodes statistiques utilisées pour l\'estimation des relations entre une variable dépendante et une ou plusieurs variables indépendantes. Elle peut être utilisée pour évaluer la force de la relation entre les variables et pour modéliser la relation future entre elles. L\'analyse de régression comprend plusieurs variations, telles que linéaire, linéaire multiple et non linéaire. Les modèles les plus courants sont les modèles linéaires simples et les modèles linéaires multiples. L\'analyse de régression non linéaire est couramment utilisée pour des ensembles de données plus complexes dans lesquels les variables dépendantes et indépendantes présentent une relation non linéaire. L\'analyse de régression offre de nombreuses applications dans diverses disciplines, dont la finance.', 'reg.regression_category', 'https://en.wikipedia.org/wiki/Regression_analysis', 'https://fr.wikipedia.org/wiki/R%C3%A9gression_(statistiques)'),
(4, 'Cluster Analysis', 'Méthodes de Regroupement', 'CLU', 'feather icon-share-2', 'Cluster analysis involves formulating a problem, selecting a distance measure, selecting a clustering procedure, deciding the number of clusters, interpreting the profile clusters and finally, assessing the validity of clustering. The variables on which the cluster analysis is to be done should be selected by keeping past research in mind. It should also be selected by theory, the hypotheses being tested, and the judgment of the researcher. An appropriate measure of distance or similarity should be selected; the most commonly used measure is the Euclidean distance or its square. Cluster Analysis has been used in marketing for various purposes. Segmentation of consumers in cluster analysis is used on the basis of benefits sought from the purchase of the product. It can be used to identify homogeneous groups of buyers. ', 'L\'analyse des clusters consiste à formuler un problème, à choisir une mesure de distance, à sélectionner une procédure de regroupement, à décider du nombre de clusters, à interpréter les clusters de profil et enfin, à évaluer la validité du regroupement. Les variables sur lesquelles l\'analyse par grappes doit être effectuée doivent être sélectionnées en gardant à l\'esprit les recherches antérieures. Elles doivent également être sélectionnées en fonction de la théorie, des hypothèses testées et du jugement du chercheur. Une mesure appropriée de la distance ou de la similarité doit être choisie ; la mesure la plus couramment utilisée est la distance euclidienne ou son carré. L\'analyse des grappes a été utilisée dans le marketing à des fins diverses. La segmentation des consommateurs dans l\'analyse par grappes est utilisée sur la base des avantages recherchés lors de l\'achat du produit. Elle peut être utilisée pour identifier des groupes homogènes d\'acheteurs.', 'clust.clustering_category', 'https://en.wikipedia.org/wiki/Cluster_analysis', 'https://fr.wikipedia.org/wiki/Partitionnement_de_donn%C3%A9es'),
(5, 'Reinforcement Learning', 'Apprentissage par Renforcement', 'RL', 'feather icon-cpu', 'Reinforcement learning is the training of machine learning models to make a sequence of decisions. The agent learns to achieve a goal in an uncertain, potentially complex environment. In reinforcement learning, an artificial intelligence faces a game-like situation. The computer employs trial and error to come up with a solution to the problem. To get the machine to do what the programmer wants, the artificial intelligence gets either rewards or penalties for the actions it performs. Its goal is to maximize the total reward. Although the designer sets the reward policy–that is, the rules of the game–he gives the model no hints or suggestions for how to solve the game. It’s up to the model to figure out how to perform the task to maximize the reward, starting from totally random trials and finishing with sophisticated tactics and superhuman skills. By leveraging the power of search and many trials, reinforcement learning is currently the most effective way to hint machine’s creativity. In contrast to human beings, artificial intelligence can gather experience from thousands of parallel gameplays if a reinforcement learning algorithm is run on a sufficiently powerful computer infrastructure. ', 'L\'apprentissage par renforcement est la formation de modèles d\'apprentissage machine pour prendre une séquence de décisions. L\'agent apprend à atteindre un objectif dans un environnement incertain et potentiellement complexe. Dans l\'apprentissage par renforcement, une intelligence artificielle est confrontée à une situation de jeu. L\'ordinateur fait des essais et des erreurs pour trouver une solution au problème. Pour amener la machine à faire ce que le programmeur veut, l\'intelligence artificielle reçoit soit des récompenses, soit des pénalités pour les actions qu\'elle accomplit. Son but est de maximiser la récompense totale. Bien que le concepteur définisse la politique de récompense - c\'est-à-dire les règles du jeu - il ne donne au modèle aucune indication ou suggestion sur la façon de résoudre le jeu. C\'est au modèle de trouver comment exécuter la tâche pour maximiser la récompense, en commençant par des essais totalement aléatoires et en terminant par des tactiques sophistiquées et des compétences surhumaines. En exploitant la puissance de la recherche et des nombreux essais, l\'apprentissage par renforcement est actuellement le moyen le plus efficace de faire des allusions à la créativité de la machine. Contrairement aux êtres humains, l\'intelligence artificielle peut acquérir de l\'expérience à partir de milliers de jeux parallèles si un algorithme d\'apprentissage par renforcement est exécuté sur une infrastructure informatique suffisamment puissante.', 'rf.rein_forc_learn_cat', 'https://en.wikipedia.org/wiki/Reinforcement_learning', 'https://fr.wikipedia.org/wiki/Apprentissage_par_renforcement');

-- --------------------------------------------------------

--
-- Structure de la table `favorite`
--

CREATE TABLE `favorite` (
  `id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `models_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `models_cat`
--

CREATE TABLE `models_cat` (
  `id` int(11) NOT NULL,
  `name_en` char(55) NOT NULL,
  `name_fr` char(55) NOT NULL,
  `tag` char(4) NOT NULL,
  `description_en` tinytext NOT NULL,
  `description_fr` tinytext NOT NULL,
  `link` varchar(55) NOT NULL,
  `image` varchar(35) NOT NULL,
  `favorite` enum('yes','no') NOT NULL DEFAULT 'no',
  `id_categories` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `models_cat`
--

INSERT INTO `models_cat` (`id`, `name_en`, `name_fr`, `tag`, `description_en`, `description_fr`, `link`, `image`, `favorite`, `id_categories`) VALUES
(1, 'Simple Linear Regression', 'Régression Linéaire Simple', 'SLR', 'Simple linear regression examines the relationship between an independent variable (X axis) and a dependent variable (Y axis).', 'La régression linéaire simple examine la relation entre une variable indépendante (axe X), et une variable dépendante (axe Y).', 'reg.simple_linear_regression', 'images/cards/regression/1.jpg', 'no', 3),
(2, 'Multiple Linear Regression', 'Régression Linéaire Multiple', 'MLR', 'Multiple linear regression examines the relationship between several independent variables (X axis), and one dependent variable (Y axis).', 'La régression linéaire multiple examine la relation entre plusieurs variables indépendante (axe X), et une variable dépendante (axe Y).', 'reg.multiple_linear_regression', 'images/cards/regression/2.jpg', 'no', 3),
(3, 'Polynomial Regression', 'Régression Polynomiale', 'PR', 'Polynomial regression a form of regression in which the relationship between the independent variable (X-axis) and the dependent variable (Y-axis) is modeled in the polynomial of the Nth degree.', 'La régression polynomiale une forme de régression dans laquelle la relation entre la variable indépendante (axe X) et la variable dépendante (axe Y) sont modélisées dans le polynôme du Nième degrés.', 'reg.polynomial_regression', 'images/cards/regression/3.jpg', 'no', 3),
(4, 'K-Means Clustering', ' K-Moyennes', 'KMC', 'K-means clustering is used when you have data that is not categorized. The purpose of this algorithm is to find groups often called clusters.', 'Le regroupement K-means est utilisé lorsque vous avez des données non catégorisé. Le but de cet algorithme est de trouver des groupes souvent appelés clusters.', 'clust.k_means_clustering', 'images/cards/clustering/4.jpg', 'no', 4),
(5, 'Hierarchical Clustering', 'Regroupement Hiérarchique', 'HC', 'Hierarchical clustering an automatic classification method used from a set of N individuals, whose purpose is to divide them into a number of classes.', 'Le regroupement hierarchique une méthode de classification automatique utilisée à partir d\'un ensemble de N individus, dont le but est de les répartir dans un certain nombre de classes.', 'clust.hierarchical_clustering', 'images/cards/clustering/5.jpg', 'no', 4),
(6, 'Upper Confidence Bound', 'Limite de Confiance Supérieure', 'UCB', 'The Upper Confidence Bound is an algorithm that allows the user to choose actions by modifying his exploration-operation balance as he gains more knowledge about the environment.', 'La limite de confiance supérieure est un algorithme permettant de choisir des actions en modifiant son équilibre exploration-exploitation à mesure qu\'il acquiert plus de connaissances sur l\'environnement.', 'rf.upper_confidence_bound', 'images/cards/rl/6.jpg', 'no', 5),
(7, 'Thompson Sampling', 'Échantillonnage de Thompson', 'TS', 'Thompson\'s sampling is a heuristic algorithm for selecting actions that solve the exploration-exploitation dilemma.', 'L\'échantillonnage de Thompson est un algorithme heuristique permettant de choisir des actions qui résolvent le dilemme exploration-exploitation.', 'rf.thompson_sampling', 'images/cards/rl/7.jpg', 'no', 5);

-- --------------------------------------------------------

--
-- Structure de la table `settings`
--

CREATE TABLE `settings` (
  `id` int(11) NOT NULL,
  `name_en` char(15) NOT NULL,
  `name_fr` char(15) NOT NULL,
  `icon` varchar(25) NOT NULL,
  `link` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `settings`
--

INSERT INTO `settings` (`id`, `name_en`, `name_fr`, `icon`, `link`) VALUES
(1, 'Settings', 'Paramètres', 'feather icon-settings', 'users.settings'),
(2, 'Logout', 'Déconnexion', 'feather icon-log-out', 'users.logout');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `register_date` datetime NOT NULL,
  `lang` enum('EN','FR') NOT NULL DEFAULT 'EN',
  `last_connection` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `favorite`
--
ALTER TABLE `favorite`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_id` (`users_id`),
  ADD KEY `models_id` (`models_id`);

--
-- Index pour la table `models_cat`
--
ALTER TABLE `models_cat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_categories` (`id_categories`);

--
-- Index pour la table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `favorite`
--
ALTER TABLE `favorite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `models_cat`
--
ALTER TABLE `models_cat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `favorite`
--
ALTER TABLE `favorite`
  ADD CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `favorite_ibfk_2` FOREIGN KEY (`models_id`) REFERENCES `models_cat` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `models_cat`
--
ALTER TABLE `models_cat`
  ADD CONSTRAINT `models_cat_ibfk_1` FOREIGN KEY (`id_categories`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
