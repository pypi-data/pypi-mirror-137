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
# https://github.com/noc-lab/simple_sentence_segment
""" Sentence Tokenizers """
import re


class BasicSentenceTokenizer(object):
    r"""
    This is a basic sentence tokenizer based on regular expression.
    """

    def __init__(self):

        possible_eos = [
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\.(?=\ {1,}\w+|\ {1,}\"\w+|\ {1,}\“\w+)',
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\?(?=\ {1,}\w+|\ {1,}\"\w+|\ {1,}\“\w+)',
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\!(?=\ {1,}\w+|\ {1,}\"\w+|\ {1,}\“\w+)',
            '(?<=[0-9])\.(?=\ {1,}[A-Z]+)',
            '(?<=[0-9])\?(?=\ {1,}[A-Z]+)',
            '(?<=[0-9])\!(?=\ {1,}[A-Z]+)',
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\.',
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\?',
            '(?<=[a-z][a-z]|[A-Z][A-Z]|\w\ )\!',
            '(?<=[0-9])\.',
            '(?<=[0-9])\?',
            '(?<=[0-9])\!',
        ]
        self.possible_eos_re = re.compile('|'.join(possible_eos))

    def annotate(self, text):
        r"""
        Begin to annotate.

        Args
            - ``text`` (:obj:`str`): Input text.

        Return:
            - ``sentences`` A list of sentences.
        """
        eos = {}
        # \n is treated as eos
        eos_re = re.compile(r'\n')
        for eos_find in eos_re.finditer(text):
            start_id = eos_find.span()[0]
            eos[start_id] = {}

        for eos_find in self.possible_eos_re.finditer(text):
            start_id = eos_find.span()[0]
            eos[start_id] = {}

        eos_list = sorted(list(eos))

        if len(eos_list) == 0:
            return []
        sentences = [text[:eos_list[0]+1]]
        for k in range(len(eos_list)-1):
            tt = text[eos_list[k]+1:eos_list[k+1]+1]
            tt = tt.strip()
            if len(tt) > 0:
                sentences.append(tt)
        sentences.append(text[eos_list[-1]+1:])

        return list(filter(None, sentences))
