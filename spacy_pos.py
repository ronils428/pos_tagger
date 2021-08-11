import pandas as pd
import spacy
import numpy as np



sp = spacy.load('en_core_web_sm')

def return_sentences(raw_text):
    tokenize_document = sp(raw_text)
    text = list(tokenize_document.sents)
    for i in range(len(text)):
        text[i] = str(text[i])
    df = pd.DataFrame(text, columns = ['Sentences'])
    return df

def token_words(raw_text):
    text_to_tokenize = sp(raw_text)
    word_list = []
    for word in text_to_tokenize:
        word_list.append(word)
    return word_list

def parts_of_speech(word_list):
    final_list = []
    for word in word_list:
        embedded_list = []
        embedded_list.append(f'{word.text}')
        embedded_list.append(f'{word.pos_}')
        embedded_list.append(f'{word.tag_}')
        embedded_list.append(f'{spacy.explain(word.tag_)}')
        final_list.append(embedded_list)
    df = pd.DataFrame(final_list, columns = ['Word', 'Part of Speech', 'Tag', 'Explanation']) 
    # new_df = df[(df['Part of Speech'] == 'ADJ') | (df['Part of Speech'] == 'ADV') | (df['Part of Speech'] == 'VERB')]
    # return new_df
    return df
