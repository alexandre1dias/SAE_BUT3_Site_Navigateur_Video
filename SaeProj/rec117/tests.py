import datetime
import json
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import infos_video
from .models import Artiste, Extrait, Interview, Question


class AnalyseUrlTests(TestCase):
    def test_formats_youtube(self):
        for url in ['https://www.youtube.com/watch?v=1NYQ65FTEC8&t=10s', 'https://youtu.be/1NYQ65FTEC8',
                    'youtube.com/shorts/1NYQ65FTEC8', 'https://m.youtube.com/watch?v=1NYQ65FTEC8',
                    'https://www.youtube.com/embed/1NYQ65FTEC8']:
            self.assertEqual(infos_video.analyser_url(url), ('youtube', '1NYQ65FTEC8'), url)

    def test_formats_vimeo(self):
        self.assertEqual(infos_video.analyser_url('https://vimeo.com/1128762950'), ('vimeo', '1128762950'))
        self.assertEqual(infos_video.analyser_url('https://player.vimeo.com/video/1128762950?h=ab12cd34ef'),
                         ('vimeo', '1128762950/ab12cd34ef'))
        self.assertEqual(infos_video.analyser_url('https://vimeo.com/1128762950/ab12cd34ef'),
                         ('vimeo', '1128762950/ab12cd34ef'))

    def test_url_inconnue(self):
        self.assertEqual(infos_video.analyser_url('https://example.com/video'), (None, None))


PAGE_YOUTUBE = '''<html><meta property="og:title" content="Interview Rivkah">
<script>var ytInitialPlayerResponse = {"videoDetails":{"videoId":"1NYQ65FTEC8","lengthSeconds":"253",
"shortDescription":"Rivkah parle de son univers.\\nBonne \\u00e9coute !","author":"Studio"},
"microformat":{"playerMicroformatRenderer":{"publishDate":"2025-01-15T02:00:00-08:00"}}};</script></html>'''


def faux_reseau(adresse):
    if 'youtube.com/oembed' in adresse:
        return json.dumps({'title': 'Interview Rivkah - rec117', 'author_name': 'Studio Orléans',
                           'thumbnail_url': 'https://i.ytimg.com/vi/1NYQ65FTEC8/hqdefault.jpg'})
    if 'youtube.com/watch' in adresse:
        return PAGE_YOUTUBE
    if 'vimeo.com/api/oembed' in adresse:
        return json.dumps({'title': 'Gontard extrait', 'author_name': 'Studio', 'duration': 95,
                           'description': 'Description Vimeo', 'upload_date': '2025-02-01 10:00:00',
                           'thumbnail_url': 'https://i.vimeocdn.com/video/123-d_295x166'})
    raise OSError('pas de réseau')


@mock.patch.object(infos_video, '_telecharger', side_effect=faux_reseau)
class RecupererInfosTests(TestCase):
    def test_youtube(self, _):
        infos = infos_video.recuperer_infos('https://www.youtube.com/watch?v=1NYQ65FTEC8')
        self.assertEqual(infos['url'], 'https://youtu.be/1NYQ65FTEC8')
        self.assertEqual(infos['titre'], 'Interview Rivkah - rec117')
        self.assertEqual(infos['auteur'], 'Studio Orléans')
        self.assertEqual(infos['duree'], 253)
        self.assertEqual(infos['description'], 'Rivkah parle de son univers.\nBonne écoute !')
        self.assertEqual(infos['date'], datetime.date(2025, 1, 15))
        self.assertIsNone(infos['erreur'])

    def test_vimeo(self, _):
        infos = infos_video.recuperer_infos('https://vimeo.com/1128786403')
        self.assertEqual(infos['duree'], 95)
        self.assertEqual(infos['date'], datetime.date(2025, 2, 1))
        self.assertEqual(infos['description'], 'Description Vimeo')


class SansReseauTests(TestCase):
    @mock.patch.object(infos_video, '_telecharger', side_effect=OSError)
    def test_sans_reseau(self, _):
        infos = infos_video.recuperer_infos('https://youtu.be/1NYQ65FTEC8')
        self.assertIsNone(infos['titre'])
        self.assertTrue(infos['erreur'])
        # La miniature YouTube se déduit de l'identifiant, même sans réseau
        self.assertEqual(infos['miniature'], 'https://i.ytimg.com/vi/1NYQ65FTEC8/hqdefault.jpg')


