#
# Created by maks5507 (me@maksimeremeev.com)
#


class Node:
    def __init__(self, token, lemmatized, pos, xpos, feats, dep_rel, anc=-1):
        self.token = token
        self.lemma = lemmatized
        self.pos = pos
        self.xpos = xpos
        self.feats = feats
        self.dep_rel = dep_rel
        self.anc = anc
