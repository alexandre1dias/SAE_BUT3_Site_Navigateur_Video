from datetime import datetime, timedelta
from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Artiste, Extrait, Interview, Question, Utilisateur


class UtilisateurTestCase(Neo4jTestCase):

    def make_user(
        self, pseudo="user1", prenom="P", nom="N", email="u@example.com", password="pwd"
    ):
        return Utilisateur(
            pseudo=pseudo, prenom=prenom, nom=nom, email=email, password=password
        ).save()

    def test_creation_utilisateur_and_defaults(self):
        """Création d'un utilisateur et valeurs par défaut"""
        u = self.make_user()
        self.assertIsNotNone(u.uuid)
        self.assertEqual(u.pseudo, "user1")
        self.assertFalse(u.is_admin)

    def test_unique_constraints_pseudo_and_email(self):
        """Pseudo et email doivent être uniques"""
        self.make_user(pseudo="unique", email="unique@example.com")
        with self.assertRaises(UniqueProperty):
            # même pseudo
            self.make_user(pseudo="unique", email="other@example.com")
        with self.assertRaises(UniqueProperty):
            # même email
            self.make_user(pseudo="other", email="unique@example.com")

    def test_update_fields_and_persistence(self):
        """Mise à jour des champs et rechargement depuis la DB"""
        u = self.make_user(
            pseudo="tmp", email="tmp@example.com", prenom="Jean", nom="Dup"
        )
        u.prenom = "Jean-Baptiste"
        u.is_admin = True
        u.save()

        reloaded = Utilisateur.nodes.get(uuid=u.uuid)
        self.assertEqual(reloaded.prenom, "Jean-Baptiste")
        self.assertTrue(reloaded.is_admin)

    def test_delete_utilisateur(self):
        """Suppression d'un utilisateur"""
        u = self.make_user(pseudo="todelete", email="td@example.com")
        uuid = u.uuid
        u.delete()
        with self.assertRaises(DoesNotExist):
            Utilisateur.nodes.get(uuid=uuid)

    def test_recherches_artistes_connect_with_dateheure_default(self):
        """Connecter un artiste via recherches_artistes et vérifier la propriété date_heure par défaut"""
        u = self.make_user(pseudo="searcher", email="s@example.com")
        a = Artiste(name="Art1").save()

        # Connect sans fournir date_heure => default_now doit remplir la valeur
        u.recherches_artistes.connect(a)

        rel = u.recherches_artistes.relationship(a)
        self.assertIsNotNone(rel)
        self.assertTrue(hasattr(rel, "date_heure"))
        self.assertIsInstance(rel.date_heure, datetime)

        # relation count
        self.assertEqual(len(u.recherches_artistes.all()), 1)

    def test_recherches_artistes_connect_with_custom_date(self):
        """Connecter avec une date_heure fournie explicitement"""
        from datetime import timezone

        u = self.make_user(pseudo="searcher2", email="s2@example.com")
        a = Artiste(name="Art2").save()

        # custom_dt défini comme datetime "aware" en UTC
        custom_dt = datetime.now(timezone.utc) - timedelta(days=1)
        u.recherches_artistes.connect(a, {"date_heure": custom_dt})

        rel = u.recherches_artistes.relationship(a)
        self.assertIsInstance(rel.date_heure, datetime)

        # normalise les deux datetimes pour comparaison sans erreur
        rel_dt = rel.date_heure
        if rel_dt.tzinfo is not None:
            custom_dt = custom_dt.astimezone(rel_dt.tzinfo)
        else:
            rel_dt = rel_dt.replace(tzinfo=None)
            custom_dt = custom_dt.replace(tzinfo=None)

        delta = abs((rel_dt - custom_dt).total_seconds())
        self.assertLess(delta, 5.0)

    def test_multiple_relations_and_counts(self):
        """Vérifier qu'on peut connecter plusieurs cibles pour chaque relation et compter"""
        u = self.make_user(pseudo="multi", email="multi@example.com")
        a1 = Artiste(name="A1").save()
        a2 = Artiste(name="A2").save()
        i1 = Interview(titre="I1").save()
        e1 = Extrait(titre="E1", duree="10").save()
        q1 = Question(texte="Q1").save()

        u.recherches_artistes.connect(a1)
        u.recherches_artistes.connect(a2)
        u.regarder_interviews.connect(i1)
        u.regarder_extraits.connect(e1)
        u.recherches_questions.connect(q1)

        self.assertCountEqual(
            [x.name for x in u.recherches_artistes.all()], ["A1", "A2"]
        )
        self.assertEqual(len(u.regarder_interviews.all()), 1)
        self.assertEqual(len(u.regarder_extraits.all()), 1)
        self.assertEqual(len(u.recherches_questions.all()), 1)

    def test_disconnect_relation_and_verify(self):
        """Déconnecter une relation et vérifier qu'elle a disparu (les noeuds cibles subsistent)"""
        u = self.make_user(pseudo="dcon", email="dcon@example.com")
        a = Artiste(name="Solo").save()
        u.recherches_artistes.connect(a)
        # confirme existance
        self.assertEqual(len(u.recherches_artistes.all()), 1)

        # disconnect
        u.recherches_artistes.disconnect(a)
        self.assertEqual(len(u.recherches_artistes.all()), 0)

        # l'artiste doit toujours exister
        arts = Artiste.nodes.filter(name="Solo")
        self.assertEqual(len(arts), 1)

    def test_relation_property_read_after_reload(self):
        """Vérifier que la propriété de la relation est lisible après rechargement du noeud utilisateur"""
        u = self.make_user(pseudo="reload", email="reload@example.com")
        a = Artiste(name="ReloadArt").save()
        u.recherches_artistes.connect(a)

        # reload user from DB to simulate fresh instance
        u2 = Utilisateur.nodes.get(uuid=u.uuid)
        rel = u2.recherches_artistes.relationship(a)
        self.assertIsNotNone(rel)
        self.assertIsInstance(rel.date_heure, datetime)

    def test_filtering_by_pseudo_and_email(self):
        """Rechercher l'utilisateur via nodes.filter sur pseudo (db_property='name') et email"""
        self.make_user(pseudo="finder", email="finder@example.com")
        found_by_pseudo = Utilisateur.nodes.filter(pseudo="finder")
        found_by_email = Utilisateur.nodes.filter(email="finder@example.com")
        self.assertEqual(len(found_by_pseudo), 1)
        self.assertEqual(len(found_by_email), 1)
        self.assertEqual(found_by_pseudo[0].email, "finder@example.com")
