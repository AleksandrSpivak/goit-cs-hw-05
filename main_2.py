import requests
import string
import matplotlib.pyplot as plt

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text):

    text = remove_punctuation(text)
    words = text.lower().split()

    with ThreadPoolExecutor(7) as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor(7) as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(top_words):

    plt.barh([x[0] for x in top_words], [x[1] for x in top_words])

    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.title("Top 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":

    url = "https://gutenberg.net.au/ebooks01/0100021.txt"

    text = get_text(url)
    if text:
        result_mpr = map_reduce(text)

        top_10 = list(sorted(result_mpr.items(), key=lambda x: x[1], reverse=True))[:10]

        visualize_top_words(top_10)

        print("Результат підрахунку слів:", top_10)

    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
