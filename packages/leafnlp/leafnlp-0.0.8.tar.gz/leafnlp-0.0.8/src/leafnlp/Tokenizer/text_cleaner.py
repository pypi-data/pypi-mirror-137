# Copyright 2021 The LeafNLP Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Base for Text Cleaner. 
This module is used to clean text before tokenization.
In many cases, sentence segmentation and word tokenization are affected by
URLs and other patterns that may not be necessary. Therefore, in leafnlp,
We replace these tokens with @name.
"""
from .utils.utils import reduce_lengthening
import re


class TextCleanerBase(object):
    r"""
    This is the base for text cleaner.

    Args
        - ``preserve_url`` (:obj:`bool`, optional): *Default*: False

    If True, keep URL. Otherwise, change URL to @url.

        - ``preserve_phone`` (:obj:`bool`, optional): *Default*: False

    If True, keep URL. Otherwise, change URL to @phone.

        - ``preserve_email`` (:obj:`bool`, optional): *Default*: False

    If True, keep URL. Otherwise, change URL to @email.
    """

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False):

        self.preserve_url = preserve_url
        self.preserve_email = preserve_email
        self.preserve_phone = preserve_phone

        # URLs
        self.URL = r"((https?:\/\/|www)|\w+\.(\w{2-3}))([\w\!#$&-;=\?\-\[\]~]|%[0-9a-fA-F]{2})+"
        self.URL_RE = re.compile(self.URL, re.UNICODE)
        # phone numbers
        self.PHONE = r"(?:(?:\+?[01][\-\s.]*)?(?:[\(]?\d{3}[\-\s.\)\/]*)?\d{3}[\-\s.]*\d{4})"
        self.PHONE_RE = re.compile(self.PHONE, re.UNICODE)
        # email addresses
        self.EMAILS = r"[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]"
        self.EMAILS_RE = re.compile(self.EMAILS, re.UNICODE)

        self.DOMAINS = self.domain_rules()

    def domain_rules(self):
        r"""
        Add domain specific rules.

        Return
            - ``output`` {"key1": "rule 1", "key2": "rule 2"}

        """
        output = {}

        return output

    def annotate(self, text):
        r"""
        Begin to clean texts.

        Args
            - ``text`` (:obj:`str`): Input text.

        Return:
            - ``text`` (:obj:`str`): Output text.
        """
        if not self.preserve_url:
            text = re.sub(self.URL_RE, ' @url ', text)
        if not self.preserve_phone:
            text = re.sub(self.PHONE_RE, ' @phone ', text)
        if not self.preserve_email:
            text = re.sub(self.EMAILS_RE, ' @email ', text)

        for key in self.DOMAINS:
            text = re.sub(self.DOMAINS[key], ' @{} '.format(key), text)

        return text


class NewsCleaner(TextCleanerBase):

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False):

        super().__init__(preserve_url=preserve_url,
                         preserve_phone=preserve_phone,
                         preserve_email=preserve_email)


class TweetCleaner(TextCleanerBase):

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False,
                 preserve_user=False):

        self.preserve_user = preserve_user
        super().__init__(preserve_url=preserve_url,
                         preserve_phone=preserve_phone,
                         preserve_email=preserve_email)

    def domain_rules(self):
        r"""
        Add domain specific rules for tweets.

        Return
            - ``rules`` {"key1": "rule 1", "key2": "rule 2"}

        """
        rules = {}
        if not self.preserve_user:
            self.TWITTER_USER = r"(?:@\w+)"
            self.TWITTER_USER_RE = re.compile(self.TWITTER_USER, re.UNICODE)

            rules["user"] = self.TWITTER_USER_RE

        return rules

    def annotate(self, text):
        r"""
        Begin to clean texts.

        Args
            - ``text`` (:obj:`str`): Input text.

        Return:
            - ``text`` (:obj:`str`): Output text.

        """
        text = super().annotate(text)
        text = reduce_lengthening(text)

        return text


class ClinicalNoteCleaner(TextCleanerBase):

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False, 
                 preserve_anony_name_entity=False):

        self.preserve_anony_name_entity = preserve_anony_name_entity
        super().__init__(preserve_url=preserve_url,
                         preserve_phone=preserve_phone,
                         preserve_email=preserve_email)
        
    def domain_rules(self):
        r"""
        Add domain specific rules for clinical notes.

        Return
            - ``rules`` {"key1": "rule 1", "key2": "rule 2"}

        """
        rules = {}
        if not self.preserve_anony_name_entity:
            self.ANONY_NAME_RE = re.compile(r"(?:\[\*\*(.+?)\*\*\])")

            rules["anony_info"] = self.ANONY_NAME_RE

        return rules


class RedditCleaner(TextCleanerBase):

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False,
                 preserve_user=False):

        self.preserve_user = preserve_user
        super().__init__(preserve_url=preserve_url,
                         preserve_phone=preserve_phone,
                         preserve_email=preserve_email)

    def domain_rules(self):
        r"""
        Add  domain specific rules.

        Return
            - ``rules`` {"key1": "rule 1", "key2": "rule 2"}

        """
        rules = {}
        if not self.preserve_user:
            # Reddit user
            self.REDDIT_USER = r"(?:\/?u\/\w+)"
            self.REDDIT_USER_RE = re.compile(self.REDDIT_USER, re.UNICODE)

            rules["user"] = self.REDDIT_USER_RE

        return rules

    def annotate(self, text):
        r"""
        Begin to clean texts.

        Args
            - ``text`` (:obj:`str`): Input text.

        Return:
            - ``text`` (:obj:`str`): Output text.

        """
        text = super().annotate(text)
        text = reduce_lengthening(text)

        return text


class ReviewCleaner(TextCleanerBase):

    def __init__(self,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_email=False):

        super().__init__(preserve_url=preserve_url,
                         preserve_phone=preserve_phone,
                         preserve_email=preserve_email)
