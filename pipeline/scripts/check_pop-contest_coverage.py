import pandas as pd



def main():
    pop_df = pd.read_csv('out/csv_data/clean/pop-contest.csv')
    signals_packages_set = set(pop_df.name)
    packages_df = pd.read_csv('out/csv_data/clean/final_solr.csv')
    original_packages_set = set(packages_df.Package)

    print("From the {} packages used for solr, {} are present in the static ranks from pop-contest."
        .format(len(original_packages_set), len(original_packages_set.intersection(signals_packages_set))))
    



if __name__ == "__main__":
    main()