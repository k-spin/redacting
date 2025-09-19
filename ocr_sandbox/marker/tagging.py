import pandas as pd
import numpy as np

from syntok.tokenizer import Tokenizer
import syntok.segmenter as Segmenter
from flair.data import Token as flairTok
from flair.data import Sentence



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



def ner_on_page(text_table: pd.Series, page: int,ner_tagger) -> pd.DataFrame:

    text_to_tokenize = " ".join(text_table)

    # splits the text using syntok into tokenized sentences
    syntok_sentence_tokenization = Segmenter.segment(Tokenizer().tokenize(text_to_tokenize))

    # transforms the syntok.Token() class items into flair.Token() items so they are compatible with flair.Sentence() and the tagger
    # creates the Sentence objects from the new tokens and runs the sequence tagger on them
    flair_tok_sentences = []
    for split_sentence in syntok_sentence_tokenization:         # NOTE: issue to fix, enormous whitespace before each Sentence, have no clue why, investigate the code
        flair_tok_sentences.append(Sentence([flairTok(text = token.value, start_position=token.offset) for token in split_sentence]))

    ner_tagger.predict(flair_tok_sentences)


    ner_results_table = pd.DataFrame([item for group in [[span.to_dict() for span in proc_sentence.get_spans()] for proc_sentence in flair_tok_sentences] for item in group])
    ner_results_table = pd.concat([pd.Series(page, index=np.arange(ner_results_table.shape[0]), name='page'), ner_results_table,ner_results_table["labels"].apply(split_dicts).apply(pd.Series)],axis=1).rename({"value":"tag","confidence":"conf"},axis=1)
    # display(ner_results_table)    # sanity check before dropping the labels column
    ner_results_table = ner_results_table.drop(columns=['labels'])
    return ner_results_table


def ner_on_file(document_text: pd.DataFrame, ner_tagger) -> pd.DataFrame:
    ner_results_table = pd.DataFrame()
    for page_num in document_text['page'].unique():
        ner_results_table = pd.concat([ner_results_table,ner_on_page(document_text[document_text['page']==page_num]['text'],page_num,ner_tagger)],axis=0, ignore_index=True)
    return ner_results_table