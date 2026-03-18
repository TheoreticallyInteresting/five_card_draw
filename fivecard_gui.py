import tkinter as tk
import random
from fivecarddraw_poker import *

class PokerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Five Card Draw Poker - Betting Version")
        self.root.geometry("700x600")

        # chip and pot beginning of game
        self.player_chips = 100
        self.computer_chips = 100
        self.pot = 0
        self.ante = 5

        # state of the game
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.computer_hand = []
        self.selected = set()
        self.game_over = False

        #gui
        self.create_widgets()
        self.start_new_hand()

    def create_widgets(self):
        # add frame for pot and chips
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        self.player_chips_label = tk.Label(info_frame, text=f"Your chips: {self.player_chips}", font=("Arial", 12))
        self.player_chips_label.grid(row=0, column=0, padx=20)
        self.pot_label = tk.Label(info_frame, text=f"Pot: {self.pot}", font=("Arial", 12))
        self.pot_label.grid(row=0, column=1, padx=20)
        self.computer_chips_label = tk.Label(info_frame, text=f"Computer chips: {self.computer_chips}", font=("Arial", 12))
        self.computer_chips_label.grid(row=0, column=2, padx=20)

        #player hand
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=20)
        self.card_buttons = []

        #frame for buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        self.draw_button = tk.Button(control_frame, text="Draw Selected Cards", command=self.draw_cards, state=tk.NORMAL)
        self.draw_button.grid(row=0, column=0, padx=5)

        # Bet entry and button
        tk.Label(control_frame, text="Bet amount:").grid(row=0, column=1, padx=5)
        self.bet_entry = tk.Entry(control_frame, width=8)
        self.bet_entry.grid(row=0, column=2, padx=5)
        self.bet_button = tk.Button(control_frame, text="Place Bet", command=self.player_bet, state=tk.DISABLED)
        self.bet_button.grid(row=0, column=3, padx=5)

        self.check_button = tk.Button(control_frame, text="Check", command=self.player_check, state=tk.DISABLED)
        self.check_button.grid(row=0, column=4, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # computer hand gui
        self.computer_frame = tk.Frame(self.root)
        self.computer_frame.pack(pady=20)
        self.computer_labels = []

        # next hand button
        self.next_hand_button = tk.Button(self.root, text="Next Hand", command=self.next_hand, state=tk.DISABLED)
        self.next_hand_button.pack(pady=10)

    def start_new_hand(self):
        #set up hand. deduct antes, deal cards, update display.
        if self.game_over:
            return

        # chip antes
        self.player_chips -= self.ante
        self.computer_chips -= self.ante
        self.pot = self.ante * 2
        self.update_chips_display()

        # check for players chips
        if self.player_chips < 0:
            self.player_chips = 0
            self.game_over = True
            self.status_label.config(text="You're out of chips! Computer wins.")
            return
        if self.computer_chips < 0:
            self.computer_chips = 0
            self.game_over = True
            self.status_label.config(text="Computer is out of chips! You win!")
            return

        # creates deck and deals to players
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = [draw_card(self.deck) for _ in range(5)]
        self.computer_hand = [draw_card(self.deck) for _ in range(5)]
        self.selected.clear()

        # hides the computer hand
        self.show_player_hand()
        self.hide_computer_hand()

        # enable draw button and disable others until drawn
        self.draw_button.config(state=tk.NORMAL)
        self.bet_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.config(state=tk.DISABLED)
        self.next_hand_button.config(state=tk.DISABLED)
        self.status_label.config(text="Select cards to discard, then click Draw.")

    def show_player_hand(self):
        for btn in self.card_buttons:
            btn.destroy()
        self.card_buttons.clear()
        self.selected.clear()

        for i, (rank, suit) in enumerate(self.player_hand):
            btn = tk.Button(self.player_frame, text=f"{rank}{suit}", width=6, height=3,
                            command=lambda idx=i: self.toggle_select(idx))
            btn.grid(row=0, column=i, padx=5)
            self.card_buttons.append(btn)

    def toggle_select(self, idx):
        if idx in self.selected:
            self.selected.remove(idx)
            self.card_buttons[idx].config(relief=tk.RAISED, bg='SystemButtonFace')
        else:
            self.selected.add(idx)
            self.card_buttons[idx].config(relief=tk.SUNKEN, bg='lightblue')

    def hide_computer_hand(self):
        for lbl in self.computer_labels:
            lbl.destroy()
        self.computer_labels.clear()
        for _ in range(5):
            lbl = tk.Label(self.computer_frame, text="🂠", font=("Arial", 20), width=3)
            lbl.pack(side=tk.LEFT, padx=5)
            self.computer_labels.append(lbl)

    def draw_cards(self):
        #player discards
        for idx in sorted(self.selected, reverse=True):
            self.player_hand.pop(idx)
        while len(self.player_hand) < 5 and self.deck:
            self.player_hand.append(draw_card(self.deck))
        self.show_player_hand()

        #computer discards then draws
        comp_discard = computer_discard(self.computer_hand)
        for idx in sorted(comp_discard, reverse=True):
            self.computer_hand.pop(idx)
        while len(self.computer_hand) < 5 and self.deck:
            self.computer_hand.append(draw_card(self.deck))

        # betting controls activated
        self.draw_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.NORMAL)
        self.bet_button.config(state=tk.NORMAL if self.player_chips > 0 else tk.DISABLED)
        self.check_button.config(state=tk.NORMAL)
        self.status_label.config(text="Enter bet amount (or 0 to check) and click Place Bet, or Check.")

    def player_bet(self):
        # gets bet input
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            self.status_label.config(text="Invalid bet amount. Enter a number.")
            return

        if bet < 0:
            self.status_label.config(text="Bet cannot be negative.")
            return
        if bet > self.player_chips:
            self.status_label.config(text=f"You only have {self.player_chips} chips.")
            return

        if bet == 0:
            self.player_check()
            return

        # bet update
        self.player_chips -= bet
        self.pot += bet
        self.update_chips_display()

        #computer logic
        comp_rank = hand_rank(self.computer_hand)[0]
        #computer will call if hand rank is >=1 with chips
        if comp_rank >= 1 and self.computer_chips >= bet:
            self.computer_chips -= bet
            self.pot += bet
            self.status_label.config(text=f"Computer calls {bet}.")
            self.update_chips_display()
            self.showdown()
        else:
            # folds
            self.status_label.config(text=f"Computer folds. You win {self.pot} chips!")
            self.player_chips += self.pot
            self.pot = 0
            self.update_chips_display()
            self.end_hand()

    def player_check(self):
        self.status_label.config(text="You check. Computer checks. Showdown!")
        self.showdown()

    def showdown(self):
        # shows computer hand
        for i, lbl in enumerate(self.computer_labels):
            rank, suit = self.computer_hand[i]
            lbl.config(text=f"{rank}{suit}")

        # evaluates hands
        player_score = hand_rank(self.player_hand)
        computer_score = hand_rank(self.computer_hand)
        player_hand_name = HAND_NAMES[player_score[0]]
        computer_hand_name = HAND_NAMES[computer_score[0]]

        if player_score > computer_score:
            self.player_chips += self.pot
            result = f"You win {self.pot} chips with {player_hand_name} vs {computer_hand_name}!"
        elif computer_score > player_score:
            self.computer_chips += self.pot
            result = f"Computer wins {self.pot} chips with {computer_hand_name} vs {player_hand_name}!"
        else:
            # tie logic, split, remainder to player
            half = self.pot // 2
            self.player_chips += half
            self.computer_chips += (self.pot - half)  
            result = f"Tie! You get {half}, computer gets {self.pot - half}."

        self.pot = 0
        self.status_label.config(text=result)
        self.update_chips_display()
        self.end_hand()

    def end_hand(self):
    #"check game over and enable next hand button.
        self.bet_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.DISABLED)
        self.draw_button.config(state=tk.DISABLED)

        #game over check
        if self.player_chips <= 0:
            self.game_over = True
            self.status_label.config(text="You're out! Game over.")
        elif self.computer_chips <= 0:
            self.game_over = True
            self.status_label.config(text="Computer Busts! You win!")
        else:
            self.next_hand_button.config(state=tk.NORMAL)

    def next_hand(self):
        self.next_hand_button.config(state=tk.DISABLED)
        self.start_new_hand()

    def update_chips_display(self):
        self.player_chips_label.config(text=f"Your chips: {self.player_chips}")
        self.computer_chips_label.config(text=f"Computer chips: {self.computer_chips}")
        self.pot_label.config(text=f"Pot: {self.pot}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerGame(root)
    root.mainloop()
