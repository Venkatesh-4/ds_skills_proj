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
keywords_analyst = []
counts=[]
percentage=[]
tot_count=0
for word, count in word_freq.most_common():
    if count>=2 and word!='':
        # print(f"{word}: {count}")
        keywords_analyst.append(word)
        counts.append(count)
        tot_count = tot_count+count
for i in counts:
    percentage.append((i/tot_count)*100)

# Top keywords with their percentage of occarance 
count_keywords = pd.DataFrame({'keywords': keywords_analyst, 'counts': counts, 'percentage': percentage})
# print(count_keywords)


# print(keywords_analyst)      

# ploting keywords
# wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=200).generate_from_frequencies(word_freq)
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

g = sns.barplot(count_keywords, x="keywords", y="percentage")
g.set_xticklabels(g.get_xticklabels(), 
                          rotation=45, 
                          horizontalalignment='right')
plt.subplots_adjust(bottom=0.4)
plt.xlabel("")
plt.ylabel("Likelyhood to be in job posting (%)")
plt.title('Keyword Analysis') 
plt.show()






