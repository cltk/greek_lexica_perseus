

def file_line_generator(file):
    with open(file) as file_opened:
        for line in file_opened:
            yield line[:-1]  # remove '\n' from end of each line


if __name__ == '__main__':
    file_generator = file_line_generator('greek-lemmata.txt')
    for line in file_generator:
        #line = raw_line[:-1]
        line_split = line.split('\t')
        headword = line_split[0]
        headword_id = line_split[1]
        print(headword, headword_id)
        #print('RAW LINE:', line)
        line_lemmata = line_split[2:]
        for lemma_str in line_lemmata:
            #print('RAW LEMMA:', lemma_str)
            lemma_list = lemma_str.split(' ', 1)
            lemma = lemma_list[0]
            lemma_pos_str = lemma_list[1]
            lemma_pos_list = lemma_pos_str.split(') (')

            #for lemma_pos in lemma_pos_list:

            #print(lemma)
            print(lemma_pos_list)

        input()
