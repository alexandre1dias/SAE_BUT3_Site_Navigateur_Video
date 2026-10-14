-- Script de création des tables

DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS extrait;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS interview;
DROP TABLE IF EXISTS lieu;
DROP TABLE IF EXISTS artiste_genre;
DROP TABLE IF EXISTS artiste;
DROP TABLE IF EXISTS genre_musical;

CREATE TABLE genre_musical (
    id_genre INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_genre VARCHAR(100) NOT NULL,
    code_couleur VARCHAR(7) NOT NULL
);

CREATE TABLE artiste (
    id_artiste INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_artiste VARCHAR(150) NOT NULL
);

CREATE TABLE artiste_genre (
    id_artiste INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    PRIMARY KEY (id_artiste, id_genre),
    FOREIGN KEY (id_artiste) REFERENCES artiste(id_artiste) ON DELETE CASCADE,
    FOREIGN KEY (id_genre) REFERENCES genre_musical(id_genre) ON DELETE CASCADE
);

CREATE TABLE lieu (
    id_lieu INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_lieu VARCHAR(150) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    pays VARCHAR(100) NOT NULL
);

CREATE TABLE question (
    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    texte_question TEXT NOT NULL
);

CREATE TABLE interview (
    id_interview INTEGER PRIMARY KEY AUTOINCREMENT,
    titre_interview VARCHAR(200) NOT NULL,
    date_tournage DATE,
    description TEXT,
    url_youtube VARCHAR(255),
    url_vimeo VARCHAR(255),
    id_artiste INTEGER NOT NULL,
    id_lieu INTEGER,
    FOREIGN KEY (id_artiste) REFERENCES artiste(id_artiste) ON DELETE CASCADE,
    FOREIGN KEY (id_lieu) REFERENCES lieu(id_lieu) ON DELETE SET NULL
);

CREATE TABLE extrait (
    id_extrait INTEGER PRIMARY KEY AUTOINCREMENT,
    titre_extrait VARCHAR(200) NOT NULL,
    ordre_sequence INTEGER NOT NULL,
    timecode_debut INTEGER NOT NULL DEFAULT 0,
    timecode_fin INTEGER,
    url_youtube VARCHAR(255),
    url_vimeo VARCHAR(255),
    transcription TEXT,
    id_interview INTEGER NOT NULL,
    id_question INTEGER NOT NULL,
    FOREIGN KEY (id_interview) REFERENCES interview(id_interview) ON DELETE CASCADE,
    FOREIGN KEY (id_question) REFERENCES question(id_question) ON DELETE RESTRICT,
    CONSTRAINT uq_interview_ordre UNIQUE (id_interview, ordre_sequence)
);

CREATE TABLE utilisateur (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    lecteur_prefere VARCHAR(10) DEFAULT 'YOUTUBE' CHECK (lecteur_prefere IN ('YOUTUBE', 'VIMEO')),
    est_admin BOOLEAN NOT NULL DEFAULT 0
);