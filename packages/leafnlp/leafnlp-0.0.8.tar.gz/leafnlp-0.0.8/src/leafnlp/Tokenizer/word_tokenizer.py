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

# This code is modified based on
# https://github.com/erikavaris/tokenizer/blob/master/tokenizer/tokenizer.py
""" Word Tokenizers """
import re

from .text_cleaner import RedditCleaner, TweetCleaner, ClinicalNoteCleaner
from .utils.utils import (_replace_html_entities, get_abbreviation_general,
                          get_emotions, get_special_tokens,
                          get_special_tokens_clinical_notes, get_urls,
                          get_words_regexps, reduce_lengthening)


class TokenizerBase(object):
    r"""
    This is the base for word tokenizer.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, Perserve case. Otherwise, convert texts to lower case. 
    """

    def __init__(self, preserve_case=False):

        self.preserve_case = preserve_case

        self.set_open_domain_rules()
        self.WORD_RE = self.domain_specific_assemble()

    def set_open_domain_rules(self):
        r"""
        Basic RE Rules
        """
        self.WORDS = get_words_regexps()
        # URLs
        self.URLS = get_urls()
        self.URL = r"((https?:\/\/|www)|\w+\.(\w{2-3}))([\w\!#$&-;=\?\-\[\]~]|%[0-9a-fA-F]{2})+"
        # phone numbers
        self.PHONE = r"(?:(?:\+?[01][\-\s.]*)?(?:[\(]?\d{3}[\-\s.\)\/]*)?\d{3}[\-\s.]*\d{4})"
        # email addresses
        self.EMAILS = r"[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]"
        # html tags:
        self.HTML_TAGS = r"<[^>\s]+>"

        # ASCII Arrows
        self.ASCII_ARROWS = r"[\-]+>|<[\-]+"
        # Special tokens
        self.SPECIAL = get_special_tokens()

    def domain_specific_assemble(self):
        r"""
        Modify this function for different domains.
        """
        REGEXPS = [self.URLS]
        REGEXPS += self.SPECIAL
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def clean_text(self, text):
        r"""
        Remove unwanted tokens or patterns.
        """
        text = _replace_html_entities(text)

        return text

    def annotate(self, text):
        r"""
        Begin to tokenize.

        Args
            - ``text`` (:obj:`str`): Input text.

        Return:
            - ``words`` A list of tokens.

        Examples::

            >>> from leafnlp.tokenizer.word_tokenizer import Tokenizer
            >>> text = "I like apple juice."
            >>> tokenizer = Tokenizer()
            >>> output = tokenizer.annotate(text)
            >>> print(' '.join(output))
            >>> 
            Output: I like apple juice .
        """
        text = self.clean_text(text)
        words = self.WORD_RE.findall(text)
        if not self.preserve_case:
            words = ' '.join(words).lower().split()

        return words


class TweetTokenizer(TokenizerBase):
    r"""
    This is a tokenizer for tweets.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, Perserve case. Otherwise, convert texts to lower case. 

        - ``preserve_url`` (:obj:`bool`, optional): *Default*: True

    If True, keep URL. Otherwise, change to @url. 

        - ``preserve_email`` (:obj:`bool`, optional): *Default*: True

    If True, keep email. Otherwise, change to @email. 

        - ``preserve_phone`` (:obj:`bool`, optional): *Default*: True

    If True, keep phone number. Otherwise, change it to @phone. 

        - ``preserve_user`` (:obj:`bool`, optional): *Default*: True

    If True, keep user. Otherwise, change it to @user. 

    """

    def __init__(self,
                 preserve_case=True,
                 preserve_email=False,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_user=False):
        super().__init__(preserve_case=preserve_case)

        self.tweetcleaner = TweetCleaner(preserve_url=preserve_url,
                                         preserve_email=preserve_email,
                                         preserve_phone=preserve_phone,
                                         preserve_user=preserve_user)

    def domain_specific_assemble(self):

        # Abbreviations
        self.ABBREV = get_abbreviation_general()
        # emotions
        self.EMOTICONS = get_emotions()
        self.EMOTICONS_RE = re.compile(
            r"({})".format("|".join(self.EMOTICONS), re.UNICODE))
        # hashtags e.g., #ICCV
        self.HASHTAG = r"(?:\#\w+)"
        self.HASHTAG_RE = re.compile(self.HASHTAG, re.UNICODE)

        REGEXPS = [self.URLS, self.PHONE]
        REGEXPS += self.ABBREV
        REGEXPS += self.SPECIAL
        REGEXPS += self.EMOTICONS
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.HASHTAG, self.EMAILS, self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def clean_text(self, text):

        text = super().clean_text(text)
        text = self.tweetcleaner.annotate(text)

        return text


