#!/usr/bin/env python3

import os
import re
import pandas as pd
from tabulate import tabulate
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

analysis_dir_name = 'out/analysis/'
df = pd.read_csv('out/csv_data/clean/final.csv')
df = df.dropna(subset='Package')

def create_analysis_dir():
    if not os.path.exists(analysis_dir_name):
        os.makedirs(analysis_dir_name)

def caracterize_columns():
    n_records = len(df.index)
    na_char = df.drop(columns=['Origin', 'N_Words_Description']).notna().sum().apply(lambda x: '{:.1f}'.format((x / n_records) * 100))
    with open(analysis_dir_name + 'na_char.tex', 'w') as f:
        f.write(tabulate([x for x in zip(na_char.index, na_char.values)], headers=['Column', 'Valid Values (%)'], tablefmt="latex"))

def package_num_per_sec():
    n_top = 15
    all_sections = df['Section'].value_counts()
    top_section_count = all_sections[:n_top]
    indexes = [x for x in top_section_count.index]
    indexes.reverse()
    values = np.flip(top_section_count.values)
    
    y_pos = np.arange(len(indexes))
    _, ax = plt.subplots()
    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos, labels=indexes)
    ax.set_title('Number of packages at the top {} sections'.format(n_top))
    ax.set_xlabel('Number of packages')
    ax.set_ylabel('Section')
    plt.savefig(analysis_dir_name + 'top_pack_num_per_sec.pdf', bbox_inches='tight')
    plt.close()

    other_section_sum = np.sum(all_sections[n_top:])
    _, axis = plt.subplots()
    axis.pie([np.sum(top_section_count), other_section_sum], labels=['Top {}'.format(n_top), "Other ({})".format(len(all_sections) - n_top)], autopct='%1.1f%%')
    axis.axis('equal')
    axis.set_title('Ratio of the number of packages at the top {} sections'.format(n_top))
    plt.savefig(analysis_dir_name + 'ratio_top_sec_pack_num.pdf', bbox_inches='tight')
    plt.close()

def packages_per_origin():
    category_reg = df['Origin'].value_counts()
    _, ax = plt.subplots()
    bars = ax.bar(category_reg.index, category_reg.values)
    ax.bar_label(bars)
    plt.savefig(analysis_dir_name + 'num_pack_origin.pdf', bbox_inches='tight')
    plt.close()

    with open(analysis_dir_name + 'n_pack_per_orig.tex', 'w') as f:
        f.write(tabulate([x for x in zip(category_reg.index, category_reg.values)], headers=['Origin', 'Number of Packages'], tablefmt="latex"))

def generate_word_clouds(section):
    stopwords = set(STOPWORDS)
    section_data = df[df['Section'] == section]['Description']
    section_text_list = []
    for data in section_data:
        section_text_list += [x.lower() for x in re.split(r' |\\n', data) if len(x) > 1]
    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=stopwords, min_font_size=10, collocations=False).generate(" ".join(section_text_list))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(analysis_dir_name + '{}_wordcloud.pdf'.format(section))
    plt.close()
    


def main():
    caracterize_columns()
    package_num_per_sec()
    packages_per_origin()
    generate_word_clouds('python')
    generate_word_clouds('haskell')
    generate_word_clouds('ruby')
    generate_word_clouds('rust')
    generate_word_clouds('perl')


if __name__ == "__main__":
    main()