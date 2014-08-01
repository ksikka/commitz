#!/usr/bin/env python

from pymarkovchain import MarkovChain
from gitgetter import git_log

def markov(messages):
    # Create an instance of the markov chain. By default, it uses MarkovChain.py's location to
    # store and load its database files to. You probably want to give it another location, like so:
    mc = MarkovChain("./markov")

    # To generate the markov chain's language model, in case it's not present
    # mc.generateDatabase("\n".join(messages))

    # To let the markov chain generate some text, execute
    for i in xrange(100):
        print mc.generateString()

if __name__ == "__main__":
    commits = git_log()
    commits = [c for c in commits if not c['subject'].startswith('Merge branch')]
    print set([c['name'] for c in commits])
    #markov([c['subject'] for c in commits if not c['subject'].startswith('Merge branch') ])
    markov([])
