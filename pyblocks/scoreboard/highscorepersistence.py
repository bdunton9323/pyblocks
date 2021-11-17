import os


# The high score file must be in descending order
def _parse_file(filename, num_scores):
    scores = []
    with open(filename, "r") as file:
        for line in [line.rstrip("\n") for line in file]:
            tokens = line.split(",")
            if len(tokens) != 2:
                raise Exception("High score file is corrupt")
            scores.append((tokens[0], tokens[1]))
    # If the file contained too few scores, add empty entries
    scores.extend([("...", 0) for x in range(num_scores - len(scores))])
    return scores


class HighScoreReader(object):
    DEFAULT_ENTRIES = [
        ("MISHA", "1000"),
        ("LITTLE BEAR", "900"),
        ("BROWN BEAR", "800"),
        ("HISSY", "700"),
        ("DOGGY", "600"),
        ("PIGGY", "500"),
        ("COW", "10"),
        ("LITTLE DUCKLING", "10"),
        ("BIG DUCKLING", "5"),
        ("IGUANA", "0")
    ]

    # filename - the high score file
    # num_scores - the number of scores to limit by (could be different than the
    #              number of lines in the file)
    def __init__(self, filename, num_scores):
        self.filename = filename
        self.init_score_file()
        self.num_scores = num_scores

    # create the default file if one does not exist
    def init_score_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w+") as file:
                for entry in HighScoreReader.DEFAULT_ENTRIES:
                    file.write(entry[0] + "," + entry[1] + "\n")

    # Return a list of tuples sorted from highest score to lowest score
    def read_scores(self):
        self.scores = _parse_file(self.filename, self.num_scores)
        return self.scores[:self.num_scores]

    # Determines whether 'score' is higher than the lowest score in the list
    def is_high_score(self, score):
        scores = self.read_scores()
        return score > int(scores[-1][1])


# Writes a score to the file in the proper position
class HighScoreWriter(object):

    # num_scores - the number of scores to store in the score file
    def __init__(self, filename, num_scores):
        self.filename = filename
        self.num_scores = num_scores

    # write the score. The scores must be stored in descending order
    # score - int - the final score for the game
    # name - string - the person who got the score
    def write_score(self, name, score):
        scores = _parse_file(self.filename, self.num_scores)
        new_entry = name + ',' + str(score) + '\n'
        with open(self.filename, 'w') as file:
            written = False
            for s in scores[:-1]:
                if score > int(s[1]) and not written:
                    written = True
                    file.write(new_entry)
                file.write(s[0] + ',' + s[1] + '\n')
            # last place
            if not written:
                file.write(new_entry)
