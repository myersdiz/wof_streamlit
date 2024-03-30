import streamlit as st
import pandas as pd
import base64, json, random, time


def set_check_letter(check_letter: bool) -> None:
    if "check_letter" not in st.session_state:
        st.session_state.check_letter = check_letter

    st.session_state.check_letter = check_letter


def add_amount_to_contenstant_score(add_prize_amount: int) -> None:
    if "contestant_score" not in st.session_state:
        st.session_state.contestant_score = add_prize_amount

    st.session_state.contestant_score += add_prize_amount


def set_must_spin_wheel(must_spin_wheel: bool) -> None:
    if "must_spin_wheel" not in st.session_state:
        st.session_state.must_spin_wheel = True

    st.session_state.must_spin_wheel = must_spin_wheel


def set_has_enough_money_to_buy_vowel() -> None:
    if "has_enough_month_to_buy_vowels" not in st.session_state:
        st.session_state.has_enough_month_to_buy_vowels = False

    if st.session_state.contestant_score >= 250:
        st.session_state.has_enough_month_to_buy_vowels = True
    else:
        st.session_state.has_enough_month_to_buy_vowels = False


def set_puzzle_solved(puzzle_solved: bool) -> None:
    if "puzzle_solved" not in st.session_state:
        st.session_state.puzzle_solved = False

    st.session_state.puzzle_solved = puzzle_solved


def reset_game() -> None:
    get_random_puzzle.clear()

    # Clear the session state keys and values
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

    with open("assets/audio/solved_puzzle.mp3", "rb") as f:
        data = f.read()
        solved_puzzle_b64 = base64.b64encode(data).decode()

    return bankrupt_b64, buzzer_b64, ding_b64, new_puzzle_b64, solved_puzzle_b64


def play_audio(audio_file: str) -> None:
    random_class = str(random.random())

    html_audio_tag = f"""
        <audio class="{random_class}" autoplay="true">
        <source src="data:audio/mp3;base64,{audio_file}" type="audio/mp3">
        </audio>
        """

    st.components.v1.html(html_audio_tag, width=0, height=0, scrolling=False)


@st.cache_data
def load_wheel_prizes() -> list[str]:
    with open("wheel_prizes.json", "r") as f:
        wheel_prizes = json.loads(f.read())

    return wheel_prizes


def get_wheel_prize(wheel_prizes) -> dict[str, str]:
    wheel_prize = random.choice(list(wheel_prizes.items()))

    return wheel_prize


@st.cache_data
def get_random_puzzle(puzzle_file: str) -> tuple[str, str, set]:
    # Load the puzzles from the JSON file
    with open("puzzle_parser/" + puzzle_file.replace(" ","_").lower() + ".json", "r") as f:
        puzzles = json.loads(f.read())

    # Convert dictionary puzzles to Pandas DataFrame
    df_puzzles = pd.DataFrame(puzzles)

    # Pick one random row from the Pandas DataFrame
    df_puzzles = df_puzzles.sample(n=1)

    category = df_puzzles["CATEGORY"].values[0]

    puzzle = df_puzzles["PUZZLE"].values[0]

    round = df_puzzles["ROUND"].values[0]

    if round.startswith("BR"):
        round = "Bonus Round"
    elif round.startswith("R"):
        round = "Round " + round[1:2]
    elif round.startswith("T"):
        round = "Toss-Up Round"
    else:
        round = "Unknown Round"

    # Remove everything but letters from the puzzle and convert it to a set
    puzzle_letter_set = set("".join([c for c in puzzle if c.isalpha()]))

    return category, puzzle, puzzle_letter_set, round


def generate_puzzle_board(puzzle: str, round: str) -> dict:
    if "selected_letters" in st.session_state:
        selected_letters = st.session_state.selected_letters
    else:
        selected_letters = []

    # If round is "Bonus Round" then add R, S, T, L, N, and E to the selected letters
    if round == "Bonus Round":
        for letter in "RSTLNE":
            if letter not in st.session_state.selected_letters:
                st.session_state.selected_letters.append(letter)

    # Replace letters with underscores
    puzzle_with_underscores = "".join(["_" if c.isalpha() and c not in selected_letters else c for c in puzzle])

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


def check_letter(letter: str) -> None:
    if letter not in st.session_state.selected_letters:
        st.session_state.selected_letter = letter
        st.session_state.selected_letters.append(letter)

    set_check_letter(True)
    set_must_spin_wheel(True)

    st.rerun()


