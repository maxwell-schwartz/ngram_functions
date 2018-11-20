'''
A variety of functions for calculating ngrams,
adding starting and ending tags, and generating
text from a Markov chain.
'''

import argparse
import json
import random

def get_ngrams(text, n, word_dict):
    '''
    For each word in word_dict, create a list of
    n-1 grams that follow it.
    '''

    if n < 2:
        return word_dict

    for word in word_dict:
        word_dict[word][n] = []

    for t in text:
        if len(t) < n:
            continue
        for i, word in enumerate(t[:-n+1]):
            word_dict[word][n].append(t[i+1:i+n])

    return(word_dict)

def tokenize(text):
    '''
    Given a list of text sections (sentences, paragraphs, etc.)
    splits and returns a list of words lists.
    '''

    return [t.split() for t in text]

def add_start_and_end_tags(text):
    '''
    Takes a list of lists of words. Inserts <start> and
    <end> tags at the beginning and end of each list.
    '''

    return [['<start>'] + t + ['<end>'] for t in text]

def create_word_dict(input_file):
    '''
    Creates a dict of words from an input file.
    Dict is in the form {word1: {}, word2" {}}
    '''

    with open(input_file, 'r') as infile:
        text = [i.strip() for i in infile.readlines()]

    tokenized_text_lists = add_start_and_end_tags(tokenize(text))
    word_set = {word for text_list in tokenized_text_lists for word in text_list}
    return tokenized_text_lists, {word: {} for word in word_set}    

def generate_text(word_dict, n, seed, end_cue):
    '''
    Given a starting seed and n, generate text.
    '''

    if not word_dict[seed][n]:
        return 'Cannot generate with starting seed {}.'.format(seed)

    gen_text = [seed]
    while gen_text[-1] != end_cue:
        option_list = word_dict[gen_text[-1]].get(n)
        temp_n = n
        while not option_list and temp_n > 1:
            option_list = word_dict[gen_text[-1]].get(temp_n)
            temp_n = n - 1
        if option_list:
            gen_text += random.choice(option_list)
        else:
            return 'Error'

    if seed == '<start>':
        gen_text = gen_text[1:]
    if end_cue == '<end>':
        gen_text = gen_text[:-1]

    return ' '.join(gen_text)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', 
                        help='Text file with newline breaks between sections')
    parser.add_argument('-n', '--ngram_length', type=int,
                        help='ngram length')
    args = parser.parse_args()

    t, word_dict = create_word_dict(args.input_file)

    n = args.ngram_length
    while n > 1:
        word_dict = get_ngrams(t, n, word_dict)
        n -= 1

    print(generate_text(word_dict, args.ngram_length, '<start>', '<end>'))

if __name__ == '__main__':
    main()
