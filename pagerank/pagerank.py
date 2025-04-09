import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    keys = list(reversed(corpus))
    links = corpus[page]
    link_probability = {}
    for key in keys:
        if key in links:
            link_probability[key] = (0.85/len(links)) + (0.15/len(keys))
        else:
            link_probability[key] = (0.15/len(keys))
    return link_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = list(reversed(corpus))
    sample_count = {}
    for key in keys:
        sample_count[key] = 0
    choice = random.choice(keys)
    sample_count[choice] += 1
    prob_dist = transition_model(corpus, choice, damping_factor)
    for i in range(n - 1):
        choice = random.choices(keys, prob_dist.values())[0]
        sample_count[choice] += 1
        prob_dist = transition_model(corpus, choice, damping_factor)
    for sample in sample_count:
        sample_count[sample] = sample_count[sample]/n
    return sample_count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = list(corpus.keys())
    prob_dist = {}
    length_corpus = {}
    # initialize probabilites and lengths
    for key in keys:
        prob_dist[key] = 1/len(keys)
        length_val = len(corpus[key])
        if length_val:
            length_corpus[key] = length_val
        else:
            length_corpus[key] = len(keys)
    all_keys = False
    while (not all_keys):
        temp_dist = {}
        for key in keys:
            sum_corpus = 0
            for link in keys:
                if key in corpus[link] or not corpus[link]:
                    sum_corpus += prob_dist[link]/length_corpus[link]
            temp_dist[key] = ((1 - damping_factor)/len(keys)) + (damping_factor * sum_corpus)
        
        all_keys = True
        for key in keys:
            if abs(temp_dist[key] - prob_dist[key]) > 0.001:
                all_keys = False
                break
        prob_dist = temp_dist.copy()
    return prob_dist
    


if __name__ == "__main__":
    main()
