from tkinter import *
from functools import partial  # To prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        error_feedback = ""
        # GUI to get starting balance and stakes

        self.parent = parent
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # Mystery Heading
        self.mystery_box_label = Label(self.start_frame,
                                       text="Mystery Box Game",
                                       font="Arial 19 bold")
        self.mystery_box_label.grid(row=0)

        self.mystery_instructions = Label(self.start_frame, font="Arial 10 italic",
                                          text="Please enter a dollar amount "
                                               "(between $5 and $50) in the box "
                                               "below. Then choose the stakes. "
                                               "The higher the stakes, the more you "
                                               "can win.",
                                          wrap=275, justify=LEFT, padx=10, pady=10)

        self.mystery_instructions.grid(row=1)

        self.entry_error_frame = Frame(self.start_frame, width=12)
        self.entry_error_frame.grid(row=2)

        # Entry box... (row 1)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 19 bold", width=10)
        self.start_amount_entry.grid(row=0)

        self.add_funds = Button(self.entry_error_frame, font="Arial 14 bold",
                                text="Add Funds", command=lambda: self.check_funds())
        self.add_funds.grid(row=0, column=1)

        self.framefinal = Frame(self.entry_error_frame, bg='black')
        self.framefinal.grid(row=1, pady=10)

        self.amount_error_label = Label(fg="black",
                                        font="Arial 9 bold",
                                        justify=LEFT, text="")

        self.amount_error_label.grid(row=0, column=0)
        self.amount_error_label.place(x=20, y=175)

        # Button Frame
        self.button_frame = Frame(self.start_frame)
        self.button_frame.grid(row=3)

        button_font = "Arial 12 bold"

        # Play Button
        self.lowstakes_button = Button(self.button_frame, bg="DarkOrange1", font=button_font, text="Low ($5)",
                                       command=lambda: self.to_game(1))
        self.lowstakes_button.grid(row=0, pady=10, column=0)

        self.midstakes_button = Button(self.button_frame, text="Medium ($10)", font=button_font, bg="yellow",
                                       command=lambda: self.to_game(1))
        self.midstakes_button.grid(row=0, pady=10, column=1, padx=5)

        self.highstakes_button = Button(self.button_frame, text="High ($15)", font=button_font, bg="green1",
                                        command=lambda: self.to_game(1))
        self.highstakes_button.grid(row=0, pady=10, column=2, padx=5)

        self.lowstakes_button.config(state=DISABLED)
        self.midstakes_button.config(state=DISABLED)
        self.highstakes_button.config(state=DISABLED)

        self.help_button = Button(self.button_frame, text="How to Play", bg='grey', fg='white',
                                  font=button_font, command=lambda: self.to_help())
        self.help_button.grid(row=1, pady=10, column=1)

    def to_help(self):
        self.start_frame.destroy()
        self.entry_error_frame.destroy()
        Help()

    def check_funds(self):
        global error_feedback
        starting_balance = self.start_amount_entry.get()

        # Set error background colours (assume there are
        # no errors at the start
        error_back = "coral"
        has_errors = "no"

        # change background to white
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        self.lowstakes_button.config(state=DISABLED)
        self.midstakes_button.config(state=DISABLED)
        self.highstakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, least you can play is $5"

            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "The most you can risk is $50"

            elif starting_balance >= 15:
                # enable all buttons
                self.lowstakes_button.config(state=NORMAL)
                self.midstakes_button.config(state=NORMAL)
                self.highstakes_button.config(state=NORMAL)

            elif starting_balance >= 10:
                # enable low and medium stakes button
                self.lowstakes_button.config(state=NORMAL)
                self.midstakes_button.config(state=NORMAL)

            else:
                self.lowstakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"
        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            # set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):

        # retrieve starting balance
        starting_balance = self.starting_funds.get()
        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()


