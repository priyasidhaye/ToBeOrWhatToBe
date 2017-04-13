"""Script takes as input text and outputs predictions of conjugations of the verb 'to be'."""
from itertools import chain
import sys
import nltk
from nltk.parse.stanford import StanfordDependencyParser

def predict_tense(sentence, context):
    """This function returns the most likely tense based on the sentence and its context.
    Checks current, previous and next sentences for conjugated verbs.
    Default is past tense"""
    past_tense_tags = ['VBN', 'VBD']
    present_tense_tags = ['VBP', 'VBZ', 'VBG']
    past_tense_count = 0
    present_tense_count = 0
    combined_text = ''.join(context)
    for (word, tag) in nltk.pos_tag(nltk.word_tokenize(sentence + combined_text)):
        if tag in past_tense_tags and word != 'newword':
            print word, "past"
            past_tense_count += 1
        elif tag in present_tense_tags and word != 'newword':
            print word, "present"
            present_tense_count += 1
    prediction = "Present" if present_tense_count > past_tense_count else "Past"
    return prediction

def find_related_node(dependency_graph, node_address, relation):
    """This method reverse searched the dependency graph
    that is related to the target node to the input node address by passed relation"""
    for node_data in dependency_graph.nodes.itervalues():
        deps = node_data['deps']
        for rel, related_node in deps.iteritems():
            if relation == rel and related_node[0] == node_address:
                return node_data['address']
    return -1

def predict_subject_info(sentence, address):
    """This function predicts the most likely information about the subject."""
    dependency_lookup_failed = False
    mult = ""
    person = ""
    # Replace 'newword' by 'is'
    sentence.replace('newword', 'is')

    # Dependency parse of the sentence
    path_to_jar = 'C:\\Python27\\stanford-parser-full-2016-10-31\\stanford-parser.jar'
    path_to_models = 'C:\\Python27\\stanford-parser-full-2016-10-31\\' + \
                            'stanford-parser-3.7.0-models.jar'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, \
                            path_to_models_jar=path_to_models)
    dependencies = dependency_parser.raw_parse(sentence).next()

    # Find subject
    tobe_address = dependencies.get_by_address(address)
    deps = tobe_address['deps']
    # Check if 'to be' is the main verb of the sentence
    if 'nsubj' in deps.keys() or 'nsubjpass' in deps.keys():
        # 'to be is the main verb of the sentence. Find subject verb
        # Find the subject node
        pass
    else:
        # 'to be' is the auxillary verb of the sentence, find main verb and then subject verb
        relation = tobe_address['rel']
        related_node = find_related_node(dependencies, address, relation)
        if related_node != -1:
            deps = dependencies.get_by_address(related_node)['deps']
        else:
            dependency_lookup_failed = True
    if not dependency_lookup_failed:
        for key, addr in deps.iteritems():
            if key.find('nsubj') != -1:
                subject_node_address = addr[0]
        subject_node = dependencies.get_by_address(subject_node_address)

    # POS tag sentence to get noun/pronoun
    pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence))
    (subject_node_word, subject_node_tag) = pos_tags[subject_node_address-1]
    subject_node_word = subject_node_word.lower()
    # Case : Noun
    if subject_node_tag == 'NN' or subject_node_tag == 'NNP':
        mult = 'S'
        person = '3'
    elif subject_node_tag == 'NNS' or subject_node_tag == 'NNPS':
        mult = 'P'
        person = '3'

    # Case : Pronoun
    elif subject_node_tag == 'PRP':
        if subject_node_word in ['he', 'she', 'it']:
            mult = 'S'
            person = '3'
        elif subject_node_word in ['you']:
            mult = 'S'
            person = '2'
        elif subject_node_word in ['i']:
            mult = 'S'
            person = '1'
        elif subject_node_word in ['we']:
            mult = 'P'
            person = '1'
        elif subject_node_word in ['they']:
            mult = 'P'
            person = '3'

    # Check if subject has a conjunction relation
    if 'conj' in subject_node['deps'].keys():
        mult = 'P'

    # TODO: Add default case where above doesn't work
    # Return result
    return person + mult

def lookup_conjugation(subject_info, tense_info):
    """This function looks up the conjugation and returns predicted conjugation."""
    conjugations = {('1S', 'present'): 'am', ('1P', 'present'): 'are',
                    ('2S', 'present'): 'are', ('2P', 'present'): 'are',
                    ('3S', 'present'): 'is', ('3P', 'present'): 'are',
                    ('1S', 'past'): 'was', ('1P', 'past'): 'were',
                    ('2S', 'past'): 'were', ('2P', 'past'): 'were',
                    ('3S', 'past'): 'was', ('3P', 'past'): 'were'}
    try:
        result = conjugations[(subject_info, tense_info)]
    except KeyError:
        return ""
    return result

def predict_conjugation(sentence, context):
    """This function takes as an input the sentence and returns the predicted conjugation."""
    # Judge if future, perfect or continuous tenses :
    # Check word just before the blank.
    word_list = nltk.tokenize.word_tokenize(sentence)
    # cases where sentence contains more than one blank
    blank_positions = [index for index, word in enumerate(word_list) if word == 'newword']
    result_conjugations = list()
    for blank_position in blank_positions:
        result = ""
        earlier_word = "" if blank_position == 0 else word_list[blank_position-1]

        # Initialize lemmatizer
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

        # Initialize preceeding modifier words for conditional mood,
        # future tense and infinitive form.
        infinitive_preceeding_words = ['to', 'will', 'would', 'may', 'might', 'can', 'could']
        determiners_singular = ['this', 'that', 'little', 'either', 'enough',
                                'any', 'such', 'what', 'another', 'other']
        determiners_plural = ['these', 'those', 'many', 'few', 'some', 'both', 'all']

        if earlier_word == 'have' or earlier_word == 'has':
            # Perfect tenses
            result = 'been'

        elif lemmatizer.lemmatize(earlier_word, 'v') == 'be':
            # Continuous form of any tense
            result = 'being'

        elif earlier_word in infinitive_preceeding_words:
            # Future tense, conditional mood or infinitive
            result = 'be'

        elif earlier_word in determiners_singular:
            tense = predict_tense(sentence, context)
            result = lookup_conjugation('3S', tense)

        elif earlier_word in determiners_plural:
            tense = predict_tense(sentence, context)
            result = lookup_conjugation('3P', tense)

        else:
            # Else parse and figure out present or past tense.
            tense = predict_tense(sentence, context)
            subject = predict_subject_info(sentence, blank_position + 1)
            result = lookup_conjugation(subject, tense)
        result_conjugations.append(result)
    return result_conjugations


# Read input
N = int(sys.stdin.readline().strip())

# Check if 1 <= N <= 20
if N < 1 or N > 20:
    sys.exit()

text = sys.stdin.readline().strip().lower()
text = text.replace('----', 'newword')
list_of_sentences = nltk.tokenize.sent_tokenize(text)
previous_sentences = chain([''], list_of_sentences[:-1])
next_sentences = chain(list_of_sentences[1:], [''])
context_sentences = zip(previous_sentences, next_sentences)
result_list = list()
for i in range(len(list_of_sentences)):
    if list_of_sentences[i].find('newword') != -1:
        result_list = chain(result_list, predict_conjugation(list_of_sentences[i], context_sentences[i]))
print "\n".join(result_list)
