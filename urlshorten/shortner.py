# -*- coding: utf-8 -*-

import hashlib

class UrlShortner(object):

    def __init__(self):
        '''

        '''
        self.chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def __encode(self, idx):
        '''
        Convert a number into a unique string ( Bijective Function )
        '''
        url = ''

        if idx == 0:
            return self.chars[0]

        while idx > 0:
            url += self.chars[idx % len(self.chars)]
            idx /= len(self.chars)

        return url[::-1]

    def encode(self, uid):
        '''
        Iterate over a url and encode the URL into a unique shorten url
        '''
        if isinstance(uid, int):
            return self.__encode(uid)
        elif isinstance(uid, str) or isinstance(uid, unicode):
            site = 0
            for i in hashlib.sha256(uid).hexdigest():
                if i.isalpha():
                    site += ord(i)
                elif i.isdigit():
                    site += int(i)
        else:
            raise TypeError('You must supply either a string or an integer')

        return self.__encode(site * 1987)
