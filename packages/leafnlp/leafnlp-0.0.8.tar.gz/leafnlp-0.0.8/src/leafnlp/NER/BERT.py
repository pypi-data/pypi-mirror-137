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

import json
import os
from typing import Dict, List

import requests
import torch
from torch.autograd import Variable
from transformers import BertModel, BertTokenizer

from .utils import clean_ner_results


class ModelNER(object):
    """NER Model

    Args:
        - ``model_param`` (:obj:`str`, optional): *Defaults* to "model_ner_bert_v1".
        
        Option for model parameters. If "customized", please specify `train_model_dir` and `base_model_dir`.
        
        - ``train_model_dir`` (:obj:`str`, optional): *Defaults* to "model".
        - ``base_model_dir`` (:obj:`str`, optional): *Defaults* to "".
        
        If not specified, `base_model_dir` will be the same as `train_model_dir`
        
        - ``task`` (:obj:`str`, optional): *Defaults* to "production".
        
        Options for Task: `train`, `validate`, `test`, `production`.
        
        - ``device`` (:obj:`str`, optional): *Defaults* to "cpu".
        
        Device: e.g. `cpu` and `cuda:0`.
    """

    def __init__(self,
                 model_param="model_ner_bert_v1",
                 train_model_dir="model",
                 base_model_dir="",
                 task="production",
                 device="cpu"):   
        self.task = task
        self.train_model_dir = train_model_dir
        if not base_model_dir:
            self.base_model_dir = train_model_dir
        else:
            self.base_model_dir = base_model_dir
        self.device = device
        self.model_param = model_param

        self.pretrained_models = {}
        self.train_models = {}
        self.base_models = {}
        self.batch_data = {}

        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-base-cased')

        if self.task in ["production"]:
            self.build_vocabulary()
            if not self.model_param == "customized":
                PATH_HOME = os.path.expanduser("~")
                PATH_LEAFNLP = os.path.join(PATH_HOME, '.leafnlp_data')
                if not os.path.exists(PATH_LEAFNLP):
                    os.mkdir(PATH_LEAFNLP)
                PATH_LEAFNLP_MODELS = os.path.join(PATH_LEAFNLP, 'models')
                if not os.path.exists(PATH_LEAFNLP_MODELS):
                    os.mkdir(PATH_LEAFNLP_MODELS)
                PATH_LEAFNLP_MODELS_NER = os.path.join(
                    PATH_LEAFNLP_MODELS, 'ner')
                if not os.path.exists(PATH_LEAFNLP_MODELS_NER):
                    os.mkdir(PATH_LEAFNLP_MODELS_NER)
                PATH_LEAFNLP_MODELS_NER_MODEL = os.path.join(
                    PATH_LEAFNLP_MODELS_NER, self.model_param)
                if not os.path.exists(PATH_LEAFNLP_MODELS_NER_MODEL):
                    os.mkdir(PATH_LEAFNLP_MODELS_NER_MODEL)
                self.base_model_dir = PATH_LEAFNLP_MODELS_NER_MODEL
                self.train_model_dir = PATH_LEAFNLP_MODELS_NER_MODEL
                url_head = "https://leafnlp.s3.amazonaws.com"
                # Download label mapping
                model_file = "{}/label_mapping.json".format(
                    PATH_LEAFNLP_MODELS_NER_MODEL)
                if not os.path.exists(model_file):
                    url = "{}/.leafnlp_data/models/ner/{}/label_mapping.json".format(
                        url_head, self.model_param)
                    fout = open(model_file, "wb")
                    res = requests.get(url, stream=True)
                    for chunk in res:
                        fout.write(chunk)
                    fout.close()
                # Load label_mapping
                fl1_ = "{}/label_mapping.json".format(self.train_model_dir)
                with open(fl1_, "r") as fp:
                    label_mapping = json.load(fp)
                self.label2id = {key: label_mapping[key]
                                 for key in label_mapping}
                self.id2label = {label_mapping[key]: key for key in label_mapping}
                self.n_labels = len(self.label2id)
                # build model
                self.build_models()
                # download model param
                for model_name in list(self.base_models) + list(self.train_models):
                    model_file = "{}/{}.model".format(
                        PATH_LEAFNLP_MODELS_NER_MODEL, model_name)
                    if not os.path.exists(model_file):
                        print("Download {}".format(model_file))
                        fout = open(model_file, "wb")
                        url = "{}/.leafnlp_data/models/ner/{}/{}.model".format(
                            url_head, self.model_param, model_name)
                        res = requests.get(url, stream=True)
                        for chunk in res:
                            fout.write(chunk)
                        fout.close()
            else:
                self.build_models()
            # load model param
            for mode_name in self.pretrained_models:
                self.pretrained_models[mode_name].eval()
            for model_name in self.base_models:
                self.base_models[model_name].eval()
                model_file = "{}/{}.model".format(
                    self.base_model_dir, model_name)
                self.base_models[model_name].load_state_dict(torch.load(
                    model_file, map_location=lambda storage, loc: storage))
            for model_name in self.train_models:
                self.train_models[model_name].eval()
                model_file = "{}/{}.model".format(
                    self.train_model_dir, model_name)
                self.train_models[model_name].load_state_dict(torch.load(
                    model_file, map_location=lambda storage, loc: storage))

    def build_vocabulary(self):
        """Build Vocabulary
        """        
        vocab2id = self.tokenizer.get_vocab()
        id2vocab = {vocab2id[wd]: wd for wd in vocab2id}
        vocab_size = len(id2vocab)
        self.batch_data['vocab2id'] = id2vocab
        self.batch_data['id2vocab'] = vocab2id
        print('The vocabulary size: {}'.format(vocab_size))

    def build_models(self):
        """Build all models.
        """        
        hidden_size = 768
        self.pretrained_models['bert'] = BertModel.from_pretrained(
            'bert-base-cased',
            output_hidden_states=True,
            output_attentions=True
        ).to(self.device)
        self.TOK_START = 101
        self.TOK_END = 102
        self.TOK_PAD = 0

        self.train_models['encoder'] = EncoderRNN(
            emb_dim=hidden_size,
            hidden_size=hidden_size,
            nLayers=2,
            rnn_network="lstm",
            device=self.device
        ).to(self.device)

        self.train_models['classifier'] = torch.nn.Linear(
            hidden_size*2, self.n_labels).to(self.device)

    def build_pipe(self):
        """Shared pipe
        """        
        with torch.no_grad():
            input_emb = self.pretrained_models['bert'](
                self.batch_data['input_ids'],
                self.batch_data['pad_mask'])[0]

        input_enc, _ = self.train_models['encoder'](input_emb)

        logits = self.train_models['classifier'](torch.relu(input_enc))

        return logits

    def build_batch(self, batch_data):
        """Build Batch
        """
        token_arr = []
        output = []
        maxlen_text = 0
        if not isinstance(batch_data, List):
            batch_data = [batch_data]
        for itm in batch_data:
            if not isinstance(itm, Dict):
                try:
                    itm = json.loads(itm)
                except:
                    itm = {"text": itm}
            output.append(itm)

            if "tokens" in itm:
                if len(itm["tokens"]) > 300:
                    continue
                toks = self.tokenizer.convert_tokens_to_ids(itm["tokens"])
            else:
                toks = self.tokenizer.encode(itm["text"])[1:-1][:300]
                itm["tokens"] = self.tokenizer.convert_ids_to_tokens(toks)
            toks = [self.TOK_START] + toks + [self.TOK_END]
            token_arr.append(toks)
            if maxlen_text < len(toks):
                maxlen_text = len(toks)

        self.batch_data["maxlen_text"] = maxlen_text

        token_arr = [itm[:maxlen_text] for itm in token_arr]
        token_arr = [itm + [self.TOK_PAD for _ in range(maxlen_text-len(itm))]
                     for itm in token_arr]
        token_var = Variable(torch.LongTensor(token_arr))

        pad_mask = Variable(torch.FloatTensor(token_arr))
        pad_mask[pad_mask != float(self.TOK_PAD)] = -1.0
        pad_mask[pad_mask == float(self.TOK_PAD)] = 0.0
        pad_mask = -pad_mask

        attn_mask = Variable(torch.FloatTensor(token_arr))
        attn_mask[attn_mask == float(self.TOK_START)] = float(self.TOK_PAD)
        attn_mask[attn_mask == float(self.TOK_END)] = float(self.TOK_PAD)
        attn_mask[attn_mask != float(self.TOK_PAD)] = -1.0
        attn_mask[attn_mask == float(self.TOK_PAD)] = 0.0
        attn_mask = -attn_mask

        self.batch_data['input_ids'] = token_var.to(self.device)
        self.batch_data['pad_mask'] = pad_mask.to(self.device)
        self.batch_data['attn_mask'] = attn_mask.to(self.device)
        self.batch_data['output'] = output

    def annotate(self, input_text: List):
        """Begin to annotate the text.

        Args:
            - ``input_text`` (:obj:`List`)
            
        Examples::

            >>> from leafnlp.NER.BERT import ModelNER
            
            >>> ner_model = ModelNER(model_param="model_ner_bert_v1")
            
            >>> input_text = [{"text": "The storm hits New York."}]
            >>> output = ner_model.annotate(input_text)
            >>> print(output)
        """
        self.build_batch(input_text)
        with torch.no_grad():
            logits = self.build_pipe()
            logits = torch.softmax(logits, dim=2)

        pred = logits.topk(1, dim=2)[1].squeeze(2)
        pred = pred.data.cpu().numpy().tolist()

        output = []
        for k, itm in enumerate(self.batch_data["output"]):

            label = [self.id2label[lb] for lb in pred[k]]
            label = label[1:]
            label = label[:len(itm["tokens"])]
            itm["labels_pred"] = label

            output.append(itm)

        return clean_ner_results(output)


