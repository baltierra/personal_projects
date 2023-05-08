import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from trollbane.paths import data_path
from warnings import filterwarnings # Ignore warnings 

df = pd.read_parquet(data_path().joinpath('clean', 'notes-clean.parquet.gzip'),
            columns=['classification', 'summary', 'createdatmillis', 'validationdifficulty', 'harmful',
                      'trustworthysources', 'misleadingfactualerror', 'misleadingmanipulatedmedia',
                      'misleadingoutdatedinformation', 'misleadingmissingimportantcontext',
                      'misleadingunverifiedclaimasfact', 'misleadingsatire', 'misleadingother'])

# Substitute classification values with binary values
df = df.replace("MISINFORMED_OR_POTENTIALLY_MISLEADING", "Misinformed/Misleading")
df = df.replace("NOT_MISLEADING", "Not Misleading")
# Classification as "misinformed or potentially misleading"
misleading = df[df["classification"] == "Misinformed/Misleading"] 
# Classification as "not misleading”
not_misleading = df[df["classification"] == "Not Misleading"]

# Percentage of tweets classified as misinformation
print("Percentage of Birdwatch tweets classified as misinformation is: ",(len(misleading)/len(df))*100)

# Retrieve notes without stop words to generate word cloud externally
notes = df["summary"]
notes.to_csv("word_cloud_data")

# Plot frequency of classification data
d = sns.displot(df['classification'], kde = False, color ='blue')
d.fig.suptitle('Birdwatch Data Classification Frequency')
d.set_axis_labels(x_var="Classification", y_var="Frequency")
plt.show()

# Plot density of classification data
d = sns.displot(df['classification'], kde = False, color ='green', stat ='percent')
d.fig.suptitle('Birdwatch Data Classification Density')
d.set_axis_labels(x_var="Classification", y_var="Density")
plt.show()

# Validation difficulty
easy = df[df["validationdifficulty"] == "EASY"]
challenging = df[df["validationdifficulty"] == "CHALLENGING"]
print("Percentage of Birdwatch tweets classified as challenging to classify is: ",(len(challenging)/len(df))*100)

# Tweet's potential harm
harmful = df[df["harmful"] == "CONSIDERABLE_HARM"]
print("Percentage of Birdwatch tweets considered to cause considerable harm if believed by many: ",(len(harmful)/len(df))*100)

# Sources provided to classify tweet
source = df[df["trustworthysources"] == 1]
print("Percentage of Birdwatch tweets linked to sources considered trustworthy: ",(len(source)/len(df))*100)


# REASONS TWEETS ARE CATEGORIZED AS MISLEADING
# Tweet contains a factual error
factual = df[df["misleadingfactualerror"] == 1]
print("Percentage of tweets considered misleading due to a factual error: ",(len(factual)/len(df))*100)

# Tweet contains manipulated media
media = df[df["misleadingmanipulatedmedia"] == 1]
print("Percentage of tweets considered misleading due to manipulated media: ",(len(media)/len(df))*100)

# Tweet contains outdated information
outdated = df[df["misleadingoutdatedinformation"] == 1]
print("Percentage of tweets considered misleading due to outdated information: ",(len(outdated)/len(df))*100)

# Tweet misses important context
context = df[df["misleadingmissingimportantcontext"] == 1]
print("Percentage of tweets considered misleading due to missing context: ",(len(context)/len(df))*100)

# Tweet presents unverified claim as fact
unverified = df[df["misleadingunverifiedclaimasfact"] == 1]
print("Percentage of tweets considered misleading due to presenting unverified claim as fact: ",(len(unverified)/len(df))*100)

# Tweet contains satire
satire = df[df["misleadingsatire"] == 1]
print("Percentage of tweets considered misleading due to containing satire: ",(len(satire)/len(df))*100)

# Other reasons
other = df[df["misleadingother"] == 1]
print("Percentage of tweets considered misleading due to other reasons: ",(len(other)/len(df))*100)




