class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player1_score = 0
        self.player2_name = player2_name
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def scores_are_tied(self):
        return self.player1_score == self.player2_score

    def four_points_are_reached(self):
        return self.player1_score >= 4 or self.player2_score >= 4

    def three_points_are_reached(self):
        return self.player1_score >= 3 or self.player2_score >= 3

    def non_tied_score_after_four_points(self):
        score_difference = self.player1_score - self.player2_score
        if score_difference == 1:
            return "Advantage player1"
        elif score_difference == -1:
            return "Advantage player2"
        elif score_difference >= 2:
            return "Win for player1"
        elif score_difference <= -2:
            return "Win for player2"
        # All possible cases are covered above; this method is only called when scores are not tied.
    
    def score_as_tennis_call(self, score):
        tennis_score_names = ["Love", "Fifteen", "Thirty", "Forty"]
        if score < 4:
            return tennis_score_names[score]
        else:
            return "Deuce"

    def get_score(self):
        if self.scores_are_tied():
            if self.three_points_are_reached():
                return "Deuce"
            else:
                return self.score_as_tennis_call(self.player1_score) + "-All"
        elif self.four_points_are_reached():
            return self.non_tied_score_after_four_points()
        else:
            return self.score_as_tennis_call(self.player1_score) + "-" + self.score_as_tennis_call(self.player2_score)