class EncoderRNN(torch.nn.Module):

    def __init__(self, 
                 emb_dim=256,
                 hidden_size=256, 
                 nLayers=1,
                 rnn_network="lstm", 
                 bidirectional=True,
                 device=torch.device("cpu")):    
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn_network = rnn_network
        self.nLayers = nLayers
        self.device = device
        self.bidirectional = bidirectional

        if rnn_network == 'lstm':
            self.encoder = torch.nn.LSTM(
                input_size=emb_dim,
                hidden_size=hidden_size,
                num_layers=nLayers,
                batch_first=True,
                bidirectional=bidirectional
            ).to(device)
        elif rnn_network == 'gru':
            self.encoder = torch.nn.GRU(
                input_size=emb_dim,
                hidden_size=hidden_size,
                num_layers=nLayers,
                batch_first=True,
                bidirectional=bidirectional
            ).to(device)

    def forward(self, input_emb):

        n_dk = 1
        if self.bidirectional:
            n_dk = 2
        batch_size = input_emb.size(0)

        h0_encoder = Variable(torch.zeros(
            n_dk*self.nLayers, batch_size, self.hidden_size)).to(self.device)
        if self.rnn_network == 'lstm':
            c0_encoder = Variable(torch.zeros(
                n_dk*self.nLayers, batch_size, self.hidden_size)).to(self.device)
            # encoding
            hy_encoder, (ht_encoder, ct_encoder) = self.encoder(
                input_emb, (h0_encoder, c0_encoder))

            return hy_encoder, (ht_encoder, ct_encoder)

        elif self.rnn_network == 'gru':
            # encoding
            hy_encoder, ht_encoder = self.encoder(input_emb, h0_encoder)

            return hy_encoder, ht_encoder
