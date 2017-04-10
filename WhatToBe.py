"""Script takes as input text and outputs predictions of conjugations of the verb 'to be'."""
import sys
import nltk

def predict_conjugation(sentence):
    """This function takes as an input the sentence and returns the predicted conjugation."""
    # Judge if future, perfect or continuous tenses :
    # Check word just before the blank.
    word_list = nltk.tokenize.word_tokenize(sentence)
    # cases where sentence contains more than one blank
    blank_position = word_list.index('newword')
    earlier_word = word_list[blank_position-1]
    if earlier_word == 'have' or earlier_word == 'has':
        # Perfect tenses
        return 'been'

    # Change this to all conjugations of 'to be'
    elif earlier_word == 'be' or earlier_word == 'been':
        # Continuous form of any tense
        return 'being'

    elif earlier_word == 'will' or earlier_word == 'would':
        # Future tense
        return 'be'

    # Else parse and figure out present or past tense.
    return "is"

# Read input
N = int(sys.stdin.readline().strip())

# Check if 1 <= N <= 20
if N < 1 or N > 20:
    sys.exit()

text = sys.stdin.readline().strip()
text = text.replace('----', 'newword')
list_of_sentences = nltk.tokenize.sent_tokenize(text)
for line in list_of_sentences:
    if line.find('newword') != -1:
        print predict_conjugation(line)
