import random
import uuid
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class WordCard:
  words: List[str]


@dataclass
class Guess:
  user: str
  words: WordCard


class Game:
  def __init__(
      self, 
      bowl: NakedSaladBowl,
      room_name: str, 
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

  @staticmethod
  def create_game(admin_name: str, room_name: str, room_pw: str):
    pass

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


class Team:
  def __init__(self, name):
    self.name = name
    self.players = {}

  def add_player(self, player):
    self.players[player.id] = player

  def remove_player(self, player):
    del self.players[player.id]


class Player:
  def __init__(self, name):
    self.name = name
    self.id = uuid.uuid4()

  def join_game(self, game):
    self.current_game = game

  def make_guess(self, word_card):
    self.current_game.check(word_card)


class NakedSaladBowl:
  def __init__(self, unguessed_cards: List[str], guessed_cards: List[str], current_turn_guesses: List[Guess]):
    self.unguessed_cards = unguessed_cards
    self.guessed_cards = guessed_cards
    self.current_turn_guesses = current_turn_guesses

  def create_card(self, word_card):
    self.unguessed_cards.append(word_card)

  def create_cards(self, word_cards):
    for card in word_cards:
      self.create_card(card)

  @property
  def words(self):
    pass

  def reset(self):
    self.unguessed_cards.extend(self.guessed_cards)
    self.guessed_cards = []
