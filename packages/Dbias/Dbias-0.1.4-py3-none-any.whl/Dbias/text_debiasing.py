# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 11:09:09 2021

@author: Deepak.Reji
"""

# loading all the packages
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import requests
import numpy as np
import re
import spacy
import transformers
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForMaskedLM
import time
import plotly.graph_objects as go

#%%
# classification model
tokenizer = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
model = TFAutoModelForSequenceClassification.from_pretrained("d4data/bias-detection-model")
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer) # cuda = 0,1 based on gpu availability

# ner model
#pip install https://huggingface.co/d4data/en_pipeline/resolve/main/en_pipeline-any-py3-none-any.whl
nlp = spacy.load("en_pipeline")

# masked language model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")
unmasker = pipeline('fill-mask', model='bert-base-uncased')

#%%

def run(text_input, show_plot=False):
    # running the classification model to predict whether a sentence is biased or not
    classification_output = classifier(text_input)
    classi_out = classification_output[0]['label']
    probability = classification_output[0]['score']
    
    # running ner to extract the biased words
    doc = nlp(text_input)
    biased_words = []
    for ent in doc.ents:
         biased_words.append(ent.text)
    
    if classi_out != "Biased":
        print("The Sentence is Non biased")
        ###--end--
    
    if classi_out == "Biased" and len(biased_words) == 0 :
        print("The Sentence is biased but the model failed to pick up portion of bias")
        ###--end--
    
    
    if classi_out == "Biased" and len(biased_words) != 0 :
            # collects bias phrases and creates multiple instances of sentences based on no. of biased words
            masked_sentences = []
            for instance in biased_words:
                masked_sentences.append(text_input.replace(instance, '[MASK]'))
            
            # run multiple instances of these masked sentences and retrieves the possible replacement words
            masked_words = []
            for masked_sentence in masked_sentences:

                masked_out = unmasker(masked_sentence)
                
                words_list = []
                for words in masked_out:
                    words_list.append(words['token_str'])
                masked_words.append(words_list) 
                masked_words_flatten = sum(masked_words, [])
                
            # a single sentence with masking based on the phrases
            bias_regex = re.compile('|'.join(map(re.escape, biased_words)))
            combined_mask_sent = bias_regex.sub('[MASK]', text_input)   
            
            # create all different combinations of sentences using masked word suggestion list
            num_words = len(biased_words)
            
            final_constructed_sentences = []
            for m in range(5):
                for n in range(5):
                    occ = 1
                    original_sent = combined_mask_sent
                    for j in range(0, num_words):
                        if m == 0:
                            if j == 0:
                                id2 = 0
                            else:
                                id2 = n
                        elif m ==1:
                            if j == 0:
                                id2 = 1
                            else:
                                id2 = n
                        elif m ==2:
                            if j == 0:
                                id2 = 2
                            else:
                                id2 = n
                        elif m == 3:
                            if j == 0:
                                id2 = 3
                            else:
                                id2 = n
                        elif m == 4:
                            if j == 0:
                                id2 = 4
                            else:
                                id2 = n
               
                        new_sent = original_sent.replace('[MASK]',masked_words[j][id2] , occ)
                        original_sent = new_sent
                        occ+=1
                    
                    final_constructed_sentences.append(original_sent)
                
            final_constructed_sentences = list(set(final_constructed_sentences))
            
            # check which sentence has lowest bias 
            new_pred_label_list = []
            prob_score_list = []
            
            for sentences in final_constructed_sentences:
                new_classification_output = classifier(sentences)
                new_classi_out = new_classification_output[0]['label']
                new_probability = new_classification_output[0]['score']
                new_pred_label_list.append(new_classi_out)
                prob_score_list.append(new_probability)
            
            final_df = pd.DataFrame(list(zip(final_constructed_sentences, new_pred_label_list, prob_score_list)), columns = ['sentence', 'state', 'probability'])
            
            final_df1 = final_df[final_df['state'] == "Non-biased"].reset_index(drop=True)
            final_df1 = final_df1.sort_values(by=['probability'], ascending=False)
            final_df2 = final_df[final_df['state'] == "Biased"].reset_index(drop=True)
            final_df2 = final_df2.sort_values(by=['probability'], ascending=True)
            
            # recommending debiased/reduced bias output
            recommendation_list = []
            if len(final_df1)!= 0:
                final_probability = final_df1['probability'].iloc[0]
                final_probability = 1-final_probability
                print("Hurray! We were able to successfully de-bias the sentence fragment")
                for i in range(0, len(final_df1)):
                    recommendation_list.append({'Sentence':final_df1['sentence'][i], 'bias':1-final_df1['probability'][i]})
            else:
                final_probability = final_df2['probability'].iloc[0]
                print("We were able to reduce the amount of bias!")
                for i in range(0, len(final_df2[0:3])):
                    recommendation_list.append({'Sentence':final_df2['sentence'][i], 'bias':final_df2['probability'][i]})
            

            ##--end---
            if show_plot == True:
                # plotting the bias results
                colors = ['lightslategray',] * 5
                colors[1] = 'crimson'
    
                x = ["Original article", "De-Biased article"]
                bias = [round(probability, 3), round(final_probability, 3)]
                
                # Use textposition='auto' for direct text
                fig = go.Figure(data=[go.Bar(
                            x=x, y=bias,
                            text=bias,
                            textposition='auto',
                            marker_color=colors
                        )])
                fig.update_traces(width=0.5)
                fig.add_trace(go.Line(x=x, y=bias))
                fig.update_layout(title_text='Bias probability for new recomemendations', showlegend=False)
                fig.update_layout(
                    autosize=False,
                    width=800,
                    height=600)
                
                fig.show()
            
            #recommendation_list is the output list of dictionary
            return recommendation_list

#%%
