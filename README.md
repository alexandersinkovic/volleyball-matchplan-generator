# volleyball-matchplan-generator
Simple backtracking algorithm that generates a match plan for volleyball tournaments.

# Requirements
Every attending team is matched with a random teammate in every match.
The two teams are matched with 2 random enemies that neither of them have played against in this tournament.
Every round consists of X matches that are played simultaneously on X different fields.

# Fine Tuning
calculate_matches.py contains global static parameters that can be used to fine tune the algo to different settings, e. g. number of teams attending and number of rounds that a team plays
