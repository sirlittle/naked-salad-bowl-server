import random
import uuid
import functools
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class WordCard:
    words: List[str]


@dataclass
class Guess:
    user: str
    words: WordCard


class NakedSaladBowl:
    def __init__(self, unguessed_cards: List[str], guessed_cards: List[str], current_turn_guesses: List[Guess]):
        self.unguessed_cards = unguessed_cards
        self.guessed_cards = guessed_cards
        self.current_turn_guesses = current_turn_guesses

    def create_card(self, word_card):
        self.unguessed_cards.append(word_card)

    @property
    def words(self):
        pass

    def reset(self):
        self.unguessed_cards.extend(self.guessed_cards)
        self.guessed_cards = []

    def to_dict(self):
        return {
            'unguessed_cards': self.unguessed_cards,
            'guessed_cards': self.guessed_cards,
            'current_turn_guesses': self.current_turn_guesses
        }


class Game:
    def __init__(
            self, 
            bowl: NakedSaladBowl,
            room_name: str, 
            room_id: str,
            admin_name: str,
            room_pw: str, 
            teams: Dict[str, list],  # team name -> list[team_members] 
            scores: Dict[str, int],  # team_name -> score
            round_num: int,
            time_left: float,
            last_correct: WordCard,
    ):
        self.bowl = bowl
        self.room_name = room_name
        self.teams = teams
        self.admin_name = admin_name
        self.scores = scores
        self.round_num = round_num
        self.time_left = self.time_left
        self.last_correct = last_correct
        self._room_pw = room_pw

    def start(self):
        self.current_team = random.randint(0, len(self.teams)-1)
        self.next_round()

    def next_round(self):
        self.round += 1
        self.bowl.reset()

    def next_turn(self):
        self.current_team = (self.current_team + 1) % len(self.teams)

    def finish(self):
        pass

    def check_word(self, word_card):
        return self.bowl.has_card(word_card)

    def to_dict(self):
        return {
            'bowl': self.bowl.to_dict(),
            'room_name': self.room_name,
            'room_id': self.room_id,
            'teams': self.teams,
            'scores': self.scores,
            'round_num': self.round_num,
            'time_left': self.time_left,
            'last_correct': self.last_correct
        }
    
    def to_db_dict(self):
        db_dict = self.to_dict()
        db_dict['password'] = self.password
        return db_dict
    
    @staticmethod
    def from_dict(self, dct):
        pass
