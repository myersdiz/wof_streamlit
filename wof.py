import streamlit as st
import pandas as pd
import base64, json, random, time


def set_check_letter(check_letter: bool) -> None:
    if "check_letter" not in st.session_state:
        st.session_state.check_letter = check_letter

    st.session_state.check_letter = check_letter


def zero_contestant_score() -> None:
    st.session_state.contestant_score = 0


def add_to_contenstant_score(prize_amount: int) -> None:
    st.session_state.contestant_score += prize_amount


def set_must_spin_wheel(must_spin_wheel: bool) -> None:
    if "must_spin_wheel" not in st.session_state:
        st.session_state.must_spin_wheel = True

    st.session_state.must_spin_wheel = must_spin_wheel


def set_can_buy_vowel(can_buy_vowel: bool) -> None:
    if "can_buy_vowel" not in st.session_state:
        st.session_state.can_buy_vowel = False

    st.session_state.can_buy_vowel = can_buy_vowel


def set_has_enough_money_to_buy_vowel() -> None:
    if "has_enough_money_to_buy_vowels" not in st.session_state:
        st.session_state.has_enough_money_to_buy_vowels = False

    if st.session_state.contestant_score >= 250:
        st.session_state.has_enough_money_to_buy_vowels = True
    else:
        st.session_state.has_enough_money_to_buy_vowels = False


def set_no_more_consonants() -> None:
    if "no_more_consonants" not in st.session_state:
        st.session_state.no_more_consonants = False

    if not st.session_state.no_more_consonants:
        if len(puzzle_letter_set - set(st.session_state.selected_letters) - set("AEIOU")) == 0:
            st.session_state.no_more_consonants = True
            st.session_state.no_more_consonants_warning = True


def set_no_more_vowels() -> None:
    if "no_more_vowels" not in st.session_state:
        st.session_state.no_more_vowels = False

    if not st.session_state.no_more_vowels:
        if len(puzzle_letter_set - set(st.session_state.selected_letters) - set("BCDFGHJKLMNPQRSTVWXYZ")) == 0:
            st.session_state.no_more_vowels = True
            st.session_state.no_more_vowels_warning = True


def set_disable_consonants(disable_consonants: bool) -> None:
    if "disable_consonants" not in st.session_state:
        st.session_state.disable_consonants = disable_consonants

    st.session_state.disable_consonants = disable_consonants


def set_disable_vowels(disable_vowels: bool) -> None:
    if "disable_vowels" not in st.session_state:
        st.session_state.disable_vowels = disable_vowels

    st.session_state.disable_vowels = disable_vowels


def set_puzzle_solved(puzzle_solved: bool) -> None:
    if "puzzle_solved" not in st.session_state:
        st.session_state.puzzle_solved = puzzle_solved

    if puzzle_solved:
        if st.session_state.contestant_score < 1000:
            st.session_state.contestant_score = 1000

    st.session_state.puzzle_solved = puzzle_solved


def reset_game() -> None:
    get_random_puzzle.clear()

    for key in st.session_state.keys():
        del st.session_state[key]


@st.cache_data
def load_audio_files() -> tuple[str, str, str, str, str]:
    with open("assets/audio/bankrupt.mp3", "rb") as f:
        data = f.read()
        bankrupt_b64 = base64.b64encode(data).decode()

    with open("assets/audio/buzzer.mp3", "rb") as f:
        data = f.read()
        buzzer_b64 = base64.b64encode(data).decode()

    with open("assets/audio/ding.mp3", "rb") as f:
        data = f.read()
        ding_b64 = base64.b64encode(data).decode()

    with open("assets/audio/new_puzzle.mp3", "rb") as f:
        data = f.read()
        new_puzzle_b64 = base64.b64encode(data).decode()

    with open("assets/audio/no_more_consonants.mp3", "rb") as f:
        data = f.read()
        no_more_consonants_b64 = base64.b64encode(data).decode()

    with open("assets/audio/no_more_vowels.mp3", "rb") as f:
        data = f.read()
        no_more_vowels_b64 = base64.b64encode(data).decode()

    with open("assets/audio/solved_puzzle.mp3", "rb") as f:
        data = f.read()
        solved_puzzle_b64 = base64.b64encode(data).decode()

    return bankrupt_b64, buzzer_b64, ding_b64, new_puzzle_b64, no_more_consonants_b64, no_more_vowels_b64, solved_puzzle_b64


