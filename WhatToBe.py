"""Script takes as input text and outputs predictions of conjugations of the verb 'to be'."""
from itertools import chain
import sys
import nltk


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

def predict_subject_info(sentence):
    """This function predicts the most likely information about the subject."""
    # if there is only one verb in the sentence
    # multiple verbs, dependency parse needed
    return ""

def predict_conjugation(sentence, context):
    """This function takes as an input the sentence and returns the predicted conjugation."""
    # Judge if future, perfect or continuous tenses :
    # Check word just before the blank.
    word_list = nltk.tokenize.word_tokenize(sentence)
    # cases where sentence contains more than one blank
    blank_position = word_list.index('newword')
    earlier_word = word_list[blank_position-1]

    # Initialize lemmatizer
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    # Initialize preceeding modifier words for conditional mood, future tense and infinitive form.
    infinitive_preceeding_words = ['to', 'will', 'would', 'may', 'might', 'can', 'could']

    if earlier_word == 'have' or earlier_word == 'has':
        # Perfect tenses
        return 'been'

    elif lemmatizer.lemmatize(earlier_word, 'v') == 'be':
        # Continuous form of any tense
        return 'being'

    elif earlier_word in infinitive_preceeding_words:
        # Future tense, conditional mood or infinitive
        return 'be'

    else:
        # Else parse and figure out present or past tense.
        tense = predict_tense(sentence, context)
        subject = predict_subject_info(sentence)
        print tense
        return "is"

# Read input
N = int(sys.stdin.readline().strip())

# Check if 1 <= N <= 20
if N < 1 or N > 20:
    sys.exit()

text = sys.stdin.readline().strip()
text = text.replace('----', 'newword')
list_of_sentences = nltk.tokenize.sent_tokenize(text)
previous_sentences = chain([''], list_of_sentences[:-1])
next_sentences = chain(list_of_sentences[1:], [''])
context_sentences = zip(previous_sentences, next_sentences)
for i in range(len(list_of_sentences)):
    if list_of_sentences[i].find('newword') != -1:
        print predict_conjugation(list_of_sentences[i], context_sentences[i])
        break
