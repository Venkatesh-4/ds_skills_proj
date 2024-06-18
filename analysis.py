import pandas as pd
import glob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize, MWETokenizer
from nltk.corpus import stopwords
from IPython.display import set_matplotlib_formats


# Uncomment on first run
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

def split_job_type(job_type_str):
    parts = job_type_str.split(' ')
    if len(parts) == 4:
        x = parts[:-2] + ['-'.join(parts[-2:])]
        ret = [x[1], x[2], x[0]]
        return ret
    elif len(parts) == 3:
        x = parts[:-2] + ['-'.join(parts[-2:])]
        ret = [x[0], x[1], '']
        return ret
    elif len(parts) == 2:
        x = parts
        ret = [x[1], '', x[0]]
        return ret
    else:
        x = ['', '', '']
        return x

path = 'output'
files = glob.glob(path + "/*.csv")
  
# defining an empty list to store content
jobs_all = pd.DataFrame()
content = []
  
# checking all the csv files in the pth
for filename in files:
    
    # reading content of csv file
    _df = pd.read_csv(filename, index_col=None)
    content.append(_df)
  
# converting content to data frame
jobs_all = pd.concat(content)
df = jobs_all
col = df.columns.to_list()
columns_to_check = col[3:5]
jobs_all = df.drop_duplicates(subset=columns_to_check, keep='first')

# jobs_all.info()


#Exploratory data analysis
# print(jobs_all.job_title.value_counts().head(10))

jobs_all[['job_time', 'job_level', 'job_type']] = jobs_all['job_type'].apply(split_job_type).to_list()
print(jobs_all[['job_time', 'job_level', 'job_type']])

jobs_all.to_csv('output_fileaa.csv', header=True, index=True)

# job_positions = ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]

# # print(jobs_all.job_level.value_counts().head(4))
# job_type_counts = df['job_type'].value_counts()

# # Print the unique values and their counts
# print(job_type_counts)   
