

from cltk.corpus.greek.beta_to_unicode import Replacer
from collections import Counter
from collections import defaultdict
import operator

replacer = Replacer()

MANUAL_REPLACEMENTS = {'ἐστὶν': 'εἰμί',
                      'ἐστὶ': 'εἰμί',
                      'ἐστί': 'εἰμί',
                      'ἐστίν': 'εἰμί',
                      'λαμβάνει': 'λαμβάνω',
                      'λάβοι': 'λαμβάνω',
                      'λαβὼν': 'λαμβάνω',
                      'λαμβάνων': 'λαμβάνω',
                      }


def file_line_generator(file):
    """Open file line-by-line"""
    with open(file) as file_opened:
        for file_line in file_opened:
            yield file_line[:-1]  # remove '\n' from end of each line


def iter_headwords(def_dict):
    for inflection, headwords in def_dict.items():
        for headword in list(headwords):
            yield headword


def make_headword_count(def_dict):
    headwords = iter_headwords(def_dict)
    return Counter(headwords)



def parse_perseus_lemmata_file(file_generator, greek):
    """Parse lemmata file, looping through string for all data."""
    count = 0
    for line in file_generator:
        count += 1
        if count % 10000 == 0:
            print('Parsing line {0}'.format(count))
        line_split = line.split('\t')
        headword = line_split[0]
        if greek:
            headword = replacer.beta_code(headword.upper() + ' ')[:-1].lower()  # add space to get final sigma 'ς', then rm it
        headword_id = line_split[1]
        line_lemmata = line_split[2:]
        for lemma_str in line_lemmata:
            lemma_list = lemma_str.split(' ', 1)
            lemma = lemma_list[0]
            if greek:
                lemma = replacer.beta_code(lemma.upper() + ' ')[:-1].lower()  # add space to get final sigma 'ς', then rm it #? why some coming out capitalized?
            lemma_pos_str = lemma_list[1]
            lemma_pos_list = lemma_pos_str.split(') (')

            for lemma_pos in lemma_pos_list:
                # rm initial paren
                if lemma_pos.startswith('('):
                    lemma_pos = lemma_pos[1:]

                # rm final paren
                if lemma_pos.endswith(')'):
                    lemma_pos = lemma_pos[:-1]

                # break out any dialect or extra data: '(epic doric ionic aeolic)', '(adverb)'
                if '(' in lemma_pos and lemma_pos.endswith(')'):
                    lemma_pos_list = lemma_pos.split(' (')
                    lemma_pos = lemma_pos_list[0]
                    lemma_pos_comment = lemma_pos_list[1][:-1]
                    lemma_pos_comment_list = lemma_pos_comment.split(' ')

                #print(lemma, headword)

                yield lemma, headword


if __name__ == '__main__':
    lemma_headword_map = {}
    file_generator = file_line_generator('greek-lemmata.txt')
    lemma_headword = parse_perseus_lemmata_file(file_generator, greek=True)

    print('Starting to build map …')
    lemmata_dd = defaultdict(set)
    for k, v in lemma_headword:
        lemmata_dd[k].add(v)

    print('Building headword frequencies …')
    headword_frequencies = make_headword_count(lemmata_dd)

    print('Building final lemma-headword dict …')
    # for any lemma with more than one possible headword
    # check each for which occurs most
    final_lemmata = {}
    for k, v in lemmata_dd.items():
        if len(list(v)) > 1:
            count_dict = {}
            for curr_hw in list(v):
                curr_count = headword_frequencies[curr_hw]
                count_dict[curr_hw] = curr_count
            # http://stackoverflow.com/a/268285
            # if tie then takes one
            top_headword = max(count_dict.items(), key=operator.itemgetter(1))[0]
            final_lemmata[k] = top_headword
        else:
            final_lemmata[k] = list(v)[0]

    # could be improved to add pairs not in final_lemmata
    for k, v in MANUAL_REPLACEMENTS.items():
        if k in final_lemmata.keys():
            final_lemmata[k] = MANUAL_REPLACEMENTS[k]


    print('Starting to write file …')
    with open('greek_lemmata_cltk.py', 'w') as file_opened:
        file_opened.write('LEMMATA = ' + str(dict(final_lemmata)))
