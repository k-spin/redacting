import pandas as pd
import numpy as np

from importlib import reload as rel

from syntok.tokenizer import Tokenizer
import syntok.segmenter as Segmenter
import flair.data
rel(flair.data)
from flair.data import Token as flairTok
from flair.data import Sentence

import objects
rel(objects)
from objects import markerObject
from objects import spanObject
from objects import sentenceObject

import copy


def split_dicts(lst: list[dict]) -> dict:
    """ 
    Grabs the labels column from the NER dataframe, and splits it into two columns, one for the NER tags
    and one for the confidence of said tags.

    NOTE: If NER has assigned more than one tag, the item returned is a list. Ensure that any handling of
    the value and confidence columns properly accounts for list-type items instead of str or floats
    """
    # pick out first dict, iterate through keys, for each key store a list of all
    result = {k: [d[k] for d in lst] for k in lst[0].keys()}
    # unwrap single-item lists
    return {k: v[0] if len(v) == 1 else v for k, v in result.items()}



# def ner_on_page(text_table: pd.Series, page: int,ner_tagger) -> pd.DataFrame:

#     text_to_tokenize = " ".join(text_table)

#     # splits the text using syntok into tokenized sentences
#     syntok_sentence_tokenization = Segmenter.segment(Tokenizer().tokenize(text_to_tokenize))

#     # transforms the syntok.Token() class items into flair.Token() items so they are compatible with flair.Sentence() and the tagger
#     # creates the Sentence objects from the new tokens and runs the sequence tagger on them
#     flair_tok_sentences = []
#     for split_sentence in syntok_sentence_tokenization:         # NOTE: issue to fix, enormous whitespace before each Sentence, have no clue why, investigate the code
#         flair_tok_sentences.append(Sentence([flairTok(text = token.value, start_position=token.offset) for token in split_sentence]))

#     ner_tagger.predict(flair_tok_sentences)


#     ner_results_table = pd.DataFrame([item for group in [[span.to_dict() for span in proc_sentence.get_spans()] for proc_sentence in flair_tok_sentences] for item in group])
#     ner_results_table = pd.concat([pd.Series(page, index=np.arange(ner_results_table.shape[0]), name='page'), ner_results_table,ner_results_table["labels"].apply(split_dicts).apply(pd.Series)],axis=1).rename({"value":"tag","confidence":"conf"},axis=1)
#     # display(ner_results_table)    # sanity check before dropping the labels column
#     ner_results_table = ner_results_table.drop(columns=['labels'])
#     return ner_results_table




# def ner_on_file(document_text: pd.DataFrame, ner_tagger) -> pd.DataFrame:
#     ner_results_table = pd.DataFrame()
#     for page_num in document_text['page'].unique():
#         ner_results_table = pd.concat([ner_results_table,ner_on_page(document_text[document_text['page']==page_num]['text'],page_num,ner_tagger)],axis=0, ignore_index=True)
#     return ner_results_table





def ner_on_page(filtered_paged_offsets: pd.Series, page: int, text_to_tokenize: str, ner_tagger) -> pd.DataFrame:

    # splits the text using syntok into tokenized sentences
    syntok_sentence_tokenization = Segmenter.segment(Tokenizer().tokenize(text_to_tokenize))




    flair_tok_sentences = []
    syntok_tokens = []
    for split_sentence in syntok_sentence_tokenization:
        flair_tok_sentences.append(Sentence([flairTok(text = token.value, start_position=0) for token in split_sentence]))
        syntok_tokens.append(split_sentence)

    ner_tagger.predict(flair_tok_sentences)

    for position,sentence in enumerate(flair_tok_sentences):
        in_sent_identifier = 0
        start_position = syntok_tokens[position][0].offset
        end_position = syntok_tokens[position][-1].offset + len(syntok_tokens[position][-1].value) + 1
        # print(f"[{start_position},{end_position}]")   # +1 here to account for how syntok counts offsets (essentially the number syntok shows is the character right before the first character of the token)
        sent_text = sentence.text
        # print(sent_text)

        spanlist = []
        for span in sentence.get_spans():
            # print([tok for tok in span.tokens])
            # tokenids = [tok.idx-1 for tok in span.tokens]
            tokens_from_spans = [syntok_tokens[position][tok.idx-1] for tok in span.tokens]
            # offsets_from_spans = [tok.offset+1 for tok in tokens_from_spans]
            # can also retrieve information from the tokens not just IDs and make the new list
            # print(span)
            # print(f"Token ID's are: {tokenids}")
            # print(f"Corresponding tokens: {tokens_from_spans}")
            # print(f"Corresponding token offsets: {offsets_from_spans}")
            in_sent_identifier += 1
            # print(offset_table)
            # corr_lines = [int(np.searchsorted(offset_table['totlength'],tokoffset,side='right')) for tokoffset in tokens_from_spans]
            left_index = int(np.searchsorted(filtered_paged_offsets['totlength'],tokens_from_spans[0].offset + 1,side='right'))
            right_index = int(np.searchsorted(filtered_paged_offsets['totlength'],tokens_from_spans[-1].offset + 1,side='left'))
            
            if right_index - left_index == 0:
                index_list = [right_index]
            elif right_index - left_index >= 1:
                index_list = list(range(left_index,right_index+1))
            # print(f"LIST: {index_list}")
            linked_lines = [filtered_paged_offsets.iloc[idx]['id'] for idx in index_list]
            spanlist.append(spanObject(identifier=in_sent_identifier, tokens=tokens_from_spans,tag=span.tag,linked_lines=linked_lines))
            print(repr(spanlist[-1]))

        # NOTE: NEW PLAN
        # Fuck the sentences, get lists of spans per page, and then
        # for each span, with linked lines, normalize (span start position = offset - linepos (offset table))
        # for tokens index, use index to get corresponding char index to get corresponding char coords (here will need some more analyzing to handle multi-line items)
        # ++ function to merge token coords and hand back one (or multiple depending on case) set of bboxes
        # also see about examining the claim that simply adding redaction annotations but not redacting makes the documents able to be redacted by pdf Xchnage
        new_obj = sentenceObject(text = sent_text, start_position=start_position,end_position=end_position, spans = spanlist)
        # print(repr(new_obj))

    pass




def ner_on_file(offset_table: pd.DataFrame, markerobjects: dict[str:markerObject], ner_tagger) -> dict[str:sentenceObject]:

    sentenceobjects = {}
    for page_num in offset_table['page'].unique():

        filtered_offset_table = copy.deepcopy(offset_table[offset_table['page']==page_num])
        page_text = "".join([markerobjects[page_num][identifier].text for identifier in filtered_offset_table['id']])
        # print(page_text)
        ner_on_page(filtered_offset_table,page_num,page_text,ner_tagger)
        # ner_results_table = pd.concat([ner_results_table,],axis=0, ignore_index=True)
    
    return sentenceobjects

# .drop(['page'],axis=1,inplace=True)