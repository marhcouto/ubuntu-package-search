import matplotlib.pyplot as plt


def plot_precision_recall_curve(schema_name: str, info_need: str, recall_values: list, precision_values: list, color: str):

    plt.plot(recall_values, precision_values, '-{}D'.format(color), label=schema_name)
    plt.xlim([-0.1, 1.1])
    plt.ylim([-0.1, 1.1])
    plt.legend()

    
