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
import re

class SentimentPrediction(object):
    r"""
    This is the base for word tokenizer.

    Args
        - ``preserve_case`` (:obj:`bool`, optional): *Default*: True
    
    If True, Perserve case. Otherwise, convert texts to lower case. 
    """

    def __init__(self, model=None):

        self.model = model
        self.sentiment_worker = None
        

    def annotate(self, text = []):
        r"""
        Begin to annotate.

        Args
            - ``text`` (:obj:`list`): Input texts, a list of strings.

        Return:
            - ``sentences`` A list of sentences.
        """
        sentiment = self.sentiment_worker.annotate(text)

        return None
