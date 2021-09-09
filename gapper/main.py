import time
import utils
import os

from Tokenizer import Tokenizer
from Gapper import Gapper

start_time = time.process_time()


def main(source_dir, out_dir, lang, conds):
    """
    Process raw texts and generate gapped versions according to different conditions:
        - 'all':            canonical C-Test gapping
        - 'adjectives':     only adjectives are gapped
        - 'nouns':          only nouns are gapped
        - 'verbs':          only verbs are gapped
        - 'lexical':        only stems are gapped (left-hand deletion)
        - 'morphological':  only morphems are gapped (right-hand deletion)
        - 'content':        only content words are gapped
    :param: source_dir: path to directory containing the raw texts
    :param: out_dir:    path to directory under which to save processed files
    :param: lang:       language of the raw texts
    :param: conditions: processing conditions (e.g. 'all') (NOTE: needs to be a list)
    """

    # Get all files from source directory containing the raw texts
    raw_text_files = [file for file in os.listdir(source_dir) if file.startswith(tuple(['A', 'B', 'C']))]

    # Check/Create token_dir
    tokens_dir = f'{out_dir}/tokens'
    if not os.path.isdir(tokens_dir): # makes sure the tokens_dir exists
        os.makedirs(tokens_dir)

    # Iterate over the conditions specified in cond
    for condition in conds:

        # For each condition save gapped texts to a different subdirectory in the out_dir
        gap_dir = f'{out_dir}/gapped/{condition}'
        if not os.path.isdir(gap_dir): # makes sure the gap_dir exists
            os.makedirs(gap_dir)

        # Set number of gaps
        if condition == 'all':
            num_gaps = 25
        else:
            num_gaps = 5

        for text_file in raw_text_files:
            # Print currently processed file
            current_file = f'{source_dir}/{text_file}'
            print(current_file)

            # Set path for saving gapped text
            outfile = f"{gap_dir}/{text_file.replace('.txt', '_Gapped.txt')}"

            # Set path for saving tokens file
            token_file = f"{tokens_dir}/{text_file.replace('.txt', '_Tokens.txt')}"

            # Run tokeniser
            tk = Tokenizer(file_path=f'{source_dir}/{text_file}', token_file=token_file, language=lang)
            tk.preprocess()
            # print(tk.sentences)

            # Gap generation
            gp = Gapper(words=tk.tags, sentences=tk.sentences, num_gaps=num_gaps,
                        infile_path=current_file, tagfile_path=token_file, language=lang, condition=condition)
            gp.generate_gaps(outfile)

        # Save processed text as json
        json_file = f'{out_dir}/json/{condition}.json'
        utils.generate_json(out_dir, json_file)


if __name__ == '__main__':

    language = 'ru' # change for other languages ('de', 'ru')
    conditions = ['all'] # add to list: 'adjectives', 'nouns', 'verbs', 'lexical', 'morphological', 'content'
    source_directory = f'texts/{language}/raw'
    output_directory = f'texts/{language}'

    # call main to process raw texts
    main(source_directory, output_directory, language, conditions)

    print("\n--------------------------")
    print(time.process_time() - start_time, "seconds")
