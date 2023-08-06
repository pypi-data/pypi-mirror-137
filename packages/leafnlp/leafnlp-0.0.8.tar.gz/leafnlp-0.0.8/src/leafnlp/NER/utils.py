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


def collect_named_entities(tokens):
    """Creates a list of Entity named-tuples, storing the entity type and the start and end
    offsets of the entity.
    """

    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None

    for offset, token_tag in enumerate(tokens):

        if token_tag == 'O':
            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append({"label": ent_type, "start": start_offset, "end": end_offset})
                start_offset = None
                end_offset = None
                ent_type = None

        elif ent_type is None:
            ent_type = token_tag[2:]
            start_offset = offset

        elif ent_type != token_tag[2:] or (ent_type == token_tag[2:] and token_tag[:1] == 'B'):

            end_offset = offset - 1
            named_entities.append({"label": ent_type, "start": start_offset, "end": end_offset})

            # start of a new entity
            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    # catches an entity that goes up until the last token

    if ent_type is not None and start_offset is not None and end_offset is None:
        named_entities.append({"label": ent_type, "start": start_offset, "end": len(tokens)-1})

    return named_entities

def clean_ner_results(results):
    
    output = []
    for input_ in results:
        text = input_["text"]
        tokens = input_["tokens"]
        labels = input_["labels_pred"]

        named_entities = collect_named_entities(labels)

        outspan = []
        i = 0
        for j, wd in enumerate(tokens):
            wdlen = len(wd)
            if wd[:2] == "##":
                wdlen -= 2
            while i < len(text):
                if text[i] == " ":
                    i += 1
                else:
                    break
            span = [i, i+wdlen]
            i += wdlen
            outspan.append({"token": wd, "span": span, "label": labels[j]})
        input_["named_entities_raw"] = outspan

        out_org = []
        for itm in named_entities:
            span = [outspan[itm["start"]]["span"][0], outspan[itm["end"]]["span"][1]]
            out_org.append({"label": itm["label"], "text": text[span[0]:span[1]], "span": span})
        input_["named_entities"] = out_org
        
        output.append(input_)
        
    return output