class Help:
    def __init__(self):
        self.start_frame = Frame()
        self.start_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.help_title = Label(self.start_frame, text="I am too lazy to write the help script",
                                font="Arial 12 bold")
        self.help_title.grid(row=0)

        self.return_button = Button(self.start_frame, text="Return", font="Arial 16 bold",
                                    padx=10, pady=10, command=lambda: self.return_main())
        self.return_button.grid(row=1)

    def return_main(self):
        self.start_frame.destroy()
        Start(self)


class Game:
    def __init__(self, partner, stakes, starting_balance):

        self.starting_balance = starting_balance

        # Initialise Variables
        self.new_window = Toplevel()

        # If users press cross at top, game quits
        self.new_window.protocol("WM_DELETE_WINDOW", self.to_quit)

        self.balance = IntVar()
        self.balance.set(starting_balance)

        # Get value of stakes (use it as multiplier when calculating winnings
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # List for holding statistics
        self.round_stats_list = []
        self.game_stats_list = [starting_balance, starting_balance]

        # GUI setup
        self.game_frame = Frame(self.new_window)
        self.game_frame.grid(row=0)

        # Heading Row

        # Boxes go here (row 2)
        box_text = "Arial 16 bold"
        box_back = "pale green"
        box_width = 5

        photo = PhotoImage(file="question.gif")
        photo.height()
        self.box_frame = Frame(self.new_window)
        self.box_frame.grid(row=2, pady=10)

        self.prize1_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, image=photo, padx=10,
                                  pady=10)
        self.prize1_label.photo = photo
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, padx=10,
                                  pady=10, image=photo)
        self.prize2_label.photo = photo
        self.prize2_label.grid(row=0, column=1, padx=10)

        self.prize3_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, padx=10, pady=10,
                                  image=photo)
        self.prize3_label.photo = photo
        self.prize3_label.grid(row=0, column=2)

        # Play button goes here (row 3)
        self.play_button = Button(self.game_frame, text="Open Boxes", bg="grey",
                                  font="Arial 15 bold", width=20, padx=10, pady=10,
                                  command=self.reveal_boxes)

        # bind button to <enter> (users can push enter to reveal the boxes)

        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

        # Balance Label (row 4)
        start_text = "Game Cost: ${} \n""\nHow much " \
                     "will you win?".format(starting_balance)

        self.balance_label = Label(self.game_frame, font="Arial 12 bold",
                                   fg="green", text=start_text, wrap=300,
                                   justify=LEFT)
        self.balance_label.grid(row=4, pady=10)

        # Help and Game stats button (row 5)
        self.help_export_frame = Frame(self.game_frame)
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules",
                                  font="Arial 15 bold", bg="grey", fg="white",
                                  command=lambda: self.to_help_2())
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats...",
                                   font="Arial 15 bold", bg="blue", fg="white",
                                   command=self.to_game_stats)
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white",
                                  bg="DarkOrange4", font="Arial 15 bold", width=20,
                                  command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def to_help_2(self):
        help_2()

    def reveal_boxes(self):

        # retrieve the balance from the initial function...
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()
        round_winnings = 0
        prizes = []
        backgrounds = []
        prize_pic = []

        for i in range(0, 3):
            prize_num = random.randint(1, 100)

            if 0 < prize_num <= 5:
                prize = PhotoImage(file="gold_med.gif")
                prize_list = "gold (${})".format(5 * stakes_multiplier)
                back_color = "gold"
                round_winnings += 5 * stakes_multiplier

            elif 5 < prize_num <= 25:
                prize = PhotoImage(file="silver_med.gif")
                prize_list = "silver (${})".format(2 * stakes_multiplier)
                back_color = "seashell3"
                round_winnings += 2 * stakes_multiplier

            elif 25 < prize_num <= 65:
                prize = PhotoImage(file="copper_med.gif")
                prize_list = "copper (${})".format(1 * stakes_multiplier)
                round_winnings += stakes_multiplier
                back_color = "dark goldenrod"
            else:
                prize = PhotoImage(file="lead.gif")
                prize_list = "lead ($0)"
                back_color = "dim gray"

            prize_pic.append(prize)
            prizes.append(prize_list)
            backgrounds.append(back_color)

        photo1 = prize_pic[0]
        photo2 = prize_pic[1]
        photo3 = prize_pic[2]

        self.cb = current_balance
        # Display prizes...
        self.prize1_label.config(image=photo1)
        self.prize1_label.photo = photo1

        self.prize2_label.config(image=photo2)
        self.prize2_label.photo = photo2

        self.prize3_label.config(image=photo3)
        self.prize3_label.photo = photo3

        # Deduct cost of game
        current_balance -= 5 * stakes_multiplier

        # Add winnings
        current_balance += round_winnings

        # Set balance to new balance
        self.balance.set(current_balance)

        self.game_stats_list[1] = current_balance

        balance_statement = "Game Cost: ${}\nPayback: ${} \n" \
                            "Current Balance: ${}".format(5 * stakes_multiplier,
                                                          round_winnings,
                                                          current_balance)
        self.b_s = balance_statement
        # Add round results to statistics list
        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: ".format(prizes[0], prizes[1], prizes[2],
                                                                  5 * stakes_multiplier, round_winnings,
                                                                  current_balance)
        self.round_stats_list.append(round_summary)

        # Edit label so user can see their balance
        self.balance_label.configure(text=balance_statement)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.new_window.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance ${}\n" \
                                "Your balance is too low. You can only quit " \
                                "or view your stats.".format(current_balance)

            self.balance_label.config(fg="DarkOrange4", font="Arial 10 bold",
                                      text=balance_statement)

    def to_quit(self):
        root.destroy()

    def to_game_stats(self):
        Game.reveal_boxes(self)
        start = self.cb
        balance_statement = self.b_s

        GameStats(self, balance_statement, start)


