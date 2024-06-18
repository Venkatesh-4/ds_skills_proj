import pandas as pd
import glob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize
from nltk.tokenize.mwe import MWETokenizer
from nltk.corpus import stopwords
from IPython.display import set_matplotlib_formats
import string
from collections import Counter


# Uncomment on first run
# 
import nltk
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


def filtered_df(jobs_all, job_title, job_level):
    # filter the jobs for title (and position)
    jobs_all = jobs_all.fillna('')
    jobs_filtered = jobs_all[jobs_all.job_title.str.contains(job_title, na=False)]
    # print(jobs_filtered)
    if job_level != "":
        jobs_filtered = jobs_filtered[jobs_filtered.job_level.str.contains(job_level, na=False)]
        # print(jobs_filtered)
    # create new column for tokenized words
    jobs_filtered['tokenized_details'] = ""
    for index, row in jobs_filtered.iterrows():
        detail = row.job_details.lower() 
        values = detail.split(',')
        if len(values) > 1:
            last_value = values[-1].strip()
            if last_value.startswith("and "):
                values[-1] = last_value[4:]
        jobs_filtered.loc[index, 'tokenized_details'] = ','.join(values)
    return jobs_filtered 

# def word_cloud(jobs_filtered, keywords):
#     # convert df column to list
#     analyst_list = jobs_filtered.tokenized_details.tolist()
#     print(analyst_list)
#     # flatten list of lists
#     analyst_list = [item for sublist in analyst_list for item in sublist]
#     # filter list
#     analyst_list = [item for item in analyst_list if item in keywords]
#     # convert for wordcloud
#     analyst_list = " ".join(words for words in analyst_list)
#     # wordcloud the results
#     wc_join = WordCloud(background_color="white", collocations=False).generate(analyst_list)
#     plt.imshow(wc_join, interpolation='bilinear')
#     plt.axis("off")
#     plt.show()
#     return

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
jobs_all[['job_time', 'job_level', 'job_type']] = jobs_all['job_type'].apply(split_job_type).to_list()
# jobs_all.to_csv('output_fileaa.csv', header=True, index=True)


# jobs_all.info()


#Exploratory data analysis
# print(jobs_all.job_title.value_counts().head(10))

# print(jobs_all[['job_time', 'job_level', 'job_type']])

# job_level = ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
# print(jobs_all.job_level.value_counts().head(4))

#ANALYSIS
#Datafame filtering
analyst_entry = filtered_df(jobs_all, "Analyst", "Entry-level")
# analyst_entry.to_csv('output_fileaa.csv', header=True, index=True)

#Identifying analyst keywords

analyst_list = analyst_entry.tokenized_details
data_lists = analyst_list.str.split(',').tolist()
all_words = [word.strip() for lst in data_lists for word in lst]

word_freq = Counter(all_words)

for word, count in word_freq.most_common():
    print(f"{word}: {count}")
# #Wordcloud of keywords
# keywords_analyst = ['excel', 'sql', 'microsoft', 'tableau',  'python', 'word', 
# 'powerpoint', 'r',  'slack', 'coding', 'looker',
# 'outlook', 'azure', 'jira', 'twilio', 'server', 'snowflake', 'ai', 'warehousing', 'scrum',
# 'powerbi', 'shell', 'linux', 'sas', 'sharepoint', 'devops', 'mysql', 'c', 'visio', 
# 'javascript', 'git', 'mssql', 'vba', 'powerpoints', 'java', 'postgresql', 'spreadsheets',
# 'pandas', 'gdpr', 'elt', 'scala', 'css', 'spreadsheet', 'alteryx', 'github', 'postgres', 'power_bi', 'spss']
# word_cloud(analyst_entry, keywords_analyst)

