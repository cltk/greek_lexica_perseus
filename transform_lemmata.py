from cltk.corpus.greek.beta_to_unicode import Replacer
from collections import  defaultdict

replacer = Replacer()


def file_line_generator(file):
    """Open file line-by-line"""
    with open(file) as file_opened:
        for file_line in file_opened:
            yield file_line[:-1]  # remove '\n' from end of each line


def parse_perseus_lemmata_file(file_generator, greek):
    """Parse lemmata file, looping through string for all data."""
    count = 0
    for line in file_generator:
        count += 1
        if count % 1000 == 0:
            print('Parsing line {0}'.format(count))
        line_split = line.split('\t')
        headword = line_split[0]
        headword_id = line_split[1]
        line_lemmata = line_split[2:]
        for lemma_str in line_lemmata:
            lemma_list = lemma_str.split(' ', 1)
            lemma = lemma_list[0]
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

                if greek:
                    lemma = replacer.beta_code(lemma.upper() + ' ')[:-1].lower()  # add space to get final sigma 'ς', then rm it #? why some coming out capitalized?
                    headword = replacer.beta_code(headword.upper() + ' ')[:-1].lower()  # add space to get final sigma 'ς', then rm it

                #print(lemma, headword)

                yield lemma, headword


if __name__ == '__main__':
    lemma_headword_map = {}
    greek_file_generator = file_line_generator('greek-lemmata.txt')
    greek_lemma_headword = parse_perseus_lemmata_file(greek_file_generator, greek=False)

    print('Starting to build map …')
    lemmata_dd = defaultdict(set)
    for k, v in greek_lemma_headword:
        lemmata_dd[k].add(v)

    print('Starting to write file …')
    with open('greek_lemmata_cltk.txt', 'w') as file_opened:
        file_opened.write(str(dict(lemmata_dd)))

