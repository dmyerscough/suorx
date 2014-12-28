# -*- coding: utf-8 -*-

from django.test import TestCase
from shortner import UrlShortner
from suorx import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class UrlShortnerTest(TestCase):

    def setUp(self):
        '''

        '''
        self.url = UrlShortner()

    def test_urls(self):
        '''
        Ensure specific URL's always return consistent results
        '''
        urls = {'google.com': 'P7',
                'www.google.com': 'MO',
                'https://www.example.com': 'Ua',
                'http://www.facebook.com': 'JA',
                'http://www.google.com/about.html': 'KR'}

        for url, idx in urls.items():
            self.assertEqual(self.url.encode(url), idx)

    def test_invalid_url(self):
        '''

        '''
        pass

    def test_duplicates(self):
        '''
        Ensure that web addresses with the same character value don't generate
        the same shorten url
        '''
        self.assertNotEqual(self.url.encode('www.pod.com'),
                            self.url.encode('www.dop.com'))

    def test_invalid_chars(self):
        '''
        Ensure an exception is throw if we don't supply a string or an integer
        value
        '''
        self.assertRaises(TypeError,
                          'You must supply either a string or an integer',
                          self.url.encode(b'abc'))


class NewVisitor(TestCase):

    def setUp(self):
        '''

        '''
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        '''

        '''
        self.browser.quit()

    def test_shorten_url(self):
        '''

        '''
        self.browser.get('http://localhost:8000')

        inputbox = self.browser.find_element_by_id('urlinput')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Paste a link to shorten it...'
        )

        inputbox.send_keys('www.google.com')
        inputbox.send_keys(Keys.ENTER)

        url = self.browser.find_element_by_id('url')

        self.assertEqual('/'.join([settings.DOMAIN, 'Lt']), url.text)
