import gradio as gr
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("drug200.csv", delimiter=",")
# -*- coding: utf-8 -*-
"""pred_drugs_addict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1miD2NyrOv7i41irDQgUrNs410_vZ-oy9

Programme permetttant de detecter sous quelle drogue se trouve un patient.
"""

from numpy.core.fromnumeric import shape
import pandas as pd
import numpy as np




# Créer un objet LabelEncoder
label_encoder = LabelEncoder()

# Définir la variable de catégorie à encoder
# Encoder les catégories en entiers

Drug_encoded = label_encoder.fit_transform(df['Drug'])

Sex_encoded = label_encoder.fit_transform(df['Sex'])

BP_encoded = label_encoder.fit_transform(df['BP'])

Cholesterol_encoded = label_encoder.fit_transform(df['Cholesterol'])

df.drop("Drug", axis=1, inplace=True)
df.drop("Sex", axis=1, inplace=True)
df.drop("BP", axis=1, inplace=True)
df.drop("Cholesterol", axis=1, inplace=True)
 

df["Drug"] = Drug_encoded
df['Sex'] = Sex_encoded
df['BP'] = BP_encoded
df['Cholesterol'] = Cholesterol_encoded
df

x = df[['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']]
y = df['Drug']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

clf = RandomForestClassifier(criterion = 'entropy', n_estimators = 4)
clf.fit(X_train,y_train)
score = clf.score(X_test,y_test)
print(score)

def start(Age,Sex,BP,Cholesterol,Na_to_K):
            if (Sex =='male'):
                sex = "1"
            if (Sex =='female'):
                sex = "0"    
            if (BP =='LOW'):
                bp = "1" 
            if (BP =='NORMAL'): 
                bp = "2"     
            if (BP =='HIGH'): 
                bp = "0" 
            if (Cholesterol =='LOW'): 
                ch = "1"    
            if (Cholesterol =='NORMAL'): 
                ch = "2"       
            if (Cholesterol =='HIGH'): 
                ch = "0"       
            cels = Na_to_K
            data = []
            data = [[Age,sex,bp,ch,cels]]
            pred = pd.DataFrame(data, columns=['Age','Sex','BP','Cholesterol','Na_to_K'])
            y_pred = clf.predict(pred)
            if (y_pred ==0): 
                ch = "Drug: Y"    
            if (y_pred ==4): 
                ch = "Drug: X"       
            if (y_pred ==3): 
                ch = "Drug: C"
            if (y_pred ==1): 
                ch = "Drug: A"
            if (y_pred ==2): 
                ch = "Drug: B" 
            return  ch
            
        
def is_number(x):
    return bool(re.match("^[0-9]+$", x))

input_text = gr.inputs.Textbox(label="Na_to_K")
sex = gr.inputs.Radio(['female', 'male'], label="Sex")
BP = gr.inputs.Radio(['LOW','NORMAL','HIGH'], label="BP")
Cholesterol = gr.inputs.Radio(['LOW','NORMAL','HIGH'], label="Cholesterol")
face = gr.Interface(fn=start, inputs=[gr.inputs.Slider(1, 130),sex,BP,Cholesterol,input_text],examples = [[51,"male","HIGH","LOW",5],[60,"male","HIGH","NORMAL",8.61],[69,"female","NORMAL","HIGH",10.05],[64,"female","LOW","NORMAL",25.61],[22,"male","LOW","HIGH",8.11]],cache_examples = True ,outputs=["text"])
face.launch()