if __name__ == "__main__":
    # Load the audio files
    bankrupt_b64, buzzer_b64, ding_b64, new_puzzle_b64, solved_puzzle_b64 = load_audio_files()

    # Create a list of puzzle file names starting with season_1.json and ending with season_41.json
    puzzle_files = ["Season " + str(i) for i in range(1, 42)]
    puzzle_files.remove("Season 7")  # Season 7 is missing
    puzzle_files.remove("Season 12")  # Season 12 is missing
    puzzle_files.remove("Season 41")  # Season 41 is corrupt

    # Display the title
    st.sidebar.title("Glücksrad")

    # Display the season selection dropdown
    puzzle_file = st.sidebar.selectbox(label="Select a season", options=puzzle_files, on_change=reset_game)

    # Get a random puzzle
    category, puzzle, puzzle_letter_set, round = get_random_puzzle(puzzle_file)

    # Load the wheel prizes
    wheel_prizes = load_wheel_prizes()

    # Create a container to hold the Wheel of Fortune puzzle board image
    image_container = st.container()

    # Create a container to hold the host messages
    puzzle_message_container = st.container()

    if "check_letter" not in st.session_state:
        set_check_letter(False)

    if "contestant_score" not in st.session_state:
        add_amount_to_contenstant_score(0)

    solve_puzzle = st.chat_input("I'd like to solve the puzzle...", key="solve_puzzle")

    if solve_puzzle:
        if solve_puzzle.lower() == puzzle.lower():
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if letter not in st.session_state.selected_letters:
                    st.session_state.selected_letters.append(letter)
            st.balloons()
            puzzle_message_container.success("Congratulations!  You solved the puzzle!")
            play_audio(solved_puzzle_b64)
            set_puzzle_solved(True)
        else:
            puzzle_message_container.error("Sorry, that is not the correct answer.")
            play_audio(buzzer_b64)

    if st.session_state.check_letter:
        set_check_letter(False)

        selected_letter = st.session_state.selected_letter

        # Check if the selected letter is in the puzzle
        if selected_letter in puzzle:
            # Check if the puzzle has been solved
            if puzzle_letter_set.issubset(set(st.session_state.selected_letters)):
                st.balloons()
                puzzle_message_container.success("Congratulations!  You solved the puzzle!")
                play_audio(solved_puzzle_b64)
                set_puzzle_solved(True)
            else:
                puzzle_message_container.success("Correct!  There are " + str(puzzle.count(selected_letter)) + " " + selected_letter + "'s in the puzzle.")
                if selected_letter in ["A", "E", "I", "O", "U"]:
                    add_amount_to_contenstant_score(-250)
                for i in range(puzzle.count(selected_letter)):
                    if selected_letter not in ["A", "E", "I", "O", "U"]:
                        add_amount_to_contenstant_score(250)
                    play_audio(ding_b64)
                    # time.sleep(1.50)
        elif selected_letter.isalpha() and selected_letter not in puzzle:
            if selected_letter in ["A", "E", "I", "O", "U"]:
                add_amount_to_contenstant_score(-250)
            host_message = "Sorry, there are no " + selected_letter + "'s in the puzzle."
            puzzle_message_container.error(host_message)
            play_audio(buzzer_b64)

    st.sidebar.write("Puzzle from " + round)

    st.sidebar.write("Contestant Score: $" + str(st.session_state.contestant_score))

    # If the selected letters are not in the session state, assume this is the "first game" or a "new game"
    if "selected_letters" not in st.session_state:
        st.session_state.selected_letters = []

        set_check_letter(False)
        add_amount_to_contenstant_score(0)
        set_must_spin_wheel(True)
        set_has_enough_money_to_buy_vowel()
        set_puzzle_solved(False)

        # Play the new puzzle sound
        play_audio(new_puzzle_b64)
    else:
        set_has_enough_money_to_buy_vowel()

    # Display the spin wheel button
    if st.button("Spin Wheel", key="spin_wheel", disabled=st.session_state.puzzle_solved):
        set_must_spin_wheel(False)

        wheel_prize = get_wheel_prize(wheel_prizes)

    # Display the new puzzle button
    if st.sidebar.button("New Puzzle", key="new_puzzle"):
        reset_game()
        st.rerun()

    st.write(
        """<style>
            [data-testid="column"] {
                width: calc(14% - 1rem) !important;
                flex: 1 1 calc(14% - 1rem) !important;
                min-width: calc(14% - 1rem) !important;
            }
            </style>""",
        unsafe_allow_html=True,
    )

    # Display the consontant buttons
    st.write("Consonants")

    consonant_1, consonant_2, consonant_3, consonant_4, consonant_5, consonant_6, consonant_7 = st.columns(7)

    disable_consonants = st.session_state.must_spin_wheel or st.session_state.puzzle_solved

    if consonant_1.button(label="B", key="B", disabled="B" in st.session_state.selected_letters or disable_consonants):
        check_letter("B")

    if consonant_2.button(label="C", key="C", disabled="C" in st.session_state.selected_letters or disable_consonants):
        check_letter("C")

    if consonant_3.button(label="D", key="D", disabled="D" in st.session_state.selected_letters or disable_consonants):
        check_letter("D")

    if consonant_4.button(label="F", key="F", disabled="F" in st.session_state.selected_letters or disable_consonants):
        check_letter("F")

    if consonant_5.button(label="G", key="G", disabled="G" in st.session_state.selected_letters or disable_consonants):
        check_letter("G")

    if consonant_6.button(label="H", key="H", disabled="H" in st.session_state.selected_letters or disable_consonants):
        check_letter("H")

    if consonant_7.button(label="J", key="J", disabled="J" in st.session_state.selected_letters or disable_consonants):
        check_letter("J")

    if consonant_1.button(label="K", key="K", disabled="K" in st.session_state.selected_letters or disable_consonants):
        check_letter("K")

    if consonant_2.button(label="L", key="L", disabled="L" in st.session_state.selected_letters or disable_consonants):
        check_letter("L")

    if consonant_3.button(label="M", key="M", disabled="M" in st.session_state.selected_letters or disable_consonants):
        check_letter("M")

    if consonant_4.button(label="N", key="N", disabled="N" in st.session_state.selected_letters or disable_consonants):
        check_letter("N")

    if consonant_5.button(label="P", key="P", disabled="P" in st.session_state.selected_letters or disable_consonants):
        check_letter("P")

    if consonant_6.button(label="Q", key="Q", disabled="Q" in st.session_state.selected_letters or disable_consonants):
        check_letter("Q")

    if consonant_7.button(label="R", key="R", disabled="R" in st.session_state.selected_letters or disable_consonants):
        check_letter("R")

    if consonant_1.button(label="S", key="S", disabled="S" in st.session_state.selected_letters or disable_consonants):
        check_letter("S")

    if consonant_2.button(label="T", key="T", disabled="T" in st.session_state.selected_letters or disable_consonants):
        check_letter("T")

    if consonant_3.button(label="V", key="V", disabled="V" in st.session_state.selected_letters or disable_consonants):
        check_letter("V")

    if consonant_4.button(label="W", key="W", disabled="W" in st.session_state.selected_letters or disable_consonants):
        check_letter("W")

    if consonant_5.button(label="X", key="X", disabled="X" in st.session_state.selected_letters or disable_consonants):
        check_letter("X")

    if consonant_6.button(label="Y", key="Y", disabled="Y" in st.session_state.selected_letters or disable_consonants):
        check_letter("Y")

    if consonant_7.button(label="Z", key="Z", disabled="Z" in st.session_state.selected_letters or disable_consonants):
        check_letter("Z")

    # Display the vowel buttons
    st.write("Vowels")

    vowel_1, vowel_2, vowel_3, vowel_4, vowel_5, vowel_6, vowel_7 = st.columns(7)

    disable_vowels = not st.session_state.has_enough_month_to_buy_vowels or st.session_state.puzzle_solved

    if vowel_1.button(label="A", key="A", disabled="A" in st.session_state.selected_letters or disable_vowels):
        check_letter("A")

    if vowel_2.button(label="E", key="E", disabled="E" in st.session_state.selected_letters or disable_vowels):
        check_letter("E")

    if vowel_3.button(label="I", key="I", disabled="I" in st.session_state.selected_letters or disable_vowels):
        check_letter("I")

    if vowel_4.button(label="O", key="O", disabled="O" in st.session_state.selected_letters or disable_vowels):
        check_letter("O")

    if vowel_5.button(label="U", key="U", disabled="U" in st.session_state.selected_letters or disable_vowels):
        check_letter("U")

    # Generate the puzzle board
    puzzle_lines = generate_puzzle_board(puzzle, round)

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
