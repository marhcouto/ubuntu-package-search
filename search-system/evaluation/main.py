import json
import requests

from output import plot_all_schemas, save_map, save_metrics, save_mean_precision_at5

QRELS_FILE = "./qrels.json"
QRELS = dict()

def fetch_rocchio(query_url, relevant_documents):
    initial_response = requests.get(query_url).json()
    relevant_document_ids = list(map(lambda x: x['id'], filter(lambda x: x['package'] in relevant_documents, initial_response)))
    rocchio_documents = requests.get(query_url + "&rd={}".format(",".join(relevant_document_ids))).json()
    return list(map(lambda x: { "Package": x['package'] }, rocchio_documents))

def main():

    # Load QRELS file
    with open(QRELS_FILE, 'r') as file:
        QRELS = json.load(file)

    # Query SOLR
    for key, value in QRELS.items():
        QRELS[key]['rocchio_results'] = list(map(lambda x: x[value['interest_field']], 
            fetch_rocchio(value["query_url_rocchio"], QRELS[key]['expected_results'])))
        QRELS[key]['independent_boosts_results'] = list(map(lambda x: x[value['interest_field']], 
            requests.get(value["query_url_independent_boosts"]).json()['response']['docs']))
        QRELS[key]['good_results'] = list(map(lambda x: x[value['interest_field']], 
            requests.get(value["query_url_good"]).json()['response']['docs']))
        QRELS[key]['base_results'] = list(map(lambda x: x[value['interest_field']], 
            requests.get(value["query_url_base"]).json()['response']['docs']))
        QRELS[key]['bad_results'] = list(map(lambda x: x[value['interest_field']], 
            requests.get(value["query_url_bad"]).json()['response']['docs']))
        QRELS[key]['bad_results'] = list(map(lambda x: x[0], QRELS[key]['bad_results']))

    # Save Metrics
    for info_need in QRELS.keys():
        save_metrics(QRELS, info_need)

    # Generate precision_recall_curves
    for info_need in QRELS.keys():
        plot_all_schemas(QRELS, info_need)

    # Mean average precision
    save_map(QRELS)

    # Mean precision at 5
    save_mean_precision_at5(QRELS)


if __name__ == "__main__": 
    main()