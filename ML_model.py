# -*- coding: utf-8 -*-
"""
Author: Pandurang Pampatwar
Date: Created: 6th August 2020
Purpose:
    1. This File gets the data and then cleans it.
    2. Trains the model on cleaned data using pipeline.
    3. Should predict the output with min accuracy of 80%.

"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from joblib import dump
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# Importing the database on which the model need to be trained.
comp_log = pd.read_csv("Consumer_Complaints.csv")

# Removing unnecessary columns
cleaning = comp_log.iloc[:,[1,5]]

# Re-categorizing the data so as enhance model's accuracy.
cleaned = cleaning.dropna()
cleaned['Product'].replace(to_replace='Virtual currency', value='Money transfers', inplace=True)
cleaned['Product'].replace(to_replace='Money transfer, virtual currency, or money service', value='Money transfers', inplace=True)
cleaned['Product'].replace(to_replace='Vehicle loan or lease', value='Payday loan, title loan, or personal loan or consumer loan', inplace=True)
cleaned['Product'].replace(to_replace='Credit reporting', value='Credit reporting, credit repair services, or other personal consumer reports', inplace=True)
cleaned['Product'].replace(to_replace='Payday loan, title loan, or personal loan', value='Payday loan, title loan, or personal loan or consumer loan', inplace=True)
cleaned['Product'].replace(to_replace='Student loan', value='Payday loan, title loan, or personal loan or consumer loan', inplace=True)
cleaned['Product'].replace(to_replace='Checking or savings account', value='Bank account or service', inplace=True)
cleaned['Product'].replace(to_replace='Other financial service', value='Money transfers', inplace=True)
cleaned['Product'].replace(to_replace=['Credit card','Prepaid card'], value='Credit card or prepaid card', inplace=True)
cleaned['Product'].replace(to_replace=['Payday loan','Consumer Loan'], value='Payday loan, title loan, or personal loan or consumer loan', inplace=True)


# Splitting the data for training and testing purpose.
X_train, X_test, y_train, y_test = train_test_split(cleaned['Consumer complaint narrative'], cleaned['Product'], test_size=0.25, random_state=42)

# Creating a pipeline for the model.
text_pred = Pipeline([
    ('tfvf', TfidfVectorizer()),
('clf1', SGDClassifier(max_iter=1000, tol=0.2)),
                     ])
# Fitting the model
text_pred.fit(X_train, y_train)

# Predicting the values and then calculating the mean
predicted = text_pred.predict(X_test)
np.mean(predicted == y_test)

# Printing the scores of model
print(accuracy_score(y_test, predicted))
print(classification_report(y_test, predicted))
print(confusion_matrix(y_test, predicted))

#testing for one example different from dataset.
doc = ['I have drawn loan on my house but it is still not approved']
text_pred.predict(doc)

# Saving the model as python object.
dump(text_pred, 'model.pkl')

"""
Results:
    1. Trained the model using pipeline
    2. Model tis able to predict the category with around 85% accuracy.

"""