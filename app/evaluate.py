import numpy as np
import pandas as pd

# Basic
import csv
import pandas as pd
import numpy as np
import os
import re
from tqdm import tqdm as tqdm
from sklearn.metrics import accuracy_score

from helper import load_bert_model, transform_to_model_input, predict_from_dataset, MAX_SEQUENCE_LENGTH
model_saved_path='../model/bert_model.h5'
model, tokenizer = load_bert_model(model_saved_path)

df = pd.read_csv("../data/reviews_fr.csv")
to_replace = {
    'negative' : 0,    
    'positive' : 1    
}
df['label'].replace(to_replace, inplace=True)

sentencas = df[['content','label']].dropna()

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

batch_size = 64

y_pred_ = []
for batch in tqdm(chunker(sentencas,batch_size)):        
    X = transform_to_model_input(batch.content.values, tokenizer, MAX_SEQUENCE_LENGTH)
    y_pred = predict_from_dataset(X, model)
    for a in y_pred:
        y_pred_.append(a)
    print( accuracy_score(batch.label, y_pred) )

sentencas['predicted'] = np.array(y_pred_)
accuracy_score(sentencas.label, sentencas.predicted)