def set_audio_queue(audio_file: str, audio_play_count: int) -> None:
    if "audio_queue" not in st.session_state:
        st.session_state.audio_queue = []

    st.session_state.audio_queue.clear()

    st.session_state.audio_queue.append(audio_file)
    st.session_state.audio_queue.append(audio_play_count)


def clear_audio_queue() -> None:
    if "audio_queue" in st.session_state:
        del st.session_state.audio_queue


def play_audio(audio_file: str) -> None:
    st.components.v1.html(
        f"""
        <audio class="{str(random.random())}" autoplay="true">
        <source src="data:audio/mpeg;base64,{audio_file}" type="audio/mpeg">
        </audio>
        """,
        width=0,
        height=0,
        scrolling=False,
    )


@st.cache_data
def load_wheel_prizes() -> dict[str, str]:
    with open("wheel_prizes.json", "r") as f:
        wheel_prizes = json.loads(f.read())

    return wheel_prizes


def get_random_wheel_prize(wheel_prizes) -> tuple[str, str]:
    wheel_prize = random.choice(list(wheel_prizes.items()))

    return wheel_prize


@st.cache_data
def get_random_puzzle(puzzle_file: str) -> tuple[str, str, set]:
    # Load the puzzles from the JSON file
    with open("puzzle_parser/" + puzzle_file.replace(" ", "_").lower() + ".json", "r") as f:
        puzzles = json.loads(f.read())

    # Convert dictionary puzzles to Pandas DataFrame
    df_puzzles = pd.DataFrame(puzzles)

    df_puzzles = df_puzzles.sample(n=1)

    category = df_puzzles["CATEGORY"].values[0]

    puzzle = df_puzzles["PUZZLE"].values[0]

    # Search for parantheses in the puzzle and remove the contents
    if "(" in puzzle and ")" in puzzle:
        puzzle = puzzle[: puzzle.index("(")] + puzzle[puzzle.index(")") + 1 :]

    # Replace "?" with "" in the puzzle
    puzzle = puzzle.replace("?", "")

    # Replace double spaces with single spaces in the puzzle
    puzzle = puzzle.replace("  ", " ")

    round = df_puzzles["ROUND"].values[0]

    if round.startswith("BR"):
        round = "Bonus Round"
    elif round.startswith("R"):
        round = "Round " + round[1:2]
    elif round.startswith("T"):
        round = "Toss-Up Round"
    elif round.startswith("P"):
        round = "Prize Puzzle"
    else:
        round = "Unknown Round"

    # Remove everything but letters from the puzzle and convert it to a set
    puzzle_letter_set = set("".join([c for c in puzzle if c.isalpha()]))

    return category, puzzle, puzzle_letter_set, round


def generate_puzzle_board(puzzle: str) -> dict:
    # Replace letters with underscores
    puzzle_with_underscores = "".join(["_" if c.isalpha() and c not in st.session_state.selected_letters else c for c in puzzle])

    # Count words in puzzle
    puzzle_words = puzzle_with_underscores.split(" ")

    ln_max = 1

    # Create dictionary to hold puzzle lines
    puzzle_lines = {
        "ln1": ["", 0, 12],
        "ln2": ["", 0, 14],
        "ln3": ["", 0, 14],
        "ln4": ["", 0, 12],
    }

    # Create a variable to hold the number of words in the puzzle
    puzzle_word_count = len(puzzle_words)

    # Create a variable to hold the number of words used in the puzzle (so far)
    puzzle_word_used_count = 0

    # Loop through the words in the puzzle
    for puzzle_word in puzzle_words:
        # Loop through the lines in the puzzle
        for ln in range(ln_max, 4):
            # If the length of the line plus the length of the word plus a space is less than or equal to the line length
            if len(puzzle_lines["ln" + str(ln + 1)][0]) + len(puzzle_word) + 1 <= puzzle_lines["ln" + str(ln + 1)][2]:
                puzzle_word_used_count += 1
                puzzle_lines["ln" + str(ln + 1)][0] += puzzle_word + " "
                puzzle_lines["ln" + str(ln + 1)][1] += len(puzzle_word) + 1
                ln_max = ln
                break

    # If the number of words in the puzzle is greater than the number of words used in the puzzle
    if puzzle_word_used_count < puzzle_word_count:
        ln_max = 0

        # Create dictionary to hold puzzle lines
        puzzle_lines = {
            "ln1": ["", 0, 12],
            "ln2": ["", 0, 14],
            "ln3": ["", 0, 14],
            "ln4": ["", 0, 12],
        }

        for puzzle_word in puzzle_words:
            for ln in range(ln_max, 4):
                if len(puzzle_lines["ln" + str(ln + 1)][0]) + len(puzzle_word) + 1 <= puzzle_lines["ln" + str(ln + 1)][2]:
                    puzzle_lines["ln" + str(ln + 1)][0] += puzzle_word + " "
                    puzzle_lines["ln" + str(ln + 1)][1] += len(puzzle_word) + 1
                    ln_max = ln
                    break

    return puzzle_lines