@mock.patch.object(infos_video, '_telecharger', side_effect=faux_reseau)
@mock.patch('rec117.templatetags.videos.miniature_oembed', return_value='')
class PageAdministrationTests(TestCase):
    def setUp(self):
        self.rivkah = Artiste.objects.create(nomArtiste='Rivkah')
        self.question = Question.objects.create(texteQuestion='Présentation')
        self.admin = User.objects.create_user('chef', password='x', is_staff=True)

    def test_acces_reserve_au_staff(self, *_):
        url = reverse('admin_videos')
        self.assertRedirects(self.client.get(url), reverse('admin_connexion') + '?next=' + url)
        User.objects.create_user('visiteur', password='x')
        self.client.login(username='visiteur', password='x')
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.login(username='chef', password='x')
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_bouton_admin_visible_uniquement_au_staff(self, *_):
        url = reverse('admin_videos')
        self.assertNotContains(self.client.get(reverse('mind_map')), url)
        self.client.force_login(User.objects.create_user('visiteur', password='x'))
        self.assertNotContains(self.client.get(reverse('mind_map')), url)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('mind_map')), url)

    def test_inscription_cree_un_compte_non_staff(self, *_):
        from .forms import InscriptionForm

        self.assertEqual(set(InscriptionForm().fields), {'username', 'password1', 'password2'})
        response = self.client.post(reverse('inscription'), {
            'username': 'nouveau',
            'password1': 'MotDePasse-solide-123',
            'password2': 'MotDePasse-solide-123',
            'is_staff': 'on',
            'is_superuser': 'on',
        })
        self.assertRedirects(response, reverse('home'))
        utilisateur = User.objects.get(username='nouveau')
        self.assertFalse(utilisateur.is_staff)
        self.assertFalse(utilisateur.is_superuser)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_compte_standard_peut_se_connecter_et_se_deconnecter(self, *_):
        User.objects.create_user('visiteur', password='MotDePasse-solide-123')
        reponse = self.client.post(reverse('connexion'), {
            'username': 'visiteur',
            'password': 'MotDePasse-solide-123',
        })
        self.assertRedirects(reponse, reverse('home'))
        self.assertTrue(self.client.get(reverse('home')).wsgi_request.user.is_authenticated)

        reponse = self.client.post(reverse('deconnexion'))
        self.assertRedirects(reponse, reverse('home'))
        self.assertFalse(self.client.get(reverse('home')).wsgi_request.user.is_authenticated)

    def test_formulaire_pre_rempli(self, *_):
        self.client.force_login(self.admin)
        reponse = self.client.get(reverse('admin_ajouter', args=['interview']),
                                  {'url': 'https://www.youtube.com/watch?v=1NYQ65FTEC8'})
        form = reponse.context['form']
        self.assertEqual(form.initial['titreInterview'], 'Interview Rivkah - rec117')
        self.assertEqual(form.initial['artiste'], self.rivkah.pk)  # nom trouvé dans le titre
        self.assertEqual(form.initial['urlYoutube'], 'https://youtu.be/1NYQ65FTEC8')
        self.assertEqual(form.initial['duree'], 253)
        self.assertContains(reponse, '4:13')
        self.assertNotIn('lieu', reponse.context['auto'])

    def test_ajout_modification_suppression(self, *_):
        self.client.force_login(self.admin)
        reponse = self.client.post(reverse('admin_ajouter', args=['interview']), {
            'titreInterview': 'Interview Zed', 'urlVimeo': 'https://vimeo.com/1', 'duree': '1:02:03',
            'nouvel_artiste': 'Zed', 'nouveau_lieu': 'Salle', 'ville_nouveau_lieu': 'Tours',
            'pays_nouveau_lieu': 'France',
        })
        self.assertRedirects(reponse, reverse('admin_videos'))
        interview = Interview.objects.get(titreInterview='Interview Zed')
        self.assertEqual(interview.duree, 3723)
        self.assertEqual(interview.artiste.nomArtiste, 'Zed')
        self.assertEqual(interview.lieu.villeLieu, 'Tours')

        # Extrait : numéro automatique et nouvelle question
        self.client.post(reverse('admin_ajouter', args=['extrait']), {
            'titreExtrait': 'Zed 1', 'interview': interview.pk, 'nouvelle_question': 'Pourquoi ?',
        })
        self.client.post(reverse('admin_ajouter', args=['extrait']), {
            'titreExtrait': 'Zed 2', 'interview': interview.pk, 'question': self.question.pk,
        })
        self.assertEqual([e.ordreSequence for e in interview.extraits.all()], [1, 2])

        extrait = Extrait.objects.get(titreExtrait='Zed 2')
        self.client.post(reverse('admin_modifier', args=['extrait', extrait.pk]), {
            'titreExtrait': 'Zed 2 bis', 'interview': interview.pk, 'question': self.question.pk,
            'ordreSequence': 2, 'timecodeDebut': '0:30', 'timecodeFin': '1:00',
        })
        extrait.refresh_from_db()
        self.assertEqual((extrait.titreExtrait, extrait.timecodeDebut, extrait.timecodeFin), ('Zed 2 bis', 30, 60))

        # Suppression : confirmation d'abord, puis suppression en cascade des extraits
        url = reverse('admin_supprimer', args=['interview', interview.pk])
        self.assertContains(self.client.get(url), '2 extraits')
        self.assertTrue(Interview.objects.filter(pk=interview.pk).exists())
        self.client.post(url)
        self.assertFalse(Interview.objects.filter(pk=interview.pk).exists())
        self.assertFalse(Extrait.objects.exists())

    def test_erreurs(self, *_):
        self.client.force_login(self.admin)
        reponse = self.client.post(reverse('admin_ajouter', args=['interview']), {'titreInterview': 'X'})
        self.assertEqual(reponse.status_code, 200)
        self.assertIn('artiste', reponse.context['form'].errors)
        self.assertIn('urlYoutube', reponse.context['form'].errors)
        self.assertFalse(Interview.objects.exists())
