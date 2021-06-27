import numpy as np
import pandas as pd

# Basic
import csv
import pandas as pd
import numpy as np
import os
import re

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Tensorflow
import tensorflow as tf

if tf.test.gpu_device_name():
    print('GPU found')
else:
    print("No GPU found")

# BERT
from transformers import BertTokenizer, BasicTokenizer
from transformers import TFBertModel, TFBertPreTrainedModel, TFBertForSequenceClassification, BertConfig

MAX_SEQUENCE_LENGTH = 93
PRETRAINED_MODEL = 'bert-base-multilingual-cased'
num_labels = 2    

def transform_to_model_input(X, tokenizer, max_length):
    encoded_sentences = encode_sentences(X, tokenizer, max_length=max_length)
    X_ = [encoded_sentences['input_ids'], encoded_sentences['attention_mask']]    
    return X_

def encode_sentences(X, tokenizer, max_length):
    return tokenizer.batch_encode_plus(X,
        max_length=max_length, # tamanho máximo da sequencia de tokens
        truncation=True, # truncar a sentença
        padding=True, # usar padding
        add_special_tokens=True, # adicionar tokens especiais [CLS] e [SEP]
        return_attention_mask=True, # Retornar attention_mask
        return_token_type_ids=False, # NÃO retornar token_type_ids, pois não são necessários        
        return_tensors='tf' # Formato para usar TensorFlow/Keras
        )

def load_bert_model(url = 'bert_model.h5'):

    tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL, do_lower_case=False)    
    model = TFBertForSequenceClassification.from_pretrained(PRETRAINED_MODEL, num_labels=num_labels, output_attentions=False, output_hidden_states=False)    
    model.load_weights(url)

    return model, tokenizer    

def predict_from_sentenca(sentencas, model, tokenizer):
    """Esta função recebe um array de sentenças e um modelo BERT e retorna o valor predito.

    Parameters:
    sentences (array): conjunto de palavras    
    bert_model (function): modelo BERT
    Returns:
    array: um array de valores de scores
    """
    X = transform_to_model_input(sentencas, tokenizer, MAX_SEQUENCE_LENGTH)
    y = model(X)
    y_ = tf.math.argmax( y['logits'], axis=1 ).numpy()   
    return y_