from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from parties.models import Competition, Party
from platforms.models import Platform
from productions.models import ProductionType


class TestShowCompetition(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        competition = Competition.objects.get(party__name="Forever 2e3", name="ZX 1K Intro")

        response = self.client.get('/competitions/%d/' % competition.id)
        self.assertEqual(response.status_code, 200)


class TestGetCompetitionHistory(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        competition = Competition.objects.get(party__name="Forever 2e3", name="ZX 1K Intro")

        response = self.client.get('/competitions/%d/history/' % competition.id)
        self.assertEqual(response.status_code, 200)


class TestEditCompetition(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.competition = Competition.objects.get(party__name="Forever 2e3", name="ZX 1K Intro")

    def test_get(self):
        response = self.client.get('/competitions/%d/edit' % self.competition.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/competitions/%d/edit' % self.competition.id, {
            'name': "Speccy 1K Intro",
            'shown_date': "18 march 2000",
            'platform': '',
            'production_type': '',
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertTrue(Competition.objects.filter(party__name="Forever 2e3", name="Speccy 1K Intro").exists())


class TestImportResults(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_superuser(username='testsuperuser', email='testsuperuser@example.com', password='12345')
        self.client.login(username='testsuperuser', password='12345')
        self.competition = Competition.objects.get(party__name="Forever 2e3", name="ZX 1K Intro")
        self.competition.placings.all().delete()
        self.competition.platform = Platform.objects.get(name='ZX Spectrum')
        self.competition.production_type = ProductionType.objects.get(name='1K Intro')
        self.competition.save()

    def test_non_superuser(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/competitions/%d/import_text' % self.competition.id)
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)

    def test_get(self):
        response = self.client.get('/competitions/%d/import_text' % self.competition.id)
        self.assertEqual(response.status_code, 200)

    def test_import_tsv(self):
        response = self.client.post('/competitions/%d/import_text' % self.competition.id, {
            'format': 'tsv',
            'results': """
1\tArtifice\tSerzhSoft\t108
2\tMadrielle\tGasman\t96
3\tMathricks\t3SC\t77
"""
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertEqual(self.competition.placings.count(), 3)

    def test_import_pm1(self):
        response = self.client.post('/competitions/%d/import_text' % self.competition.id, {
            'format': 'pm1',
            'results': """
01 108 Artifice - SerzhSoft
02  96 Madrielle - Gasman
03  77 Mathricks - 3SC
"""
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertEqual(self.competition.placings.count(), 3)

    def test_import_pm2(self):
        response = self.client.post('/competitions/%d/import_text' % self.competition.id, {
            'format': 'pm2',
            'results': """
01 108 Artifice by SerzhSoft
02  96 Madrielle by Gasman
03  77 Mathricks by 3SC
"""
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertEqual(self.competition.placings.count(), 3)

    def test_import_wuhu(self):
        response = self.client.post('/competitions/%d/import_text' % self.competition.id, {
            'format': 'wuhu',
            'results': """
    1.  #04   108 pts    Artifice - SerzhSoft
    2.  #05    96 pts    Madrielle - Gasman
    3.  #06    77 pts    Mathricks - 3SC
"""
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertEqual(self.competition.placings.count(), 3)

    def test_import_unknown_format(self):
        response = self.client.post('/competitions/%d/import_text' % self.competition.id, {
            'format': 'goose',
            'results': """
01 108 HONK HONK HONK
02  96 HONK honk HONK
03  77 HONK HONK honk HONK
"""
        })
        self.assertRedirects(response, '/competitions/%d/edit' % self.competition.id)
        self.assertEqual(self.competition.placings.count(), 0)


class TestDeleteCompetition(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_superuser(username='testsuperuser', email='testsuperuser@example.com', password='12345')
        self.client.login(username='testsuperuser', password='12345')
        self.competition = Competition.objects.get(party__name="Forever 2e3", name="ZX 1K Intro")

    def test_non_superuser(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/competitions/%d/delete/' % self.competition.id)
        self.assertRedirects(response, '/parties/%d/' % Party.objects.get(name='Forever 2e3').id)

    def test_cannot_delete_competition_with_placings(self):
        response = self.client.get('/competitions/%d/delete/' % self.competition.id)
        self.assertRedirects(response, '/parties/%d/' % Party.objects.get(name='Forever 2e3').id)

    def test_get(self):
        self.competition.placings.all().delete()
        response = self.client.get('/competitions/%d/delete/' % self.competition.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.competition.placings.all().delete()
        response = self.client.post('/competitions/%d/delete/' % self.competition.id, {'yes': 'yes'})
        self.assertRedirects(response, '/parties/%d/' % Party.objects.get(name='Forever 2e3').id)
        self.assertFalse(Competition.objects.filter(party__name="Forever 2e3", name="ZX 1K Intro").exists())

    def test_post_cancel(self):
        self.competition.placings.all().delete()
        response = self.client.post('/competitions/%d/delete/' % self.competition.id, {'no': 'no'})
        self.assertRedirects(response, '/parties/%d/' % Party.objects.get(name='Forever 2e3').id)
        self.assertTrue(Competition.objects.filter(party__name="Forever 2e3", name="ZX 1K Intro").exists())
