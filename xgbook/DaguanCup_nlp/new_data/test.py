#-*- coding: utf-8 -*-
import time
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

start_time = time.time()

df_train = pd.read_csv('train_set.csv')
df_test = pd.read_csv('test_set.csv')
df_train.drop(columns=['article', 'id'], inplace=True)
df_test.drop(columns=['article'], inplace=True)

vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, max_features=100000)
vectorizer.fit(df_train['word_seg'])
X_train = vectorizer.transform(df_train['word_seg'])
X_test = vectorizer.transform(df_test['word_seg'])
y_train = df_train['class'] - 1

lg = LogisticRegression(C=4, dual=True)
lg.fit(X_train, y_train)
y_pred = lg.predict(X_test)

df_test['class'] = y_pred.tolist()
df_test['class'] = df_test['class'] + 1
df_result = df_test.loc[:, ['id', 'class']]
df_result.to_csv('result.csv', index=False)

print 'time used: %s' % (time.time() - start_time)
