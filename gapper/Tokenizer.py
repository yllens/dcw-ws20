import stanza
import subprocess


class Tokenizer:
    def __init__(self, file_path, token_file, language):
        self.language = language          # 2-character language tag (e.g., 'ru', 'en', 'de')
        self.path = file_path             # Paths to input file
        self.token_file = token_file      # Path to file in which to save tokens for POS tagging
        self.sentences, self.tokenized_sentences, self.tokens, self.tags = [], [], [], []

        # Stanza NLP pipeline
        self.nlp = stanza.Pipeline(lang=language,                    # Stanza NLP pipeline
                                   processors='tokenize, pos',
                                   tokenize_no_ssplit=False)
        self.doc = None                                           # Stanza-processed Document object

    def preprocess(self):
        Tokenizer.process_text(self)
        Tokenizer.get_sentences(self)
        Tokenizer.get_tokens(self)
        Tokenizer.write_tokens(self)
        Tokenizer.get_pos_tags(self)

    def process_text(self):
        """

        :return:
        """
        try:
            # Read input file
            raw_text = ' '.join([line.strip('\n') for line in open(self.path, 'r').readlines()])

            # Extract Stanza-processed Document object for input file
            self.doc = self.nlp(raw_text)

        except FileNotFoundError:
            return 'Error: File does not exist at {}'.format(self.path)

    def get_sentences(self):
        """ Extract sentences from the Stanza Document object generated for the input text file.
        Generates list of lists of format [ [sentence1], [sentence2], ...].
        """
        # Get list of full sentences
        self.sentences.append([sent.text.strip(' ') for sent in self.doc.sentences])
        self.sentences = self.sentences[0]

        # Get list of sentences split by token (excluding punctuation)
        for sentence in self.doc.sentences:
            self.tokenized_sentences.append([token.text for token in sentence.tokens
                                             if token.text not in '.,!?)»(«-–":'])

    def get_tokens(self):
        """ Extract tokens from the Stanza Document object generated for the input text file(s).
        Generates list of lists of format
            [ [[ (sent1_word1, doc_sent1_pos1), (sent1_word2, sent1_pos2), ...],
              [ (doc1_sent2_word1, doc1_sent1_pos1), (doc1_sent2_word2, doc1_sent2_pos2), ...], ...],
            ...]
        """
        # Exclude first and last sentence
        for sentence in self.doc.sentences[1:-1]:   # [1:-1] for Gapper
            self.tokens += ([word.text for word in sentence.words])

    def write_tokens(self):
        """

        :return:
        """
        try:
            with open(self.token_file, 'w', encoding='utf-8') as infile:
                for token in self.tokens:
                    infile.write(token + '\n')
        except FileNotFoundError:
            return 'Error: File does not exist at {}'.format(self.token_file)

    def get_pos_tags(self):
        """

        :return:
        """
        if self.language == 'ru':
            language = 'russian'
        elif self.language == 'en':
            language = 'english-bnc'
        elif self.language == 'de':
            language = 'german'
        else:
            return 'Error: soz no work'
        tagger = '/Users/sne/TreeTagger/bin/tree-tagger'
        param_file = '/Users/sne/TreeTagger/lib/{}.par'.format(language)

        tagged_output = subprocess.run([r'{} {} {} -lemma -token'.format(tagger, param_file, self.token_file)],
                                       encoding='utf-8',
                                       shell=True,
                                       capture_output=True)

        self.tags = [item.split('\t') for item in tagged_output.stdout.splitlines()]
