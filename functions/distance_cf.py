#
# Created by maks5507 (me@maksimeremeev.com)
#


class DistanceComplexityFunction:
    def complexity(self, tokens):
        total = len(tokens)
        complexities = []
        last_position = {}
        for i in range(total):
            if tokens[i] not in last_position:
                last_position[tokens[i]] = i
                complexities.append(-1)
            else:
                complexities.append(i - last_position[tokens[i]])
                last_position[tokens[i]] = i
        for i in range(total):
            if complexities[i] == -1:
                complexities[i] = total - last_position[tokens[i]] + i
        return [-score for score in complexities]
