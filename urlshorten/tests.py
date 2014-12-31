# -*- coding: utf-8 -*-

from django.test import TestCase
from shortner import UrlShortner
from suorx import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


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

    def test_shorten_url(self):
        '''

        '''
        browser = webdriver.Firefox()
        browser.implicitly_wait(3)

        browser.get('http://www.suorx.com')

        inputbox = browser.find_element_by_id('urlinput')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Paste a link to shorten it...'
        )

        inputbox.send_keys('www.google.com')
        inputbox.send_keys(Keys.ENTER)

        url = browser.find_element_by_id('url')

        time.sleep(2)

        self.assertEqual('/'.join(['http://' + settings.DOMAIN, 'Lt']), url.text)
        browser.quit()

    def test_language(self):
        '''

        '''
        languages = {'de': u'Link eintragen um diesen zu kürzen',
                     'fr': u'Copier un lien pour en réduire sa taille',
                     'id': u'Tempelkan link untuk diperpendek...',
                     'it': u'Incolla un link per abbreviarlo...',
                     'ja': u'短縮したいURLを入力してください。',
                     'ko': u'링크를 단축합시다...',
                     'ru': u'Вставьте ссылку, чтобы сделать её сократить...',
                     'sv': u'Klistra in en länk för att förkorta den',
                     'zh': u'将网址缩短...'}

        for lang, phrase in languages.items():
            profile = webdriver.FirefoxProfile()
            profile.set_preference('intl.accept_languages', lang)

            browser = webdriver.Firefox(firefox_profile=profile)
            browser.implicitly_wait(3)

            browser.get('http://www.suorx.com')

            inputbox = browser.find_element_by_id('urlinput')

            self.assertEqual(
                inputbox.get_attribute('placeholder'),
                phrase
            )

            inputbox.send_keys('www.google.com')
            inputbox.send_keys(Keys.ENTER)

            url = browser.find_element_by_id('url')
            time.sleep(2)

            self.assertEqual('/'.join(['http://' + settings.DOMAIN, 'Lt']), url.text)
            browser.quit()