def check_letter(letter: str, round: str) -> None:
    if round == "Bonus Round":
        if letter not in st.session_state.bonus_selected_letters:
            st.session_state.selected_letter = letter
            st.session_state.bonus_selected_letters.append(letter)

        set_check_letter(True)

        st.rerun()
    else:
        if letter not in st.session_state.selected_letters:
            st.session_state.selected_letter = letter
            st.session_state.selected_letters.append(letter)

        set_check_letter(True)
        set_must_spin_wheel(True)

        st.rerun()


if __name__ == "__main__":
    # Load the audio files
    bankrupt_b64, buzzer_b64, ding_b64, new_puzzle_b64, no_more_consonants_b64, no_more_vowels_b64, solved_puzzle_b64 = load_audio_files()

    # Display the title in the sidebar
    st.sidebar.title("Wheel's Fortune")

    # Create a list of season names starting with Season 1 ending with Season 41
    puzzle_files = ["Season " + str(i) for i in range(1, 42)]
    puzzle_files.remove("Season 7")  # Season 7 is missing
    puzzle_files.remove("Season 12")  # Season 12 is missing
    puzzle_files.remove("Season 41")  # Season 41 is corrupt

    # Display the season selection dropdown
    puzzle_file = st.sidebar.selectbox(label="Select a season", options=puzzle_files, on_change=reset_game)

    # Get a random puzzle
    category, puzzle, puzzle_letter_set, round = get_random_puzzle(puzzle_file)

    st.sidebar.write("Puzzle from " + round)

    # Load the wheel prizes
    wheel_prizes = load_wheel_prizes()

    # Create a container to hold the Wheel of Fortune puzzle board image (image added later in code)
    image_container = st.container()

    # Create a container to hold the host messages
    puzzle_message_container = st.container()

    if round != "Bonus Round":
        solve_puzzle = st.chat_input("I'd like to solve the puzzle...", key="solve_puzzle")

        if solve_puzzle:
            if solve_puzzle.lower() == puzzle.lower():
                # Add all the remaining letters to the selected letters
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    if letter not in st.session_state.selected_letters:
                        st.session_state.selected_letters.append(letter)

                puzzle_message_container.success("Congratulations!  You solved the puzzle!")
                set_audio_queue(solved_puzzle_b64, 1)
                set_puzzle_solved(True)
                st.balloons()
            else:
                puzzle_message_container.error("Sorry, that is not the correct answer.")
                set_audio_queue(buzzer_b64, 1)

        if "check_letter" not in st.session_state:
            set_check_letter(False)

        if st.session_state.check_letter:
            set_check_letter(False)

            selected_letter = st.session_state.selected_letter

            set_no_more_consonants()
            set_no_more_vowels()

            # Check if the selected letter is a vowel, subtract $250 from the contestant score
            if selected_letter in ["A", "E", "I", "O", "U"]:
                add_to_contenstant_score(-250)

            # Check if the selected letter is in the puzzle
            if selected_letter in puzzle:
                # Check if the puzzle has been solved
                if puzzle_letter_set.issubset(set(st.session_state.selected_letters)):
                    puzzle_message_container.success("Congratulations!  You solved the puzzle!")
                    set_audio_queue(solved_puzzle_b64, 1)
                    set_puzzle_solved(True)
                    st.balloons()
                else:
                    puzzle_message_container.success("Correct!  There are " + str(puzzle.count(selected_letter)) + " " + selected_letter + "'s in the puzzle.")

                    if selected_letter not in ["A", "E", "I", "O", "U"]:
                        set_can_buy_vowel(True)

                        for i in range(puzzle.count(selected_letter)):
                            add_to_contenstant_score(st.session_state.prize_amount)

                    set_has_enough_money_to_buy_vowel()

                    set_audio_queue(ding_b64, puzzle.count(selected_letter))
            elif selected_letter.isalpha() and selected_letter not in puzzle:
                puzzle_message_container.error("Sorry, there are no " + selected_letter + "'s in the puzzle.")
                set_can_buy_vowel(False)
                set_audio_queue(buzzer_b64, 1)

        # If the selected letters are not in the session state, assume this is the "first game" or a "new game"
        if "selected_letters" not in st.session_state:
            st.session_state.selected_letters = []
            st.session_state.bonus_selected_letters = []

            set_check_letter(False)
            zero_contestant_score()
            set_must_spin_wheel(True)
            set_no_more_consonants()
            set_can_buy_vowel(False)
            set_has_enough_money_to_buy_vowel()
            set_no_more_vowels()
            set_puzzle_solved(False)
            set_audio_queue(new_puzzle_b64, 1)

            puzzle_message_container.warning("Open the sidebar to see puzzles from a different season and also see your score.")

        if st.session_state.no_more_consonants and not st.session_state.puzzle_solved and st.session_state.no_more_consonants_warning:
            puzzle_message_container.warning("No more consonants left in the puzzle.")
            st.session_state.no_more_consonants_warning = False
            set_audio_queue(no_more_consonants_b64, 1)

        if st.session_state.no_more_vowels and not st.session_state.puzzle_solved and st.session_state.no_more_vowels_warning:
            puzzle_message_container.warning("No more vowels left in the puzzle.")
            st.session_state.no_more_vowels_warning = False
            set_audio_queue(no_more_vowels_b64, 1)

        # Display the spin wheel button
        if st.button(label="Spin Wheel", key="spin_wheel", disabled=st.session_state.puzzle_solved):
            set_must_spin_wheel(False)

            wheel_prize = get_random_wheel_prize(wheel_prizes)

            st.session_state.prize_amount = wheel_prize[1]["prize_amount"]

            if wheel_prize[1]["prize_name"] == "Bankrupt":
                zero_contestant_score()
                set_must_spin_wheel(True)
                set_can_buy_vowel(False)
                set_audio_queue(bankrupt_b64, 1)
                puzzle_message_container.error("Sorry, you spun Bankrupt.  You lose all your money.")
            elif wheel_prize[1]["prize_name"] == "Lose a Turn":
                set_must_spin_wheel(True)
                set_can_buy_vowel(False)
                puzzle_message_container.error("Sorry, you spun Lose a Turn.  You lose your turn.")
            else:
                set_must_spin_wheel(False)
                set_can_buy_vowel(False)
                puzzle_message_container.success("You spun " + wheel_prize[1]["prize_name"])

        # Display the contestant score
        st.sidebar.write("Contestant Score: $" + str(st.session_state.contestant_score))

        play_audio_checkbox = st.sidebar.checkbox("Play Audio", value=True)

        # Display the new puzzle button
        if st.sidebar.button(label="New Puzzle", key="new_puzzle"):
            reset_game()
            st.rerun()

        # Disable consonants if:
        # 1. The contestant must spin the wheel
        # 2. The puzzle does not contain any more consonants
        # 3. The puzzle has been solved
        st.session_state.disable_consonants = st.session_state.must_spin_wheel or st.session_state.no_more_consonants or st.session_state.puzzle_solved

        # Disable vowels if:
        # 1. The contestant cannot buy a vowel
        # 2. The contestant does not have enough money to buy a vowel
        # 3. The puzzle does not contain any more vowels
        # 4. The puzzle has been solved
        st.session_state.disable_vowels = (
            not st.session_state.can_buy_vowel
            or st.session_state.no_more_vowels
            or not st.session_state.has_enough_money_to_buy_vowels
            or st.session_state.puzzle_solved
        )
    else:
        # If the selected letters are not in the session state, assume this is the "first game" or a "new game"
        if "selected_letters" not in st.session_state:
            st.session_state.selected_letters = []
            st.session_state.bonus_selected_letters = []

            set_check_letter(False)
            zero_contestant_score()
            set_puzzle_solved(None)
            set_audio_queue(new_puzzle_b64, 1)

            set_disable_consonants(False)
            set_disable_vowels(True)

            puzzle_message_container.warning("Open the sidebar to see puzzles from a different season and also see your score.")

            for letter in "RSTLNE":
                if letter not in st.session_state.selected_letters:
                    st.session_state.selected_letters.append(letter)

            puzzle_message_container.warning("The letters R, S, T, L, N, and E are already filled in for you.  Choose 3 more consonants and 1 more vowel.")

        if "check_letter" not in st.session_state:
            set_check_letter(False)

        if st.session_state.check_letter:
            if "bonus_consonant_count" not in st.session_state:
                st.session_state.bonus_consonant_count = 0

            if "bonus_vowel_count" not in st.session_state:
                st.session_state.bonus_vowel_count = 0

            if st.session_state.bonus_consonant_count < 2:
                st.session_state.bonus_consonant_count += 1

                if st.session_state.bonus_consonant_count > 0:
                    puzzle_message_container.warning("Choose another consonant.")

                set_check_letter(False)
                set_disable_consonants(False)
                set_disable_vowels(True)
            elif st.session_state.bonus_vowel_count < 1:
                puzzle_message_container.warning("Choose a vowel.")

                st.session_state.bonus_vowel_count += 1

                set_check_letter(False)
                set_disable_consonants(True)
                set_disable_vowels(False)
            else:
                for letter in st.session_state.bonus_selected_letters:
                    st.session_state.selected_letters.append(letter)

                set_check_letter(True)
                set_disable_consonants(True)
                set_disable_vowels(True)

                solve_puzzle = st.chat_input("I'd like to solve the puzzle...", key="solve_puzzle")

                if solve_puzzle:
                    if solve_puzzle.lower() == puzzle.lower():
                        puzzle_message_container.success("Congratulations!  You solved the puzzle!")
                        set_audio_queue(solved_puzzle_b64, 1)
                        set_puzzle_solved(True)
                        st.balloons()
                    else:
                        puzzle_message_container.error("Sorry, that is not the correct answer.")
                        set_audio_queue(buzzer_b64, 1)
                        set_puzzle_solved(False)

                    # Add all the remaining letters to the selected letters
                    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        if letter not in st.session_state.selected_letters:
                            st.session_state.selected_letters.append(letter)

                if st.session_state.puzzle_solved is None:
                    puzzle_message_container.warning("You get only one chance to solve the puzzle!  Good luck.")

        # Display the contestant score
        st.sidebar.write("Contestant Score: $" + str(st.session_state.contestant_score))

        play_audio_checkbox = st.sidebar.checkbox("Play Audio", value=True)

        # Display the new puzzle button
        if st.sidebar.button(label="New Puzzle", key="new_puzzle"):
            reset_game()
            st.rerun()

    # endif

    st.write("Letter board")

    st.write(
        """<style>
            [data-testid="column"] {
                width: calc(10% - 1rem) !important;
                flex: 1 1 calc(10% - 1rem) !important;
                min-width: calc(10% - 1rem) !important;
            }
            </style>""",
        unsafe_allow_html=True,
    )

    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10 = st.columns(10)

    if col_1.button(
        label="A",
        key="A",
        disabled="A" in st.session_state.selected_letters or "A" in st.session_state.bonus_selected_letters or st.session_state.disable_vowels,
    ):
        check_letter("A", round)

    if col_2.button(
        label="B",
        key="B",
        disabled="B" in st.session_state.selected_letters or "B" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("B", round)

    if col_3.button(
        label="C",
        key="C",
        disabled="C" in st.session_state.selected_letters or "C" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("C", round)

    if col_4.button(
        label="D",
        key="D",
        disabled="D" in st.session_state.selected_letters or "D" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("D", round)

    if col_5.button(
        label="E",
        key="E",
        disabled="E" in st.session_state.selected_letters or "E" in st.session_state.bonus_selected_letters or st.session_state.disable_vowels,
    ):
        check_letter("E", round)

    if col_6.button(
        label="F",
        key="F",
        disabled="F" in st.session_state.selected_letters or "F" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("F", round)

    if col_7.button(
        label="G",
        key="G",
        disabled="G" in st.session_state.selected_letters or "G" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("G", round)

    if col_8.button(
        label="H",
        key="H",
        disabled="H" in st.session_state.selected_letters or "H" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("H", round)

    if col_9.button(
        label="I",
        key="I",
        disabled="I" in st.session_state.selected_letters or "I" in st.session_state.bonus_selected_letters or st.session_state.disable_vowels,
    ):
        check_letter("I", round)

    if col_10.button(
        label="J",
        key="J",
        disabled="J" in st.session_state.selected_letters or "J" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("J", round)

    if col_1.button(
        label="K",
        key="K",
        disabled="K" in st.session_state.selected_letters or "K" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("K", round)

    if col_2.button(
        label="L",
        key="L",
        disabled="L" in st.session_state.selected_letters or "L" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("L", round)

    if col_3.button(
        label="M",
        key="M",
        disabled="M" in st.session_state.selected_letters or "M" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("M", round)

    if col_4.button(
        label="N",
        key="N",
        disabled="N" in st.session_state.selected_letters or "N" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("N", round)

    if col_5.button(
        label="O",
        key="O",
        disabled="O" in st.session_state.selected_letters or "O" in st.session_state.bonus_selected_letters or st.session_state.disable_vowels,
    ):
        check_letter("O", round)

    if col_6.button(
        label="P",
        key="P",
        disabled="P" in st.session_state.selected_letters or "P" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("P", round)

    if col_7.button(
        label="Q",
        key="Q",
        disabled="Q" in st.session_state.selected_letters or "Q" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("Q", round)

    if col_8.button(
        label="R",
        key="R",
        disabled="R" in st.session_state.selected_letters or "R" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("R", round)

    if col_9.button(
        label="S",
        key="S",
        disabled="S" in st.session_state.selected_letters or "S" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("S", round)

    if col_10.button(
        label="T",
        key="T",
        disabled="T" in st.session_state.selected_letters or "T" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("T", round)

    if col_1.button(
        label="U",
        key="U",
        disabled="U" in st.session_state.selected_letters or "U" in st.session_state.bonus_selected_letters or st.session_state.disable_vowels,
    ):
        check_letter("U", round)

    if col_2.button(
        label="V",
        key="V",
        disabled="V" in st.session_state.selected_letters or "V" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("V", round)

    if col_3.button(
        label="W",
        key="W",
        disabled="W" in st.session_state.selected_letters or "W" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("W", round)

    if col_4.button(
        label="X",
        key="X",
        disabled="X" in st.session_state.selected_letters or "X" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("X", round)

    if col_5.button(
        label="Y",
        key="Y",
        disabled="Y" in st.session_state.selected_letters or "Y" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("Y", round)

    if col_6.button(
        label="Z",
        key="Z",
        disabled="Z" in st.session_state.selected_letters or "Z" in st.session_state.bonus_selected_letters or st.session_state.disable_consonants,
    ):
        check_letter("Z", round)

    # Generate the puzzle board lines
    puzzle_lines = generate_puzzle_board(puzzle)

    # Display the Wheel of Fortune puzzle board
    image_container.image(
        """https://www.thewordfinder.com/wof-puzzle-generator/puzzle.php?bg=2&ln1="""
        + puzzle_lines["ln1"][0]
        + """&ln2="""
        + puzzle_lines["ln2"][0]
        + """&ln3="""
        + puzzle_lines["ln3"][0]
        + """&ln4="""
        + puzzle_lines["ln4"][0]
        + """&cat="""
        + category.replace("&", "%26")
        + """&"""
    )

    if (st.session_state.puzzle_solved and round != 'Bonus Round') or (st.session_state.puzzle_solved is not None and round == 'Bonus Round'):
        puzzle_message_container.success("Open the sidebar and click 'New Puzzle' to play again!")

    st.sidebar.caption(
        "This Streamlit application is dedicated to the popular television game show Wheel of Fortune.  "
        + "It is not affiliated with Wheel of Fortune, Sony Pictures, or any of its affiliates.  "
        + "No challenge to ownership is implied, and all marks, logos, images, and other materials used "
        + "wherein remain property of their respective owners."
    )

    if "audio_queue" in st.session_state:
        if play_audio_checkbox:
            for i in range(st.session_state.audio_queue[1]):
                play_audio(st.session_state.audio_queue[0])

                if st.session_state.audio_queue[1] > 1:
                    time.sleep(1.5)

        clear_audio_queue()
