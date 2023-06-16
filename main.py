import random
import re
import openai

openai.api_key = "mysecretkey"  # api key


# define the MarkovChain class
class MarkovChain:
    def __init__(self, order=5):  # default order if no order is specified
        # initialize the MarkovChain object with a specified order
        self.order = order
        # initialize an empty dictionary to hold the Markov chain model
        self.chain = {}

    def add_text(self, text):
        # split the input text into words
        words = re.findall(r'\b\w+\b', text)  # raw string matches one or more consecutive word characters
        # iterate over each n-gram in the text and add it to the Markov chain model
        for i in range(len(words) - self.order):
            # create an n-gram key for the Markov chain
            key = tuple(words[i:i + self.order])
            # add the next word in the text to the list of words that follow the n-gram (add the tuple to a key)
            if key in self.chain:
                self.chain[key].append(words[i + self.order])
            else:
                self.chain[key] = [words[i + self.order]]

    def generate_sentence(self, length=10):  # default lenght if no length is specififed
        # choose a random starting n-gram from the Markov chain model
        start = random.choice(list(self.chain.keys()))
        # list to hold sentences
        sentence = list(start)
        # generate words until the desired sentence length is reached
        while len(sentence) < length:
            # get the current n-gram by taking the last n words of the sentence
            key = tuple(sentence[-self.order:])
            # if there is no transition possible end the sentence
            if key not in self.chain:
                break
            # choose a random word to follow the current n-gram and add it to the sentence
            word = random.choice(self.chain[key])
            sentence.append(word)
        # join the words in the sentence into a single string
        sentence_str = ' '.join(sentence)
        # use a language model to generate a completion for the sentence
        completion = openai.Completion.create(
            engine="davinci",
            prompt=sentence_str,
            max_tokens=50,
            n=1,
            stop=None,
        ).choices[0].text
        # split the completion into sentences and capitalize the first letter of each sentence I spent a lot of time
        # trying to make this work but I think the gpt model isn't working correctly.
        sentences = completion.split('.')
        sentences = [s.capitalize().strip() + '.' for s in sentences if s.strip() != '']
        # join the sentences into a single string
        sentence_str = ' '.join(sentences)
        return sentence_str


# prompt the user to enter text
text = input("Enter text to generate random sentences to be completed by the GPT language model: ")

# prompt the user to enter order to be used
mcorder = int(input("Enter the Markov chain order 1-10: "))
if mcorder < 1 or mcorder > 10:
    print("Invalid order. Using default order of 5.")
    mcorder = 5

# create a MarkovChain object with the specified order
mc = MarkovChain(order=mcorder)

# add user input text to the MarkovChain
mc.add_text(text)

# prompt the user to enter the desired sentence length and number of sentences
sent_length = int(input("Enter the max sentence length (number of words): "))
num_sentences = int(input("Enter the desired max of sentences: "))

# generate random sentences
generated_sentences = []
while len(generated_sentences) < num_sentences:
    sentence = mc.generate_sentence(length=sent_length)
    if sentence is not None:
        generated_sentences.append(sentence)

# print the generated sentences
for sentence in generated_sentences:
    print(sentence)
