import tkinter as tk
import random
from fivecarddraw_poker import*

class PokerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Five Card Draw Poker")
        self.root.geometry("600x400")
        self.deck = create_deck()
        random.shuffle(self.deck)
        # state of the game
        self.player_hand = [draw_card(self.deck) for _ in range(5)]
        self.computer_hand = [draw_card(self.deck) for _ in range(5)]
        self.selected = set()          
        self.round = 1
        self.player_wins = 0
        self.computer_wins = 0
        #gui
        self.create_widgets()
        self.show_player_hand()

    def create_widgets(self):
        self.score_label = tk.Label(self.root, text="Round 1  |  You 0 - 0 Computer", font=("Arial", 14))
        self.score_label.pack(pady=10)

        #player hand 
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=20)
        self.card_buttons = []

        #buttons
        self.draw_button = tk.Button(self.root, text="Draw Selected Cards", command=self.draw_cards, state=tk.NORMAL)
        self.draw_button.pack(pady=5)

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

        self.status_label = tk.Label(self.root, text="Click cards to select, then press Draw", font=("Arial", 10))
        self.status_label.pack(pady=5)

        #computer hand
        self.computer_frame = tk.Frame(self.root)
        self.computer_frame.pack(pady=20)
        self.computer_labels = []
        self.hide_computer_hand()

        #next round
        self.next_button = tk.Button(self.root, text="Next Round", command=self.next_round, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        #discard selected cards
    def draw_cards(self):
        for idx in sorted(self.selected, reverse=True):
            self.player_hand.pop(idx)
        #draw new cards
        while len(self.player_hand) < 5 and self.deck:
            self.player_hand.append(draw_card(self.deck))
        self.show_player_hand()

        #ai turn
        comp_discard = computer_discard(self.computer_hand)
        for idx in sorted(comp_discard, reverse=True):
            self.computer_hand.pop(idx)
        while len(self.computer_hand) < 5 and self.deck:
            self.computer_hand.append(draw_card(self.deck))

            #showdown 
            self.showdown()

    def hide_computer_hand(self):
        for lbl in self.computer_labels:
            lbl.destroy()
            self.computer.labels.clear()
        for _ in range(5):
            lbl = tk.Label(self.computer_frame, text="🂠", font=("Arial", 20), width=3)

            #reveals cards
    def showdown(self):
        for i, lbl, in enumerate(self.computer_labels):
            rank, suit = self.computer_hand[i]
            lbl.config(text=f"{rank}{suit}")

        #evaluation
        player_score = hand_rank(self.player_hand)
        player_hand_name = HAND_NAMES[player_score[0]]
        computer_score = hand_rank(self.computer_hand)
        computer_hand_name = HAND_NAMES[computer_score[0]]

        if player_score > computer_score:
            result = "You win this round!"
            self.player_wins += 1
        elif computer_score > player_score:
            result = "You lose this round!"
            self.computer_wins += 1
        else:
            result = "Tied round!"
        self.status_label.config(text=f"{result} You: {player_hand_name} Computer: {computer_hand_name}")
        self.score_label.config(text=f"Round {self.round} | You {self.player_wins} - {self.computer_wins} Computer")

        #enables next round, prevents more drawing
        self.draw_button.config(state=tk.DISABLED)
        if self.round < 5:
            self.next_button.config(state=tk.NORMAL)
        else:
            if self.player_wins > self.computer_wins:
                final = "You win the match!"
            elif self.computer_wins > self.player_wins:
                final = "You lose the match!"
            else:
                final = "Match tied!"
            self.status_label.config(text=final)

        #resets cards for next round
    def next_round(self):
            self.round += 1
            self.deck = create_deck()
            random.shuffle(self.deck)
            self.player_hand = [draw_card(self.deck) for _ in range(5)]
            self.computer_hand = [draw_card(self.deck) for _ in range(5)]
            self.selected.clear()
            self.show_player_hand()
            self.hide_computer_hand()
            self.draw_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
            self.status_label.config(text="Click to select cards to draw.")
            self.score_label.config(text=f"Round {self.round}  |  You {self.player_wins} - {self.computer_wins} Computer")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerGame(root)
    root.mainloop()
