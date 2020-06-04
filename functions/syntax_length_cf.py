#
# Created by maks5507 (me@maksimeremeev.com)
#


class SyntaxLengthComplexityFunction:
    def complexity(self, tokens):
        complexities = []
        for token in tokens:
            complexities += [0]
            for i, pt in enumerate(token):
                if pt.pos == 'PUNCT' or pt.anc == -1:
                    continue
                complexities[-1] = max(complexities[-1], abs(pt.anc - i))
        return complexities
