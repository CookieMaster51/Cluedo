import json
import random
import typing

# def power():
#     with open("connections.json", "r") as connections_file:
#         connections_file = json.load(connections_file)
#         for room in connections_file.keys():
#             connections = connections_file[room]
#             weight = sum(connections.values())
#             print(room, weight)s

# power()


class Cards:
    num_to_card = {
        0: "SCARLETT",
        1: "MUSTARD",
        2: "GREEN",
        3: "PEACOCK",
        4: "PLUM",
        5: "ORCHID",
        6: "DAGGER",
        7: "ROPE",
        8: "REVOLVER",
        9: "LEAD_PIPE",
        10: "CANDLESTICK",
        11: "WRENCH",
        12: "KITCHEN",
        13: "BALLROOM",
        14: "CONSERVATORY",
        15: "BILLIARD_ROOM",
        16: "LIBRARY",
        17: "STUDY",
        18: "HALL",
        19: "LOUNGE",
        20: "DINNING_ROOM",
    }
    card_to_num = {
        "SCARLETT": 0,
        "MUSTARD": 1,
        "GREEN": 2,
        "PEACOCK": 3,
        "PLUM": 4,
        "ORCHID": 5,
        "DAGGER": 6,
        "ROPE": 7,
        "REVOLVER": 8,
        "LEAD_PIPE": 9,
        "CANDLESTICK": 10,
        "WRENCH": 11,
        "KITCHEN": 12,
        "BALLROOM": 13,
        "CONSERVATORY": 14,
        "BILLIARD_ROOM": 15,
        "LIBRARY": 16,
        "STUDY": 17,
        "HALL": 18,
        "LOUNGE": 19,
        "DINNING_ROOM": 20
    }


class Util:
    @staticmethod
    def roll_dice():
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return d1 + d2

    @staticmethod
    def get_poss_rooms(curr_room: int, roll: int):
        with open("app\\connections.json", "r", encoding="utf-8") as connections:
            connections = json.load(connections)
        can_get_to = []
        room_conn_dict = connections[Cards.num_to_card[curr_room].lower()]
        for room in room_conn_dict:
            distance = room_conn_dict[room]
            if distance <= roll:
                can_get_to.append(Cards.card_to_num[room.upper()])

        return can_get_to


class Question:
    def __init__(self, person, weapons, room, player) -> None:
        self.question = [person, weapons, room]
        self.player = player

    def validate(self, accusation: bool):
        accusation = not accusation
        return True
        # FIX THIS
        # if not self.question[0] >= 0 and not self.question[0] <= 6:
        #     return False
        # elif not self.question[1] >= 7 and not self.question[1] <= 11:
        #     return False
        # elif not self.question[2] >= 12 and not self.question[2] <= 20:
        #     return False
        # if not accusation:
        #     if not self.player.pos == self.question[2]:
        #         return False
        # else:
        #     return True


class Player:
    def __init__(self, name: str, character: int) -> None:
        self.hand = []
        self.has_turn = True
        self.name = name
        self.pos = character
        self.roll_bank = 0
        self.banked = False

    @typing.final
    def register_card(self, card):
        self.hand.append(card)

    def give_question(self, question: Question, showing, showed: bool):
        if showed:
            print(f"With {question.question}, {showing.name} did show")
        else:
            print(f"With {question.question}, {showing.name} did not show")

    def give_answer(self, card, came_from):
        if card and came_from:
            print(f"{came_from.name} showed {card}")
        else:
            print("No one showed anything")

    def choose_which_to_show(self, matches):
        return random.choice(matches)

    def turn(self):
        roll = Util.roll_dice()
        print(f"You rolled a {roll}, giving you a distance of {roll + self.roll_bank}")

        possible = Util.get_poss_rooms(self.pos, roll + self.roll_bank)
        print(possible)

        ans = int(input("which index to move to, -1 for bank  "))
        if ans == -1:
            self.roll_bank += roll
            self.banked = True
        else:
            self.pos = possible[ans]
            self.roll_bank = 0

        if not self.banked:
            return self.get_question()
        else:
            self.banked = False
            return None

    @typing.final
    def get_question(self):
        person, weapon, room = self.get_question_from_player()
        question = Question(person, weapon, room, self)
        if question.validate(False):
            return question
        else:
            return None

    def get_question_from_player(self) -> tuple[int, int, int]:
        person = int(input("Who to suggest"))
        weapon = int(input("what to suggest"))
        room = int(input("where to suggest"))
        return (person, weapon, room)

    @typing.final
    def has_card(self, question: Question):
        matches = []
        for possible in question.question:
            if possible in self.hand:
                matches.append(possible)

        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        else:
            return self.choose_which_to_show(matches)

    def accuse(self) -> Question | None:
        yesno = input("would you like to accuse")

        if yesno.lower() == "y":
            person = int(input("Who to accuse"))
            weapon = int(input("what to accuse"))
            room = int(input("where to accuse"))
            question = Question(person, weapon, room, self)

            if question.validate(True):
                return question
            else:
                return None
        else:
            return None


class Board:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.hidden = []

    def choose_and_send(self) -> None:
        deck = [i for i in range(0, 21)]

        hidden_char = random.randint(0, 5)
        deck.remove(hidden_char)

        hidden_weapon = random.randint(6, 11)
        deck.remove(hidden_weapon)

        hidden_room = random.randint(12, 20)
        deck.remove(hidden_room)

        self.hidden = [hidden_char, hidden_weapon, hidden_room]

        current = random.randint(
            0, len(self.players) - 1
        )  # random start to make it fair
        while len(deck) != 0:
            to_give = random.choice(deck)
            deck.remove(to_give)
            self.players[current].register_card(to_give)

            current += 1
            if current == len(self.players):
                current = 0

    def broadcast(self, question: Question, showing: Player, showed: bool):
        for player in self.players:
            player.give_question(question, showing, showed)

    def player_question(self, question, current_player, current):
        if question:
            offset = 1
            back_at_start = False
            showed = False

            while not back_at_start and not showed:
                next_player = self.players[(current + offset) % len(self.players)]
                showing = next_player.has_card(question)
                if showing:
                    current_player.give_answer(showing, next_player)
                    self.broadcast(question, next_player, True)
                    showed = True
                else:
                    self.broadcast(question, next_player, False)
                    offset += 1
                    if offset % len(self.players) == 0:
                        back_at_start = True
                        current_player.give_answer(None, None)

    def start_game(self):
        guessed = False
        current = 0
        while not guessed:
            current_player = self.players[current]
            if current_player.has_turn:
                question = current_player.turn()
                self.player_question(question, current_player, current)

                accusation = current_player.accuse()
                if accusation:
                    print(accusation.question)
                    if accusation.question == self.hidden:
                        guessed = True
                        winner = current_player
                    else:
                        current_player.has_turn = False

            current = (current + 1) % len(self.players)
        print(winner.name, "has won", self.hidden)
