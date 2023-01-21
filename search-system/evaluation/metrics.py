import numpy as np

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)


def get_precisions(results: list, relevant: list):
    return [
        round(len([
            doc 
            for doc in results[:idx]
            if doc in relevant
        ]) / idx, 5)
        for idx, _ in enumerate(results, start=1)
    ]


def get_recalls(results:list, relevant: list):
    return [
        round(len([
            doc for doc in results[:idx]
            if doc in relevant
        ]) / len(relevant), 5)
        for idx, _ in enumerate(results, start=1)
    ]


@metric
def ap(results, relevant):
    """Average Precision"""
    num = 1 / len(relevant)
    all_recalls = [round(x, 5) for x in np.arange(0, 1 + num, num)]
    recalls = get_recalls(results, relevant)
    precisions = get_precisions(results, relevant)   

    best = { x: 0 for x in all_recalls } # Best precision for each recall
    for r, p in list(zip(recalls, precisions)):
        if best[r] < p:
            best[r] = p

    return sum(best.values()) / len(best.values())


@metric
def recall(results, relevant):
    return len([doc for doc in results if doc in relevant]) / len(relevant)


@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc in relevant])/n


@metric
def p5(results, relevant, n=5):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc in relevant])/n


@metric
def recall(results, relevant):
    return len([doc for doc in relevant if doc in results]) / len(relevant)


@metric
def precision(results, relevant):
    return len([doc for doc in results if doc in relevant]) / len(results)


def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

