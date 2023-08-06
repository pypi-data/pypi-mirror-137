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
# modified from
# https://github.com/erikavaris/tokenizer/blob/master/tokenizer/reg.py
# https://www.nltk.org/_modules/nltk/tokenize/casual.html
import re


class BasicNormalizer():
    r"""Casual text normalization, for common contractions in English
    """

    def __init__(self):
        # add cant? technically a separate word
        self.CONTRACTIONS_NEG = re.compile(
            r"cannot\b|\w+n't\b|shant|wont", re.I)
        self.CONTRACTIONS_FUT = re.compile(
            r"\b(i'll|he'll|she'll|you'll|youll|we'll)\b", re.I)  # ill, hell, shell, well
        # assuming "'d" is modal "should/would" for now; "had" also possible but not coded here
        self.CONTRACTIONS_MOD = re.compile(
            r"\b(i'd|you'd|youd|he'd|she'd|we'd)\b", re.I)  # id, hed, shed, wed
        self.CONTRACTIONS_COPULA = re.compile(
            r"\b(i'm|im|you're|youre|we're|they're|theyre|he's|hes|shes|she's|it's)\b", re.I)  # were, its
        self.CONTRACTIONS_HAVE = re.compile(r"\w+'ve\b", re.I)
        self.GOTTA = re.compile(r'\bgotta\b', re.I)
        self.GONNA = re.compile(r'\bgonna\b', re.I)
        self.HAFTA = re.compile(r'\bhafta\b', re.I)
        self.WANNA = re.compile(r'\bwanna\b', re.I)

    def infinitives(self, text):
        r"""Separate infinitive contractions. Returns text string.
        """
        if re.findall(self.GOTTA, text):
            text = re.sub(self.GOTTA, 'got to', text)
        if re.findall(self.GONNA, text):
            text = re.sub(self.GONNA, 'going to', text)
        if re.findall(self.HAFTA, text):
            text = re.sub(self.HAFTA, 'have to', text)
        if re.findall(self.WANNA, text):
            text = re.sub(self.WANNA, 'want to', text)

        return text

    def copula_contracts(self, text):
        r"""Un-contract copulas. Returns text string.
        """
        cop_matches = re.findall(self.CONTRACTIONS_COPULA, text)
        if len(cop_matches) >= 1:
            for match in cop_matches:
                if match.lower() in ["i'm", "im"]:
                    replace_with = "I am"
                elif match.lower() in ["you're", "youre"]:
                    replace_with = "you are"
                elif match.lower() in ["they're", "theyre"]:
                    replace_with = "they are"
                elif match.lower() == "we're":
                    replace_with = "we are"
                elif match.lower() in ["hes", "shes"]:
                    replace_with = match.split("s")[0] + ' is'
                else:
                    replace_with = match.split("'")[0] + ' is'
                text = re.sub(match, replace_with, text)

        return text

    def neg_contracts(self, text):
        r"""Un-contract negatives. Returns text string.
        """
        neg_matches = re.findall(self.CONTRACTIONS_NEG, text)
        if len(neg_matches) >= 1:
            # Get substrings, and replace with verb + not
            for match in neg_matches:
                if match.lower() in ["won't", "wont"]:
                    replace_with = "will not"
                elif match.lower() in ['cannot', "can't"]:
                    replace_with = 'can not'
                elif match.lower() in ["shan't", "shant"]:
                    replace_with = 'shall not'
                else:
                    splitting_neg = re.compile(r"n't", re.I)
                    replace_with = re.split(splitting_neg, match)[0] + " not"
                text = re.sub(match, replace_with, text)
        return text

    def fut_contracts(self, text):
        r"""Un-contract futures. Returns text string.
        """
        fut_matches = re.findall(self.CONTRACTIONS_FUT, text)
        if len(fut_matches) >= 1:
            # Get substrings and replace with pro + will
            for match in fut_matches:
                if match.lower() == "youll":
                    replace_with = match.split("ll")[0] + ' will'
                else:
                    replace_with = match.split("'")[0] + ' will'
                text = re.sub(match, replace_with, text)
        return text

    def mod_contracts(self, text):
        r"""Un-contract modals. Returns text string.
        """
        mod_matches = re.findall(self.CONTRACTIONS_MOD, text)
        if len(mod_matches) >= 1:
            # Get substrings and replace with pro + would
            for match in mod_matches:
                if match.lower() == "youd":
                    replace_with = match.split("d")[0] + ' would'
                else:
                    replace_with = match.split("'")[0] + ' would'
                text = re.sub(match, replace_with, text)

        return text

    def have_contracts(self, text):
        r"""Un-contract futures. Returns text string.
        """
        have_matches = re.findall(self.CONTRACTIONS_HAVE, text)
        if len(have_matches) >= 1:
            # Get substrings and replace with pro + have
            for match in have_matches:
                replace_with = match.split("'")[0] + ' have'
                text = re.sub(match, replace_with, text)
        return text

    def normalize(self, text):
        r"""Simple regularization to de-contract negatives,
        futures, modals, copulas, and pluperfect.
        Returns text string
        
        Example::

            >>> from leafnlp.normalizer.basic_normalizer import BasicNormalizer
            >>> text = "I'll go to the airport."
            >>> normalizer = BasicNormalizer()
            >>> print(normalizer.normalize("I'll go to the airport."))
            >>>
            Output: I will go to the airport.
        """
        text = self.infinitives(text)
        text = self.neg_contracts(text)
        text = self.fut_contracts(text)
        text = self.mod_contracts(text)
        text = self.copula_contracts(text)
        text = self.have_contracts(text)

        return text
