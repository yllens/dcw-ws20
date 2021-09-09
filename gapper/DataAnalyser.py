"""
Author: yllens, sne31196
Last edited: 9th Spetember 2021 
Desription: Contains functions for linguistic complexity analysis.
"""

import math
import pyphen


class DataAnalyser:
    def __init__(self, tags, sentences, language):
        self.language = language                         # Input language ('en' or 'ru')
        self.tags = tags                                 # List of [token, pos tag, lemma] for each word in input file
        self.words = [item[0] for item in tags
                      if item[0] not in '.,!?)»(«-–":']  # All words in input text (excluding punctuation)
        self.sentences = sentences                       # All sentences in input text
        self.lemmas = [item[2] for item in tags]         # All lemmas in input text
        self.syllables = []                              # Number of syllables in each word
        self.nouns, self.pronouns, self.verbs, \
            self.adjectives, self.adverbs = [], [], [], [], []

    def num_sentences(self):
        """ :return: total number of sentences in input text
        """
        return len(self.sentences)

    def num_words(self):
        """ :return: total number of words in input text
        """
        return len(self.words)

    def avg_word_len(self):
        """ :return: average word length (in characters) over whole input text
        """
        word_lengths = [len(token) for token in self.words]

        try:
            avg_word_len = round(sum(word_lengths) / len(word_lengths), 2)
        except ZeroDivisionError:
            avg_word_len = 0

        return avg_word_len

    def avg_sent_len(self):
        """ :return: average sentence length (in words) over whole input text
        """
        try:
            avg_sent_len = round(len(self.words) / len(self.sentences), 2)
        except ZeroDivisionError:
            avg_sent_len = 0

        return avg_sent_len

    # def conjunctions_ratio(self):
    #     """ Calculate ratio of conjunctions (num conjunctions / words).
    #
    #     :return: conjunctions ratio
    #     """
    #     conjunctions = self.conll_df[self.conll_df['UPOS'] == 'CCONJ']
    #
    #     try:
    #         conj_ratio = round(len(conjunctions) / len(self.words) * 100, 2)
    #     except ZeroDivisionError:
    #         conj_ratio = 0
    #
    #     return conj_ratio

    def get_nouns(self):
        if self.language == 'en' or self.language == 'ru':
            self.nouns = [item[0] for item in self.tags if item[1].startswith('N')]
        elif self.language == 'de':
            self.nouns = [item[0] for item in self.tags if item[1].startswith(tuple(['N', 'F']))]
        else:
            return 'Error: Please enter a valid language.'

    def get_pronouns(self):
        if self.language == 'en':
            self.pronouns = [item for item in self.tags if item[1].startswith('P')
                             and not item[1].startswith(tuple(['PU', 'PR', 'POS']))]  # PU = punctuation, PR = preposition, POS = possessive genitive ('s)
        elif self.language == 'ru':
            self.pronouns = [item for item in self.tags if item[1].startswith('P')]
        elif self.language == 'de':
            self.pronouns = [item for item in self.tags if item[1].startswith('P')
                             and not item[1].startswith('PT') and item[1] != 'PAV']    # PT = 'particle', PAV = pronomial adverb (e.g., dafür)
        else:
            return 'Error: Please enter a valid language.'

    def get_verbs(self):
        if self.language in ['en', 'ru', 'de']:
            self.verbs = [item[0] for item in self.tags if item[1].startswith('V')]
        else:
            return 'Error: Please enter a valid language.'

    def get_adverbs(self):
        if self.language == 'en':
            self.adverbs = [item[0] for item in self.tags if item[1].startswith('AV')]
        elif self.language == 'ru':
            self.adverbs = [item[0] for item in self.tags if item[1].startswith('R')]
        elif self.language == 'de':
            self.adverbs = [item[0] for item in self.tags if item[1].startswith('ADV')]
        else:
            return 'Error: Please enter a valid language.'

    def get_adjectives(self):
        if self.language == 'en':
            self.adjectives = [item[0] for item in self.tags if item[1].startswith('AJ')]
        if self.language == 'ru':
            self.adjectives = [item[0] for item in self.tags if item[1].startswith('A')]
        elif self.language == 'de':
            self.adjectives = [item[0] for item in self.tags if item[1].startswith('ADJ')]
        else:
            return 'Error: Please enter a valid language.'

    def get_num_syllables(self):
        """ Helper method for functions that require syllable count.
        """
        if self.language == 'en':
            tag = 'en_GB'
        elif self.language == 'ru':
            tag = 'ru_RU'
        elif self.language == 'de':
            tag = 'de_DE'
        else:
            return 'Error: Please enter a valid language.'

        syllabifier = pyphen.Pyphen(lang=tag)

        for word in self.words:
            syllables = syllabifier.inserted(word).split('-')
            self.syllables.append(len(syllables))

    def flesch_kincaid_grade_level(self):
        """ Calculate Flesch-Kincaid grade level.

        en formula (Flesch, 1948) = (0.39 * ASL) + (11.8 * ASW) - 15.59
        ru formula (Solovyev et al, 2018) = (0.36 * ASL) + (5.76 * ASW) − 11.97

        :return: Flesch-Kincaid grade level
        """
        avg_word_len = sum(self.syllables)/len(self.words)
        avg_sentence_len = sum([len(sentence) for sentence in self.sentences])/len(self.sentences)

        try:
            if self.language == 'en':
                score = (0.39 * avg_sentence_len) + (11.8 * avg_word_len) - 15.59
            elif self.language == 'ru':
                score = (0.36 * avg_sentence_len) + (5.76 * avg_word_len) - 11.97
            elif self.language == 'de':
                score = (0.39 * avg_sentence_len) + (11.8 * avg_word_len) - 15.59       # FIND GERMAN FORMULA
            else:
                return 'Error: Please enter a valid language.'
        except ZeroDivisionError:
            score = 0

        return round(score, 2)

    def flesch_reading_ease(self):
        """ Calculate Flesch reading ease score.

        en formula (Kincaid et al, 1975) = 206.835 - (1.015 * ASL) - (84.6 * AWL)
        ru formula (Solovyev et al, 2018) = 208.7 − (2.6 * ASL) − (39.2 * ASW)
        de formula (Amstad, 1978) = 180 - ASL - AWL * 58.5

        :return: Flesch reading ease score
        """
        avg_word_len = sum(self.syllables)/len(self.words)
        avg_sentence_len = sum([len(sentence) for sentence in self.sentences])/len(self.sentences)

        try:
            if self.language == 'en':
                score = 206.835 - (1.015 * avg_sentence_len) - (84.6 * avg_word_len)
            elif self.language == 'ru':
                score = 208.7 - (2.6 * avg_sentence_len) - (39.2 * avg_word_len)
            elif self.language == 'de':
                score = 180 - avg_sentence_len - (avg_word_len * 58.5)
            else:
                return 'Error: Please enter a valid language.'
        except ZeroDivisionError:
            score = -1

        return round(score, 2)

    # def frequent_words(self, frequencies_file):
    #     """ Get percentage of frequent words based on RNC & BNC frequency lists.
    #
    #     :param frequencies_file:  file containing the 6318 most frequent words in a language and their frequency counts
    #     :return:                  percentage of frequent words in input text
    #     """
    #     freq_file = open(frequencies_file, 'r')
    #     freq_df = pd.read_csv(freq_file, delimiter='\t')
    #     freq_file.close()
    #
    #     freq_df = pd.DataFrame.sort_values(freq_df, by='frequency', ascending=False)
    #
    #     # Match length of the en frequencies file
    #     if self.language == 'ru':
    #         freq_df = freq_df[:6318]
    #
    #     most_freq_words = freq_df['word'].values.tolist()
    #
    #     freq_words_count = 0
    #     for word in self.lemmas:
    #         if word in most_freq_words:
    #             freq_words_count += 1
    #
    #     try:
    #         freq_words = round(freq_words_count / len(self.lemmas) * 100, 2)
    #     except ZeroDivisionError:
    #         freq_words = 0
    #
    #     return freq_words

    # def lemma_overlaps_generation(self):
    #     """ Calculate lemma overlap between two and three adjacent sentences.
    #
    #     :return:  list of lists for values for two and three adjacent sentences, with a
    #                 sub-list for each sentence containing all of the overlapping lemmas
    #     """
    #     # Data frame of lemmas, their index, and their POS tag in each input text sentence
    #     lemmas_with_index = self.conll_df[['ID', 'LEMMA', 'UPOS']]
    #
    #     # Index of last item in each sentence in lemmas raw frame to group lemmas by sentence
    #     sentence_indices = lemmas_with_index.loc[lemmas_with_index['ID'].shift(-1) == 1]
    #     sentence_indices = sentence_indices.index.values.tolist()
    #     sentence_indices = [x + 1 for pair in zip(sentence_indices, sentence_indices) for x in pair]
    #     sentence_indices.insert(0, 0)
    #     sentence_indices.append(len(lemmas_with_index))
    #
    #     # Remove non-word (punctuation) lemmas
    #     lemmas_with_index['LEMMA'] = lemmas_with_index.LEMMA.str.replace('\\W', '')
    #     lemmas_with_index = lemmas_with_index[lemmas_with_index.LEMMA != '']
    #
    #     # List of tuples (lemma, POS tag)
    #     lemmas = list(zip(lemmas_with_index.LEMMA, lemmas_with_index.UPOS))
    #
    #     # List of sentences in input text split by lemma
    #     sentences = []
    #     iterator = iter(sentence_indices)
    #     for index in iterator:
    #         sentences.append(lemmas[index: next(iterator)])
    #
    #     overlaps_2, overlaps_3 = [], []
    #
    #     if len(sentences) in [0, 1]:
    #         return [], []
    #
    #     elif len(sentences) == 2:
    #         overlaps_2 = [lemma for lemma in sentences[0] if lemma in sentences[1]]
    #         overlaps_3 = [], []
    #
    #     else:
    #         for sentence in sentences:
    #             # Index of current sentence in sentences list
    #             curr_index = sentences.index(sentence)
    #
    #             # If the sentence is not one of the first two or last two sentences in the text
    #             if sentences.index(sentence) not in [0, 1, len(sentences) - 2, len(sentences) - 1]:
    #                 # Get lemma overlaps between current sentence and one left and one right neighbour
    #                 overlap_2_left = [lemma for lemma in sentence if lemma in sentences[curr_index - 1]]
    #                 overlap_2_right = [lemma for lemma in sentence if lemma in sentences[curr_index + 1]]
    #                 overlaps_2.append(overlap_2_left)
    #                 overlaps_2.append(overlap_2_right)
    #
    #                 # Get lemma overlaps between current sentence and two lefts and two right neighbours
    #                 overlap_3_left = [lemma for lemma in sentence if lemma in sentences[curr_index - 2]
    #                                   and lemma in sentences[curr_index - 1]]
    #                 overlap_3_right = [lemma for lemma in sentence if lemma in sentences[curr_index + 2]
    #                                    and lemma in sentences[curr_index + 1]]
    #                 overlaps_2.append(overlap_3_left)
    #                 overlaps_2.append(overlap_3_right)
    #
    #             # If the sentence is the second or second to last in list
    #             elif sentences.index(sentence) in [1, len(sentences) - 2]:
    #                 try:
    #                     # Try find overlap with one left neighbour and two right neighbours
    #                     overlap_2 = [lemma for lemma in sentence if lemma in sentences[curr_index - 1]]
    #                     overlap_3 = [lemma for lemma in sentence if lemma in sentences[curr_index + 2]
    #                                  and lemma in sentences[curr_index + 1]]
    #
    #                 except IndexError:
    #                     # If no left neighbours, find overlap with one right neighbour and two left neighbours
    #                     overlap_2 = [lemma for lemma in sentence if lemma in sentences[curr_index + 1]]
    #                     overlap_3 = [lemma for lemma in sentence if lemma in sentences[curr_index - 2]
    #                                  and lemma in sentences[curr_index - 1]]
    #
    #                 overlaps_2.append(overlap_2)
    #                 overlaps_3.append(overlap_3)
    #
    #             # If the sentence is the first or last in list
    #             else:
    #                 try:
    #                     # Try find overlap with left neighbours
    #                     overlap_2 = [lemma for lemma in sentence if lemma in sentences[curr_index - 1]]
    #                     overlap_3 = [lemma for lemma in sentence if lemma in sentences[curr_index - 2]
    #                                  and lemma in sentences[curr_index - 1]]
    #
    #                 except IndexError:
    #                     # If no left neighbours, find overlap with right neighbours
    #                     overlap_2 = [lemma for lemma in sentence if lemma in sentences[curr_index + 2]]
    #                     overlap_3 = [lemma for lemma in sentence if lemma in sentences[curr_index + 2]
    #                                  and lemma in sentences[curr_index + 1]]
    #
    #                 overlaps_2.append(overlap_2)
    #                 overlaps_3.append(overlap_3)
    #
    #     lengths_2 = [len(item) for item in overlaps_2]
    #     if sum(lengths_2) == 0:
    #         overlaps_2 = []
    #
    #     lengths_3 = [len(item) for item in overlaps_3]
    #     if sum(lengths_3) == 0:
    #         overlaps_3 = []
    #
    #     # Flatten lists
    #     if len(self.sentences) >= 4:
    #         overlaps_2 = [y for x in overlaps_2 for y in x]
    #     if len(self.sentences) >= 4:
    #         overlaps_3 = [y for x in overlaps_3 for y in x]
    #
    #     return overlaps_2, overlaps_3
    #
    # def lemma_overlaps_calculation(self, overlaps_2, overlaps_3):
    #     """ Calculate lemma overlap scores for two and three adjacent sentences.
    #
    #     :param overlaps_2:  list of overlapping lemmas for two adjacent sentences from get_lemma_overlaps()
    #     :param overlaps_3:  list of overlapping lemmas for three adjacent sentences from get_lemma_overlaps()
    #     :return: avg_overlap_2, avg_overlap_3: average lemma overlap scores (all lemmas)
    #              content_word_overlap_2, content_word_overlap_3: content lemma overlap scores
    #              pos_overlaps_2, pos_overlaps_3: overlap scores for each content POS
    #     """
    #     # Total number of sentences in text
    #     num_sentences = len(self.sentences)
    #
    #     # Total number of lemma overlaps in sentences
    #     num_overlaps_2 = len(overlaps_2)
    #     num_overlaps_3 = len(overlaps_3)
    #
    #     # Average lemma overlap score (all lemmas)
    #     try:
    #         avg_overlap_2 = num_overlaps_2 / num_sentences
    #     except ZeroDivisionError:
    #         avg_overlap_2 = 0
    #     try:
    #         avg_overlap_3 = num_overlaps_3 / num_sentences
    #     except ZeroDivisionError:
    #         avg_overlap_3 = 0
    #
    #     content_word_pos = ['NOUN', 'PRON', 'PROPN', 'VERB', 'ADJ', 'ADV']
    #
    #     # List of lemma overlap scores for each content POS (=len(6), items are in the order N, PRO, PROPN, V, ADJ, ADV)
    #     pos_overlaps_2, pos_overlaps_counts_2 = [], []
    #     content_words_2, content_word_overlap_2 = [], []
    #
    #     # Calculate lemma overlaps between two adjacent sentences
    #     if len(overlaps_2) > 0:
    #         try:
    #             content_words_2 = [word for word in overlaps_2 if word[1] in content_word_pos and len(word) > 0]
    #             content_word_overlap_2 = len(content_words_2) / num_sentences
    #
    #             # Calculate lemma overlap for each content POS
    #             nouns_2 = [word for word in content_words_2 if word[1] == 'NOUN']
    #             pron_2 = [word for word in content_words_2 if word[1] == 'PRON']
    #             propn_2 = [word for word in content_words_2 if word[1] == 'PROPN']
    #             verbs_2 = [word for word in content_words_2 if word[1] == 'VERB']
    #             adj_2 = [word for word in content_words_2 if word[1] == 'ADJ']
    #             adv_2 = [word for word in content_words_2 if word[1] == 'ADV']
    #
    #             all_pos = [nouns_2] + [pron_2] + [propn_2] + [verbs_2] + [adj_2] + [adv_2]
    #
    #             for pos in all_pos:
    #                 if len(pos) > 0:
    #                     pos_overlaps_counts_2.append(len(pos))
    #                 else:
    #                     pos_overlaps_counts_2.append(0)
    #
    #         except IndexError:
    #             pos_overlaps_counts_2.append(0)
    #     else:
    #         content_word_overlap_2 = 0
    #
    #     if len(pos_overlaps_counts_2) > 0:
    #         for pos in pos_overlaps_counts_2:
    #             pos_overlaps_2.append(round(pos / num_sentences, 2))
    #
    #     # Calculate lemma overlaps between three adjacent sentences
    #     pos_overlaps_3, pos_overlaps_counts_3 = [], []
    #
    #     if len(overlaps_3) > 0:
    #         lengths = [len(item) for item in overlaps_3]
    #
    #         # If list is irregularly shaped, flatten it
    #         if any(a != 2 for a in lengths):
    #             overlaps_3 = [word for item in overlaps_3 for word in item]
    #
    #         content_words_3 = [word for word in overlaps_3 if word[1] in content_word_pos and len(word) > 0]
    #
    #         if len(content_words_3) > 0:
    #             content_word_overlap_3 = len(content_words_3) / num_sentences
    #
    #             # Calculate lemma overlap for each content POS
    #             nouns_3 = [word for word in content_words_3 if word[1] == 'NOUN']
    #             pron_3 = [word for word in content_words_3 if word[1] == 'PRON']
    #             propn_3 = [word for word in content_words_3 if word[1] == 'PROPN']
    #             verbs_3 = [word for word in content_words_3 if word[1] == 'VERB']
    #             adj_3 = [word for word in content_words_3 if word[1] == 'ADJ']
    #             adv_3 = [word for word in content_words_3 if word[1] == 'ADV']
    #
    #             all_pos = [nouns_3] + [pron_3] + [propn_3] + [verbs_3] + [adj_3] + [adv_3]
    #
    #             for pos in all_pos:
    #                 if len(pos) > 0:
    #                     pos_overlaps_counts_3.append(len(pos))
    #                 else:
    #                     pos_overlaps_counts_3.append(0)
    #
    #         else:
    #             content_word_overlap_3 = 0
    #
    #     else:
    #         content_word_overlap_3 = 0
    #
    #     if len(pos_overlaps_counts_3) > 0:
    #         for pos in pos_overlaps_counts_3:
    #             pos_overlaps_3.append(round(pos / num_sentences, 2))
    #
    #     if not content_word_overlap_2:
    #         content_word_overlap_2 = 0
    #     if not content_word_overlap_3:
    #         content_word_overlap_3 = 0
    #
    #     return round(avg_overlap_2, 2), round(avg_overlap_3, 2),\
    #         round(content_word_overlap_2, 2), round(content_word_overlap_3, 2),\
    #         pos_overlaps_2, pos_overlaps_3

    def lexical_density(self):
        """ Calculate lexical density (number of content words divided by total number of words).
        :return: lexical density of input text
        """
        if self.language in ['en', 'ru', 'de']:
            content_words = self.nouns + self.verbs + self.adjectives + self.adverbs
        else:
            return 'Error: Please enter a valid language.'

        try:
            lex_density = round(len(content_words) / len(self.words), 2)
        except ZeroDivisionError:
            lex_density = 0

        return lex_density

    def pronouns_ratio(self):
        """ :return: ratio of pronouns (number of pronouns divided by total number of words)
        """
        try:
            num_pron = round(len(self.pronouns) / len(self.words) * 100, 2)
        except ZeroDivisionError:
            num_pron = 0

        return num_pron

    def n_pron_ratio(self):
        """ Calculate noun-pronoun ratio in input text.

        :return: noun to pronoun ratio
        """
        try:
            n_pron_ratio = round(len(self.pronouns) / len(self.nouns) * 100, 2)
        except ZeroDivisionError:
            n_pron_ratio = 0

        return n_pron_ratio

    # def num_subclauses(self):
    #     """ Calculate number of subclauses in input text.
    #
    #     :return: number of subclauses
    #     """
    #     deprels = self.conll_df['DEPREL'].values.tolist()
    #     subord_clauses = [rel for rel in deprels if rel.split(':')[0] in ['acl', 'advcl']]
    #
    #     return len(subord_clauses)

    def polysyllabic_word_ratio(self):
        """ 'Polysyllabic' is defined as 3+ syllables for en, 4+ for ru (Oborneva (?))
        :return: polysyllabic word ratio as a percentage
        """
        if self.language == 'en':
            num_polysyllabic_words = [syl_count for syl_count in self.syllables if syl_count >= 3]
        elif self.language == 'ru':
            num_polysyllabic_words = [syl_count for syl_count in self.syllables if syl_count >= 4]
        elif self.language == 'de':
            num_polysyllabic_words = [syl_count for syl_count in self.syllables if syl_count >= 3]  # NEED TO CHECK
        else:
            return 'Error: Please enter a valid language.'

        try:
            polysyllabic_word_ratio = round(len(num_polysyllabic_words)/len(self.words), 2)
        except ZeroDivisionError:
            polysyllabic_word_ratio = 0

        return round(polysyllabic_word_ratio * 100, 2)

    def type_token_ratio_all(self):
        """ Calculate type-token ratio for all words in given text using corrected
            TTR calculation T / sqrt(2*N) to account for text length effects (Lu, 2012).
        :return: type-token ratio (all words)
        """
        all_types = set(self.words)

        try:
            ratio = len(all_types) / math.sqrt(2 * (len(self.words)))
        except ZeroDivisionError:
            ratio = 0

        return round(ratio, 2)

    def type_token_ratio_nouns(self):
        """ Calculate type-token ratio for all nouns in given text using corrected
            TTR calculation T / sqrt(2*N) to account for effects of text length on ratio (Lu, 2012).
        :return: type-token ratio (nouns)
        """
        noun_types = set(self.nouns)
        try:
            ratio = len(noun_types) / math.sqrt(2 * (len(self.nouns)))
        except ZeroDivisionError:
            ratio = 0

        return round(ratio, 2)

    def type_token_ratio_verbs(self):
        """ Calculate type-token ratio for all verbs in given text using corrected
            TTR calculation T / sqrt(2*N) to account for effects of text length on ratio (Lu, 2012).
        :return: type-token ratio (verbs)
        """
        verb_types = set(self.verbs)

        try:
            ratio = len(verb_types) / math.sqrt(2 * (len(self.verbs)))
        except ZeroDivisionError:
            ratio = 0

        return round(ratio, 2)

    def type_token_ratio_adjs(self):
        """ Calculate type-token ratio for all adjectives in given text using corrected
            TTR calculation T / sqrt(2*N) to account for effects of text length on ratio (Lu, 2012).
        :return: type-token ratio (adjectives)
        """
        adjective_types = set(self.adjectives)

        try:
            ratio = len(adjective_types) / math.sqrt(2 * (len(self.adjectives)))
        except ZeroDivisionError:
            ratio = 0

        return round(ratio, 2)

    def type_token_ratio_advs(self):
        """ Calculate type-token ratio for all adverbs in given text using corrected
            TTR calculation T / sqrt(2*N) to account for effects of text length on ratio (Lu, 2012).
        :return: type-token ratio (adverbs)
        """
        adverb_types = set(self.adverbs)

        try:
            ratio = len(adverb_types) / math.sqrt(2 * (len(self.adverbs)))
        except ZeroDivisionError:
            ratio = 0

        return round(ratio, 2)

    def save_results(self, num_gaps=None, named_entities=None, verbose=True, output_path=None):
        """
        Generate a file containing the linguistic complexity measures for a text
        :param num_gaps:
        :param named_entities:
        :param verbose:
        :param output_path:
        :return:
        """

        # Run analysis
        DataAnalyser.get_nouns(self), DataAnalyser.get_pronouns(self), DataAnalyser.get_verbs(self),\
            DataAnalyser.get_adjectives(self), DataAnalyser.get_adverbs(self)
        DataAnalyser.get_num_syllables(self)
        num_words = DataAnalyser.num_words(self)
        num_sentences = DataAnalyser.num_sentences(self)
        if named_entities:
            ne = named_entities
        else:
            ne = '(none)'
        avg_word_len = DataAnalyser.avg_word_len(self)
        avg_sent_len = DataAnalyser.avg_sent_len(self)
        flesch_kincaid_grade_level = DataAnalyser.flesch_kincaid_grade_level(self)
        flesch_reading_ease = DataAnalyser.flesch_reading_ease(self)
        lexical_density = DataAnalyser.lexical_density(self)
        n_pron_ratio = DataAnalyser.n_pron_ratio(self)
        pronouns_ratio = DataAnalyser.pronouns_ratio(self)
        polysyllabic_word_ratio = DataAnalyser.polysyllabic_word_ratio(self)
        type_token_ratio_all = DataAnalyser.type_token_ratio_all(self)
        type_token_ratio_nouns = DataAnalyser.type_token_ratio_nouns(self)
        type_token_ratio_verbs = DataAnalyser.type_token_ratio_verbs(self)
        type_token_ratio_adjs = DataAnalyser.type_token_ratio_adjs(self)
        type_token_ratio_advs = DataAnalyser.type_token_ratio_advs(self)

        # Print analysis to Terminal
        if verbose:
            print('')
            print('Total number of words:      ', num_words)
            print('Total number of sentences:  ', num_sentences)
            print('')
            if num_gaps:
                print('Total number of gaps:       ', num_gaps)
            if ne:
                print('Named entities:             ', ne)
            print('Average word length:        ', avg_word_len)
            print('Average sentence length:    ', avg_sent_len)
            print('')
            print('Flesch-Kincaid grade level: ', flesch_kincaid_grade_level)
            print('Flesch reading ease score:  ', flesch_reading_ease)
            print('')
            print('Lexical density:            ', lexical_density)
            print('Noun-pronoun ratio:         ', n_pron_ratio)
            print('Pronoun ratio:              ', pronouns_ratio)
            print('Polysyllabic words ratio:   ', polysyllabic_word_ratio)
            print('')
            print('TTR (all words):            ', type_token_ratio_all)
            print('TTR (nouns):                ', type_token_ratio_nouns)
            print('TTR (verbs):                ', type_token_ratio_verbs)
            print('TTR (adjectives):           ', type_token_ratio_adjs)
            print('TTR (adverbs):              ', type_token_ratio_advs)

        # save
        if output_path:
            filename = '_'.join(output_path.split('/')[-1].split('_')[0:2])
            with open(output_path, 'w') as outfile:
                outfile.write('-----------------------------------------------------------\n'
                              '\tCOMPLEXITY AND READABILITY REPORT FOR {}\n'
                              '-----------------------------------------------------------\n\n'.format(filename))
                outfile.write('\tGENERAL STATISTICS\n---------------------------\n')
                outfile.write('- Total number of words:\t {}\n'.format(num_words))
                outfile.write('- Total number of sentences: {}\n'.format(num_sentences))
                if num_gaps:
                    outfile.write('- Total number of gaps: {}\n'.format(num_gaps))
                if ne:
                    outfile.write('- Named entities: {}\n'.format(ne))
                outfile.write('- Average word length (in letters):   {}\n'.format(avg_word_len))
                outfile.write('- Average sentence length (in words): {}\n\n'.format(avg_sent_len))

                outfile.write('\tREADABILITY FORMULAS\n---------------------------\n')
                outfile.write('- Flesch-Kincaid grade level: {}\n\n'.format(flesch_kincaid_grade_level))
                outfile.write('How to interpret FKG:\nFKG corresponds to U.S. school grade levels (1st-12th).\n\n')

                # outfile.write('FRE Russian formula (Solovyev et al, 2018) = 208.7 − (2.6 * average sentence length (in words)) − (39.2 * average word length (in syllables)\n')
                outfile.write('- Flesch reading ease score: {}\n\n'.format(flesch_reading_ease))
                # outfile.write('FKG Russian formula (Solovyev et al, 2018) = (0.36 * average sentence length (in words)) + (5.76 * average word length (in syllables)) − 11.97\n')
                outfile.write('How to interpret FRE:\n'
                              'SCORE\t\t\tGRADE LEVEL\t\t\tNOTES\n'
                              '100.00–90.00\t5th grade\t\t\tVery easy to read.\n'
                              '90.0–80.0\t\t6th grade\t\t\tEasy to read.\n'
                              '80.0–70.0\t\t7th grade\t\t\tFairly easy to read.\n'
                              '70.0–60.0\t\t8th & 9th grade\t\tPlain en.\n'
                              '60.0–50.0\t\t10th to 12th grade\tFairly difficult to read.\n'
                              '50.0–30.0\t\tCollege\t\t\t\tDifficult to read.\n'
                              '30.0–10.0\t\tCollege graduate\tVery difficult to read. Best understood by university graduates.\n'
                              '10.0–0.0\t\tProfessional\t\tExtremely difficult to read. Best understood by university graduates.\n\n')

                outfile.write('\tTYPE-TOKEN RATIOS\n---------------------------\n')
                # outfile.write('Type-Token Ratio (TTR) = T / sqrt(2*N) (Lu, 2012)\n')
                outfile.write('- TTR (all words):\t{}\n'.format(type_token_ratio_all))
                outfile.write('- TTR (nouns):\t\t{}\n'.format(type_token_ratio_nouns))
                outfile.write('- TTR (verbs):\t\t{}\n'.format(type_token_ratio_verbs))
                outfile.write('- TTR (adjectives):\t{}\n'.format(type_token_ratio_adjs))
                outfile.write('- TTR (adverbs):\t{}\n\n'.format(type_token_ratio_advs))

                outfile.write('\tOTHER STATISTICS\n---------------------------\n')
                outfile.write('- Lexical density:\t\t\t{}\n'.format(lexical_density))
                outfile.write('- Noun-pronoun ratio:\t\t{}\n'.format(n_pron_ratio))
                outfile.write('- Pronoun ratio:\t\t\t{}\n'.format(pronouns_ratio))
                outfile.write('- Polysyllabic words ratio:\t{}'.format(polysyllabic_word_ratio))
