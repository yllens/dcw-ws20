""" Gap options:
    - half
    - half+1
    - half-1
    - removing only inflectional morpheme on content words ?
    - skip function words ?

    Named entities:

    Nouns starting with 'Np' = proper nouns (named entities) (RUSSIAN)
    'NE' (GERMAN)
    skip TRUNC (GERMAN)

    Tagset source: http://corpus.leeds.ac.uk/mocky/msd-ru.html
"""
from nltk.stem import SnowballStemmer, Cistem, LancasterStemmer


class Gapper:
    def __init__(self, words, sentences, num_gaps, infile_path, tagfile_path, language, condition):
        self.infile_path = infile_path
        self.tagfile_path = tagfile_path
        self.words = words                              # List of [token, pos tag, lemma] for each word in input file
        self.sentences = sentences                      # List of full sentences
        self.gapped_tokens, self.gapped_sents = [], []  # Lists of gapped tokens and gapped sentences
        self.merged_tokens = []                         # List of tokens merged with punctuation
        self.gap_count = 0                              # Number of gapped words
        self.num_gaps = num_gaps                        # Number of gaps to generate
        self.named_entities = []
        self.condition = condition
        self.language = language
        self.content_tags = []

    def generate_gaps(self, save_dir):
        if self.condition in ['lexical', 'morphological']:
            self.get_stemmed_gaps()
        else:
            self.get_gaps()

        self.merge_punctuation(), self.regroup_sentences()

        if self.gap_count < self.num_gaps:
            print('Error: Text is too short (only {} gaps were created).'.format(self.gap_count))
        else:
            if save_dir:
                try:
                    with open(save_dir, 'w') as outfile:
                        outfile.write(str(self.gapped_sents))
                except FileNotFoundError:
                    return 'Error: File does not exist at {}'.format(save_dir)
            if self.named_entities:
                ne = self.named_entities
            else:
                ne = '(none)'

            return print('Gapping is complete! Your text has a total of {} gaps, {} sentences, and'
                         ' {} words.\nNamed entities: {}'
                         ''.format(self.num_gaps, len(self.sentences), len(self.words), ne))

    def get_gaps(self):
        """

        :return:
        """
        punctuation = '[!\"#$%&\'()*+,-./:;<=>?@\\[\\]^_`{|}~»«›‹„“”‚‘‐‑‒–—―−﹣]'
        named_entities = tuple(['Np', 'NE', 'NP0'])
        idx = 0

        self.set_content_tags()
        self.content_tags = tuple(self.content_tags)

        # if self.condition in ['nouns', 'verbs', 'adjectives']:
        #     self.num_gaps = len([word for word in self.words if word[1].startswith(named_entities)
        #                          and word[1].startswith(self.content_tags) and len(word[0]) > 3])

        for word in self.words:
            token, pos_tag, lemma = word

            # If tag is punctuation, skip
            if token in punctuation:
                self.gapped_tokens.append(token)
                continue

            # If token is a named entity, skip
            if pos_tag.startswith(named_entities):
                self.gapped_tokens.append(token)
                self.named_entities.append(token)
                idx -= 1
                continue

            if self.gap_count < self.num_gaps:
                if idx % 2 == 1:
                    # If the word is a content word and longer than 3 characters, add a gap
                    if not pos_tag.startswith(named_entities) and pos_tag.startswith(self.content_tags) and len(token) >= 2:
                        word_len = int(len(token) / 2)

                        # Create gaps
                        word = token[:word_len]
                        gap = '[gap]' + token[word_len:] + '[/gap]'
                        gapped_word = word + gap
                        self.gapped_tokens.append(gapped_word)
                        self.gap_count += 1

                    # If not a content word, named entity, or is shorter than 3 characters, do not add a gap
                    else:
                        idx -= 1
                        self.gapped_tokens.append(token)

                # Append un-gapped tokens
                else:
                    self.gapped_tokens.append(token)

            # Append leftover tokens when num_gaps is exceeded
            else:
                self.gapped_tokens.append(token)

            idx += 1

    def get_stemmed_gaps(self):
        if self.language == 'ru':
            stemmer = SnowballStemmer('russian')
        elif self.language == 'en':
            stemmer = LancasterStemmer()
        elif self.language == 'de':
            stemmer = Cistem()
        else:
            return 'Error: Please enter a valid language.'

        punctuation = '[!\"#$%&\'()*+,-./:;<=>?@\\[\\]^_`{|}~»«›‹„“”‚‘‐‑‒–—―−﹣]'
        named_entities = tuple(['Np', 'NE', 'NP0'])
        idx = 0

        self.set_content_tags()
        self.content_tags = tuple(self.content_tags)

        for word in self.words:
            token, pos_tag, lemma = word
            gapped_word = ''

            # If tag is punctuation, skip
            if token in punctuation:
                self.gapped_tokens.append(token)
                continue

            # If token is a named entity, skip
            if pos_tag.startswith(named_entities):
                self.gapped_tokens.append(token)
                self.named_entities.append(token)
                idx -= 1
                continue

            if self.gap_count < self.num_gaps:
                if idx % 2 == 1:
                    # If the word is a content word and longer than 3 characters, add a gap
                    if not pos_tag.startswith(named_entities) and pos_tag.startswith(self.content_tags) and len(token) >= 2:

                        if self.language in ['ru', 'en']:
                            token_stem = stemmer.stem(token)

                            if 'ё' in token:
                                char_idx = [i for i, c in enumerate(list(token)) if c == 'ё' and i < len(token_stem)]
                                for idx in char_idx:
                                    token_stem = token_stem[:idx] + 'ё' + token_stem[idx + 1:]

                            affix = token.replace(token_stem, '')

                            if self.condition == 'lexical':
                                if token_stem != token:
                                    gapped_word = '[gap]' + token_stem + '[/gap]' + affix
                                else:
                                    gapped_word = token_stem
                                    idx -= 1
                            elif self.condition == 'morphological':
                                if token_stem != token:
                                    gapped_word = token_stem + '[gap]' + affix + '[/gap]'
                                else:
                                    gapped_word = token_stem
                                    idx -= 1
                            else:
                                print('Error: gaps not generated.')

                        elif self.language == 'de':
                            token_stem = stemmer.stem(token)

                            if token[0].upper() == token[0]:
                                token_stem = token[0] + token_stem[1:]

                            for char in ['ä', 'ö', 'ü']:
                                if char in token:
                                    char_idx = [i for i, c in enumerate(list(token)) if c == char and i < len(token_stem)]
                                    for idx in char_idx:
                                        token_stem = token_stem[:idx] + char + token_stem[idx + 1:]

                            if 'ß' in token:
                                char_idx = [i for i, c in enumerate(list(token)) if c == 'ß' and i < len(token_stem)]
                                for idx in char_idx:
                                    token_stem = token_stem[:idx] + 'ß' + token_stem[idx + 2:]

                            affixes = token.replace(token_stem, '_').split('_')

                            if self.condition == 'lexical':
                                if token_stem != token:
                                    if len(affixes) == 2 and affixes[0]:
                                        gapped_word = affixes[0] + '[gap]' + token_stem + '[/gap]' + affixes[1]
                                    else:
                                        gapped_word = '[gap]' + token_stem + '[/gap]' + affixes[1]
                                else:
                                    gapped_word = token_stem
                                    idx -= 1
                            elif self.condition == 'morphological':
                                if token_stem != token:
                                    if len(affixes) == 2 and affixes[0]:
                                        gapped_word = '[gap]' + affixes[0] + '[/gap]' + token_stem + '[gap]' + affixes[1] + '[/gap]'
                                    else:
                                        gapped_word = token_stem + '[gap]' + affixes[1] + '[/gap]'
                                else:
                                    gapped_word = token_stem
                                    idx -= 1
                            else:
                                print('Error: gaps not generated.')
                        else:
                            print('Error: gaps not generated.')

                        self.gapped_tokens.append(gapped_word)
                        self.gap_count += 1

                    # If not a content word, named entity, or is shorter than 3 characters, do not add a gap
                    else:
                        idx -= 1
                        self.gapped_tokens.append(token)

                # Append un-gapped tokens
                else:
                    self.gapped_tokens.append(token)

            # Append leftover tokens when num_gaps is exceeded
            else:
                self.gapped_tokens.append(token)

            idx += 1

    def merge_punctuation(self):
        """

        :return:
        """
        punctuation_right = '.,!?)»]}:'
        punctuation_left = '(«"[{'

        for token in self.gapped_tokens:
            if self.merged_tokens:

                if token == '"' and not self.merged_tokens[-1].startswith('"'):
                    self.merged_tokens.append(token)
                    continue
                elif token == '"' and self.merged_tokens[-1].startswith('"'):
                    merged_token = self.merged_tokens.pop() + token
                    self.merged_tokens.append(merged_token)
                    continue

                # If the previous token in the list is left-punctuation
                if self.merged_tokens[-1] in punctuation_left:
                    merged_token = self.merged_tokens.pop() + token
                    self.merged_tokens.append(merged_token)

                    # Skip next item (duplicated token)
                    continue

                # If the current token is right-punctuation
                elif token in punctuation_right:
                    merged_token = self.merged_tokens.pop() + token
                    self.merged_tokens.append(merged_token)

                # If the current token is not right-punctuation
                else:
                    self.merged_tokens.append(token)

            # If first item in gapped_tokens list
            else:
                self.merged_tokens.append(token)

    def regroup_sentences(self):
        """

        :return:
        """
        self.gapped_sents.append(self.sentences[0])
        self.gapped_sents.append(' '.join(self.merged_tokens))
        self.gapped_sents.append(self.sentences[-1])
        self.gapped_sents = ' '.join(self.gapped_sents)

    def set_content_tags(self):
        if self.condition in ['all', 'lexical', 'morphological']:
            if self.language == 'ru':
                self.content_tags = ['N', 'V', 'A', 'R', 'P', 'S', 'C', 'M', 'Q']
            elif self.language == 'en':
                self.content_tags = ['N', 'V', 'A', 'C', 'D', 'E', 'O', 'P']
            elif self.language == 'de':
                self.content_tags = ['N', 'F', 'V', 'AD', 'AP', 'ART', 'CARD', 'K', 'P']
            else:
                return 'Gapper error: Please enter a valid language.'

        elif self.condition == 'content':
            if self.language == 'ru':
                self.content_tags = ['N', 'V', 'A', 'R']
            elif self.language == 'en':
                self.content_tags = ['N', 'V', 'AV', 'AJ']
            elif self.language == 'de':
                self.content_tags = ['N', 'F', 'V', 'ADV', 'ADJ']
            else:
                return 'Gapper error: Please enter a valid language.'

        elif self.condition == 'nouns':
            if self.language in ['ru', 'en']:
                self.content_tags = 'N'
            elif self.language == 'de':
                self.content_tags = ['N', 'F']
            else:
                return 'Gapper error: Please enter a valid language.'

        elif self.condition == 'verbs':
            if self.language in ['en', 'ru', 'de']:
                self.content_tags = 'V'
            else:
                return 'Error: Please enter a valid language.'

        elif self.condition == 'adjectives':
            if self.language == 'en':
                self.content_tags = 'AJ'
            if self.language == 'ru':
                self.content_tags = 'A'
            elif self.language == 'de':
                self.content_tags = 'ADJ'
            else:
                return 'Error: Please enter a valid language.'

        else:
            return 'Gapper error: Please enter a valid language.'
