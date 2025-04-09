import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP 
NP -> N | Adj NP | Det NP | N NP | P NP | Adj NP | Conj NP | N VP | NP Adv 
VP -> V | P VP | V NP | Adv VP | V VP | Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()


        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lower_case_sentence = sentence.lower()
    tokenized_sentence = nltk.NLTKWordTokenizer().tokenize(lower_case_sentence)
    def one_alphabetic_character(word):
        for character in word:
            if character.isalpha():
                return True
        return False
    def remove_punctuation(word):
        if not word[len(word) - 1].isalpha():
            return word[0:len(word)-1]
        return word
    only_alpha_numeric_tokens = [remove_punctuation(elem) for elem in tokenized_sentence if one_alphabetic_character(elem)]
    return only_alpha_numeric_tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result = []
    for s in tree.subtrees(lambda t: t.label() == "NP"):
        temp = [x for x in s.subtrees(lambda y: y.label() == "NP")]
        if len(temp) > 0:
            temp = temp[1:]
        if len(temp) == 0:
            result.append(s)
    return result


if __name__ == "__main__":
    main()