class help_2:
    def __init__(self):
        self.new_win = Toplevel()
        self.frame_1 = Frame(self.new_win)
        self.frame_1.grid()

        self.label = Label(self.frame_1, text="Help",
                           font="Arial 19 bold")
        self.label.grid(row=0)

        self.label_1 = Label(self.frame_1, text="Too lazy to write help script",
                             font="Arial 19 bold")
        self.label_1.grid(row=0)

        self.return_button = Button(self.frame_1, text="Return", padx=10, pady=10,
                                    font="Arial 16 bold", command=lambda: self.quit_help())
        self.return_button.grid(row=2)

    def quit_help(self):
        self.new_win.destroy()


class GameStats:

    def __init__(self, partner, balance_statement, start):
        self.new_window = Toplevel()
        self.new_window.grid()

        self.frame_1 = Frame(self.new_window)
        self.frame_1.grid()

        self.label = Label(self.frame_1, text="Game Statistics",
                           font="Arial 19 bold")
        self.label.grid(row=0)

        self.label_2 = Label(self.frame_1, text="Here are your Game "
                                                "Statistics. Please use "
                                                "the Export button to access the "
                                                "results of each round that you played",
                             wrap=150, justify=LEFT, fg='green')
        self.label_2.grid(row=1, column=0)

        self.label_3 = Label(self.frame_1, text="{}".format(balance_statement), font="Arial 11 bold")

        self.label_3.grid(row=2)
        # "Current Balance: ${}\n" "Amount Lost: ${}\n" "Rounds Played: ${}"

        self.button_frame_1 = Frame(self.frame_1)
        self.button_frame_1.grid(row=3)

        self.export = Button(self.button_frame_1, text="Export", bg="blue",
                             fg="white", font="Arial 16 bold")
        self.export.grid(row=0)

        self.dismiss = Button(self.button_frame_1, text="Dismiss", bg="red",
                              fg="white", font="Arial 16 bold", command=lambda: self.quit_tab(), )
        self.dismiss.grid(row=0, column=1)

    def quit_tab(self):
        self.new_window.destroy()


# Main Routine
if __name__ == "__main__":
    root = Tk()
    Start(root)
    root.title("Mystery Box")
    root.mainloop()
