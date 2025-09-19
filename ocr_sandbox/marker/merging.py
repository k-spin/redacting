import pandas as pd
import numpy as np




def get_index_set_per_page(ner_table_pagelevel: pd.DataFrame, lookup_table_pagelevel: pd.Series, tagfilter: list[str]) -> set:


    # this is a solution modified to the current outputs, this will need to be changed to picking out coordinates probably and matching sentences to ensure proper covering IF we manage to get a char-wise or word-wise OCRing

    page_index_set = set()
    # display(ner_table_pagelevel)
    # display(lookup_table_pagelevel)
    add_search_offset = lookup_table_pagelevel.index[0]
    for index, row in ner_table_pagelevel.iterrows():
        if row['tag'] in tagfilter:
            continue
        else:
            left_index = np.searchsorted(lookup_table_pagelevel, row['start_pos']+1, side='right') + add_search_offset      # +1 here to account for syntok, whose offset is counted from the spacing character right behind the token, and not at the start of the word itself
            right_index = np.searchsorted(lookup_table_pagelevel, row['end_pos'], side='left') + add_search_offset         # NOTE THIS MIGHT NOT BE THE CASE ON ALL TOKENS, NEED TO INSPECT OUTPUTS AND MODIFY THE OFFSET AT TOKEN CREATION ACCORDINGLY ?
            # print(int(left_index),int(right_index))     # sanity check for found indices
            if right_index - left_index >= 1: page_index_set.update(np.arange(left_index,right_index+1).tolist())
            else: page_index_set.update([int(left_index)])
    
    return page_index_set

def get_index_set(ner_table, lookup_table, tagfilter):
    
    main_index_dict = {}
    
    for page_num in ner_table['page'].unique():
        main_index_dict.update({int(page_num):get_index_set_per_page(ner_table[ner_table['page']==page_num],lookup_table[lookup_table['page']==page_num]['totlength'],tagfilter)})
    return main_index_dict