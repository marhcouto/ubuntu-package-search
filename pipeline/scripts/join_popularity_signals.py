import pandas as pd
import math

def main():
    pop_df = pd.read_csv('out/csv_data/clean/pop-contest.csv')
    packages_df = pd.read_csv('out/csv_data/clean/final_solr.csv')
    packages_df['Depends'] = packages_df['Depends'].fillna("")
    packages_df['Recommends'] = packages_df['Recommends'].fillna("")
    packages_df['Suggests'] = packages_df['Suggests'].fillna("")
    packages_df['Breaks'] = packages_df['Breaks'].fillna("")
    packages_df['Conflicts'] = packages_df['Conflicts'].fillna("")
    packages_df['Replaces'] = packages_df['Replaces'].fillna("")
    pop_df.rename(columns={"name": "Package", "inst": "Downloads", "vote": "Regularly Used", "recent": "Recently Updated"}, inplace=True)
    new_df = pd.merge(packages_df, pop_df[['Package', 'Downloads', 'Regularly Used', 'Recently Updated']], how='left', on='Package')

    section_metrics_median = {}
    for section in new_df['Section'].unique():
        section_medians = new_df[new_df['Section'] == section].median(skipna=True, numeric_only=True)
        section_metrics_median[section] = [
            section_medians['Downloads'],
            section_medians['Regularly Used'], 
            section_medians['Recently Updated']
        ]
    
    new_df['Downloads'] = new_df[['Section', 'Downloads']].apply(lambda x: section_metrics_median[x['Section']][0] if math.isnan(x['Downloads']) else x['Downloads'], axis='columns')
    new_df['Regularly Used'] = new_df[['Section', 'Regularly Used']].apply(lambda x: section_metrics_median[x['Section']][1] if math.isnan(x['Regularly Used']) else x['Regularly Used'], axis='columns')
    new_df['Recently Updated'] = new_df[['Section', 'Recently Updated']].apply(lambda x: section_metrics_median[x['Section']][2] if math.isnan(x['Recently Updated']) else x['Recently Updated'], axis='columns')

    new_df['Downloads'] = new_df['Downloads'].astype('int64')
    new_df['Regularly Used'] = new_df['Regularly Used'].astype('int64')
    new_df['Recently Updated'] = new_df['Recently Updated'].astype('int64')
    new_df.to_csv('out/csv_data/clean/full_final_solr.csv', index=False)


if __name__ == "__main__":
    main()