import streamlit as st  # type: ignore


def levenshtein_distance(token1, token2):
    distances = [[0] * (len(token2) + 1) for _ in range(len(token1) + 1)]

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                prev_min = distances[t1 - 1][t2 - 1]
                distances[t1][t2] = min(prev_min + 1,
                                        distances[t1][t2 - 1] + 1,
                                        distances[t1 - 1][t2] + 1)

    return distances[len(token1)][len(token2)]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set(line.strip().lower() for line in lines))
    return words


vocabs = load_vocab(file_path='./data/vocab.txt')

st.title('Word Correction')
word = st.text_input('Your Word')

if st.button('Compute'):
    distances = dict()
    for vocab in vocabs:
        distances[vocab] = levenshtein_distance(word, vocab)
    sorted_distance = dict(sorted(distances.items(), key=lambda item: item[1]))
    correct_word = list(sorted_distance.keys())[0]
    st.write('Correct: ', correct_word)
