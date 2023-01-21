import matplotlib.pyplot as plt
import pandas as pd
import os

from precision_recall_curve import plot_precision_recall_curve
from metrics import get_precisions, get_recalls, ap, calculate_metric, p5


def save_metrics(qrels: dict, info_need: str):

    if not os.path.exists("./results"):
        os.makedirs("./results")

    # Calculate precision at 10, average precision and other metrics
    evaluation_metrics = {
        'ap': 'Average Precision',
        'p10': 'Precision at 10 (P@10)',
        'p5': 'Precision at 5 (P@5)',
        'recall': 'Recall'
    }

    # Rocchio algorithm
    df_rocchio = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, qrels[info_need]['rocchio_results'], qrels[info_need]['expected_results'])]
            for m in evaluation_metrics
        ]
    )

    # Independent Boosts schema
    df_independent_boosts = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, qrels[info_need]['independent_boosts_results'], qrels[info_need]['expected_results'])]
            for m in evaluation_metrics
        ]
    )

    # Good schema
    df_good = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, qrels[info_need]['good_results'], qrels[info_need]['expected_results'])]
            for m in evaluation_metrics
        ]
    )

    # Base schema
    df_base = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, qrels[info_need]['base_results'], qrels[info_need]['expected_results'])]
            for m in evaluation_metrics
        ]
    )

    # Bad schema
    df_bad = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, qrels[info_need]['bad_results'], qrels[info_need]['expected_results'])]
            for m in evaluation_metrics
        ]
    )

    with open('results/{}.tex'.format(info_need), 'w') as tf:
        tf.write("\n\n{}\n".format("Rocchio Algorithm"))
        tf.write(df_rocchio.style.to_latex())
        tf.write("\n\n{}\n".format("Independent Boosts schema"))
        tf.write(df_independent_boosts.style.to_latex())
        tf.write("\n\n{}\n".format("Good schema"))
        tf.write(df_good.style.to_latex())
        tf.write("\n\n{}\n".format("Base schema"))
        tf.write(df_base.style.to_latex())
        tf.write("\n\n{}\n".format("Bad schema"))
        tf.write(df_bad.style.to_latex())


def save_map(qrels: dict):

    if not os.path.exists("./results"):
        os.makedirs("./results")

    # Mean average precision
    rocchio_map = 0
    independent_boosts_schema_map = 0
    good_schema_map = 0
    base_schema_map = 0
    bad_schema_map = 0
    counter = 0

    for info_need in qrels.keys():
        rocchio_map += ap(qrels[info_need]['rocchio_results'], qrels[info_need]['expected_results'])
        independent_boosts_schema_map += ap(qrels[info_need]['independent_boosts_results'], qrels[info_need]['expected_results'])
        good_schema_map += ap(qrels[info_need]['good_results'], qrels[info_need]['expected_results'])
        base_schema_map += ap(qrels[info_need]['base_results'], qrels[info_need]['expected_results'])
        bad_schema_map += ap(qrels[info_need]['bad_results'], qrels[info_need]['expected_results'])
        counter += 1
    
    rocchio_map /= counter
    independent_boosts_schema_map /= counter
    good_schema_map /= counter
    base_schema_map /= counter
    bad_schema_map /= counter

    df = pd.DataFrame(data=[["Rocchio Algorithm", rocchio_map], ["Independent Boosts Schema", independent_boosts_schema_map], ["Good schema", good_schema_map], ["Base schema", base_schema_map], ["Bad schema", bad_schema_map]], 
        columns=["Schema", "Mean Average Precision (map)"])

    with open('results/map.tex', 'w') as tf:
        tf.write(df.style.to_latex())


def save_mean_precision_at5(qrels: dict):
    if not os.path.exists("./results"):
        os.makedirs("./results")

    # Mean Precision at 5
    rocchio_pat5 = 0
    independent_boosts_schema_pat5 = 0
    good_schema_pat5 = 0
    base_schema_pat5 = 0
    bad_schema_pat5 = 0
    counter = 0

    for info_need in qrels.keys():
        rocchio_pat5 += p5(qrels[info_need]['rocchio_results'], qrels[info_need]['expected_results'])
        independent_boosts_schema_pat5 += p5(qrels[info_need]['independent_boosts_results'], qrels[info_need]['expected_results'])
        good_schema_pat5 += p5(qrels[info_need]['good_results'], qrels[info_need]['expected_results'])
        base_schema_pat5 += p5(qrels[info_need]['base_results'], qrels[info_need]['expected_results'])
        bad_schema_pat5 += p5(qrels[info_need]['bad_results'], qrels[info_need]['expected_results'])
        counter += 1
    
    rocchio_pat5 /= counter
    independent_boosts_schema_pat5 /= counter
    good_schema_pat5 /= counter
    base_schema_pat5 /= counter
    bad_schema_pat5 /= counter

    df = pd.DataFrame(data=[["Rocchio Algorithm", rocchio_pat5], ["Independent Boosts Schema", independent_boosts_schema_pat5], ["Good schema", good_schema_pat5], ["Base schema", base_schema_pat5], ["Bad schema", bad_schema_pat5]], 
        columns=["Schema", "Mean Precision At 5"])

    with open('results/mp5.tex', 'w') as tf:
        tf.write(df.style.to_latex())


def plot_all_schemas(qrels: dict, info_need: str):

    if not os.path.exists("./results"):
        os.makedirs("./results")

    plt.clf()

    if len(info_need) > 60:
        plt.title(info_need[:40] + '-\n' + info_need[40:])
    else:
        plt.title(info_need)

    # Base schema
    recall_values = get_recalls(qrels[info_need]['base_results'], qrels[info_need]['expected_results'])
    precision_values = get_precisions(qrels[info_need]['base_results'], qrels[info_need]['expected_results'])
    plot_precision_recall_curve("base_schema", info_need, recall_values, precision_values, 'b')
    # Bad schema
    recall_values = get_recalls(qrels[info_need]['bad_results'], qrels[info_need]['expected_results'])
    precision_values = get_precisions(qrels[info_need]['bad_results'], qrels[info_need]['expected_results'])
    plot_precision_recall_curve("bad_schema", info_need, recall_values, precision_values, 'r')
    # Good schema
    recall_values = get_recalls(qrels[info_need]['good_results'], qrels[info_need]['expected_results'])
    precision_values = get_precisions(qrels[info_need]['good_results'], qrels[info_need]['expected_results'])
    plot_precision_recall_curve("good_schema", info_need, recall_values, precision_values, 'g')
    # Independent Boosts schema
    recall_values = get_recalls(qrels[info_need]['independent_boosts_results'], qrels[info_need]['expected_results'])
    precision_values = get_precisions(qrels[info_need]['independent_boosts_results'], qrels[info_need]['expected_results'])
    plot_precision_recall_curve("independent_boosts_schema", info_need, recall_values, precision_values, 'y')
    # Rocchio Algorithm
    recall_values = get_recalls(qrels[info_need]['rocchio_results'], qrels[info_need]['expected_results'])
    precision_values = get_precisions(qrels[info_need]['rocchio_results'], qrels[info_need]['expected_results'])
    plot_precision_recall_curve("rocchio_algorithm", info_need, recall_values, precision_values, 'm')

    plt.savefig('results/{}.pdf'.format(info_need))
    plt.savefig('results/{}.png'.format(info_need))