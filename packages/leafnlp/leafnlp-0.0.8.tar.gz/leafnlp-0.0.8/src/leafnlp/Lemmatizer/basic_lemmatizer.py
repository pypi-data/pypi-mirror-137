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
# Data from https://github.com/michmech/lemmatization-lists
import json
import os

PATH_HOME = os.path.expanduser("~")
PATH_LEAFNLP_DATA = os.path.join(PATH_HOME, '.leafnlp_data/models')


class BasicLemmatizer():
    r"""Basic Lemmatizer"""

    def __init__(self):
        r"""Casual text normalization, for common contractions in English
        """

        file_ = os.path.join(PATH_LEAFNLP_DATA,
                             'lemmatizer/mapping_en.json')
        with open(file_, 'r') as fp:
            self.mapping = json.load(fp)

    def lemmatize(self, text):
        r"""Lemmatize the text.
        
        Example::
        
            >>> from leafnlp.lemmatizer.basic_lemmatizer import BasicLemmatizer
            >>> text = "leafnlp is a new package."
            >>> lemmatizer = BasicLemmatizer()
            >>> print(lemmatizer.lemmatize(text))
            >>>
            Output: leafnlp be a new package.
        
        """
        return ' '.join([self.mapping[wd]
                         if wd in self.mapping else wd for wd in text.split()])