class RedditTokenizer(TokenizerBase):
    r"""
    This is a tokenizer for reddit.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, Perserve case. Otherwise, convert texts to lower case. 

        - ``preserve_url`` (:obj:`bool`, optional): *Default*: True

    If True, keep URL. Otherwise, change to @url. 

        - ``preserve_email`` (:obj:`bool`, optional): *Default*: True

    If True, keep email. Otherwise, change to @email. 

        - ``preserve_phone`` (:obj:`bool`, optional): *Default*: True

    If True, keep phone number. Otherwise, change it to @phone. 

        - ``preserve_user`` (:obj:`bool`, optional): *Default*: True

    If True, keep user. Otherwise, change it to @user. 

    """

    def __init__(self,
                 preserve_case=True,
                 preserve_email=False,
                 preserve_url=False,
                 preserve_phone=False,
                 preserve_user=False):
        super().__init__(preserve_case=preserve_case)

        self.redditcleaner = RedditCleaner(preserve_url=preserve_url,
                                           preserve_email=preserve_email,
                                           preserve_phone=preserve_phone,
                                           preserve_user=preserve_user)

    def domain_specific_assemble(self):

        # Abbreviations
        self.ABBREV = get_abbreviation_general()
        # emotions
        self.EMOTICONS = get_emotions()
        self.EMOTICONS_RE = re.compile(
            r"({})".format("|".join(self.EMOTICONS), re.UNICODE))
        # hashtags e.g., #ICCV
        self.HASHTAG = r"(?:\#\w+)"
        self.HASHTAG_RE = re.compile(self.HASHTAG, re.UNICODE)

        REGEXPS = [self.URLS, self.PHONE]
        REGEXPS += self.ABBREV
        REGEXPS += self.SPECIAL
        REGEXPS += self.EMOTICONS
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.HASHTAG, self.EMAILS, self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def remove_tokens(self, text):

        text = super().remove_tokens(text)
        text = self.redditcleaner.annotate(text)

        return text


class NewsTokenizer(TokenizerBase):
    r"""
    This is a tokenizer for News articles.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, Perserve case. Otherwise, convert texts to lower case. 

        - ``preserve_url`` (:obj:`bool`, optional): *Default*: True

    If True, keep URL. Otherwise, remove URLs. 

    """

    def __init__(self,
                 preserve_case=False,
                 preserve_url=True):
        super().__init__(preserve_case=preserve_case,
                         preserve_url=preserve_url)

    def domain_specific_assemble(self):

        # Abbreviations
        self.ABBREV = get_abbreviation_general()
        # emotions
        self.EMOTICONS = get_emotions()
        self.EMOTICONS_RE = re.compile(
            r"({})".format("|".join(self.EMOTICONS), re.UNICODE))
        # hashtags e.g., #ICCV
        self.HASHTAG = r"(?:\#\w+)"
        self.HASHTAG_RE = re.compile(self.HASHTAG, re.UNICODE)
        # Reddit user
        self.REDDIT_USER = r"(?:\/?u\/\w+)"
        self.REDDIT_USER_RE = re.compile(self.REDDIT_USER, re.UNICODE)

        REGEXPS = [self.URLS, self.PHONE]
        REGEXPS += self.ABBREV
        REGEXPS += self.SPECIAL
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.EMAILS, self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def remove_tokens(self, text):

        text = super().remove_tokens(text)

        return text


class ClinicalNotesTokenizer(TokenizerBase):
    r"""
    This is a tokenizer for News articles.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, perserve case. Otherwise, convert texts to lower case. 

        - ``preserve_url`` (:obj:`bool`, optional): *Default*: True

    If True, keep URL. Otherwise, remove URLs.

        - ``preserve_anonymous_name_entity`` (:obj:`bool`, optional): *Default*: False

    Used to process MIMIC III clinical notes. 
    If True, keep `[**Name Last**]`. Otherwise, replace it with `anony_named_entity`.

    """

    def __init__(self,
                 preserve_case=True,
                 preserve_url=False,
                 preserve_email=False,
                 preserve_phone=False,
                 preserve_anony_name_entity=False):
        super().__init__(preserve_case=preserve_case)

        self.preserve_anony_name_entity = preserve_anony_name_entity

        self.tweetcleaner = ClinicalNoteCleaner(preserve_url=preserve_url,
                                                preserve_email=preserve_email,
                                                preserve_phone=preserve_phone,
                                                preserve_anony_name_entity=preserve_anony_name_entity)

    def domain_specific_assemble(self):

        # Abbreviations
        self.ABBREV = get_abbreviation_general()
        self.SPECIAL_CLINIC = get_special_tokens_clinical_notes()

        REGEXPS = [self.URLS]
        REGEXPS += self.ABBREV
        REGEXPS += self.SPECIAL
        REGEXPS += self.SPECIAL_CLINIC
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.EMAILS, self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def clean_text(self, text):

        text = super().clean_text(text)
        text = self.tweetcleaner.annotate(text)

        return text


class ReviewTokenizer(TokenizerBase):
    r"""
    This is a tokenizer for News articles.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True

    If True, preserve case. Otherwise, convert texts to lower case.

        - ``preserve_url`` (:obj:`bool`, optional): *Default*: True

    If True, keep URL. Otherwise, remove URLs. 

    """

    def __init__(self,
                 preserve_case=False,
                 preserve_url=True):
        super().__init__(preserve_case=preserve_case,
                         preserve_url=preserve_url)

    def domain_specific_assemble(self):

        # Abbreviations
        self.ABBREV = get_abbreviation_general()
        # emotions
        self.EMOTICONS = get_emotions()
        self.EMOTICONS_RE = re.compile(
            r"({})".format("|".join(self.EMOTICONS), re.UNICODE))
        # hashtags e.g., #ICCV
        self.HASHTAG = r"(?:\#\w+)"
        self.HASHTAG_RE = re.compile(self.HASHTAG, re.UNICODE)
        # Reddit user
        self.REDDIT_USER = r"(?:\/?u\/\w+)"
        self.REDDIT_USER_RE = re.compile(self.REDDIT_USER, re.UNICODE)

        REGEXPS = [self.URLS, self.PHONE]
        REGEXPS += self.ABBREV
        REGEXPS += self.SPECIAL
        REGEXPS += [self.HTML_TAGS, self.ASCII_ARROWS]
        REGEXPS += [self.EMAILS, self.WORDS]

        return re.compile(r"({})".format("|".join(REGEXPS)),
                          re.VERBOSE | re.I | re.UNICODE)

    def remove_tokens(self, text):

        text = super().remove_tokens(text)

        return text
