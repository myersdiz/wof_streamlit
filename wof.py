import streamlit as st
import pandas as pd
import base64, json, random, time


def setCheckLetter(checkLetter: bool) -> None:
    if "CheckLetter" not in st.session_state:
        st.session_state.CheckLetter = checkLetter

    st.session_state.CheckLetter = checkLetter


def addAmountToContestantScore(addPrizeAmount: int) -> None:
    if "ContestantScore" not in st.session_state:
        st.session_state.ContestantScore = addPrizeAmount

    st.session_state.ContestantScore += addPrizeAmount


def setMustSpinWheel(MustSpinWheel: bool) -> None:
    if "MustSpinWheel" not in st.session_state:
        st.session_state.MustSpinWheel = True

    st.session_state.MustSpinWheel = MustSpinWheel


def setHasEnoughMoneyToBuyVowel() -> None:
    if "HasEnoughMoneyToBuyVowel" not in st.session_state:
        st.session_state.HasEnoughMoneyToBuyVowel = False

    if st.session_state.ContestantScore >= 250:
        st.session_state.HasEnoughMoneyToBuyVowel = True
    else:
        st.session_state.HasEnoughMoneyToBuyVowel = False


def setPuzzleSolved(PuzzleSolved: bool) -> None:
    if "PuzzleSolved" not in st.session_state:
        st.session_state.PuzzleSolved = False

    st.session_state.PuzzleSolved = PuzzleSolved


@st.cache_data
def loadAudioFiles() -> tuple[str, str, str, str]:
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

    return buzzer_b64, ding_b64, new_puzzle_b64, solved_puzzle_b64


def autoplay_audio(audio_file) -> None:
    random_str = str(random.random())

    audio_html = f"""
        <audio class="{random_str}" autoplay="true">
        <source src="data:audio/mp3;base64,{audio_file}" type="audio/mp3">
        </audio>
        """
    st.components.v1.html(audio_html, width=0, height=0, scrolling=False)


@st.cache_data
def getRandomPuzzle(puzzle_file) -> tuple[str, str, set]:
    # Load the puzzles from the JSON file
    with open("puzzle_parser/" + puzzle_file, "r") as f:
        puzzles = json.loads(f.read())

    # Convert dictionary puzzles to Pandas DataFrame
    df_puzzles = pd.DataFrame(puzzles)

    # Pick one random row from the Pandas DataFrame
    df_puzzles = df_puzzles.sample(n=1)

    category = df_puzzles["CATEGORY"].values[0]

    puzzle = df_puzzles["PUZZLE"].values[0]

    # Remove everything but letters from the puzzle and convert it to a set
    puzzle_letter_set = set("".join([c for c in puzzle if c.isalpha()]))

    return (category, puzzle, puzzle_letter_set)


def generatePuzzleBoard(puzzle) -> dict:
    if "selected_letters" in st.session_state:
        selected_letters = st.session_state.selected_letters
    else:
        selected_letters = []

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


def checkLetter(letter):
    if letter not in st.session_state.selected_letters:
        st.session_state.selected_letter = letter
        st.session_state.selected_letters.append(letter)

    setCheckLetter(True)
    setMustSpinWheel(True)

    st.rerun()


if __name__ == "__main__":
    # Load the audio files
    buzzer_b64, ding_b64, new_puzzle_b64, solved_puzzle_b64 = loadAudioFiles()

    # Create a list of puzzle file names starting with season_1.json and ending with season_41.json
    puzzle_files = ["season_" + str(i) + ".json" for i in range(1, 42)]

    puzzle_file = st.sidebar.selectbox("Select Season", puzzle_files)

    # Display the title
    st.title("Glücksrad")

    # Get a random puzzle
    category, puzzle, puzzle_letter_set = getRandomPuzzle(puzzle_file)

    # Create a container to hold the Wheel of Fortune puzzle board image
    image_container = st.container()

    # Create a container to hold the host messages
    host_message_container = st.container()

    # If the selected letters are not in the session state, assume this is the "first game" or a "new game"
    if "selected_letters" not in st.session_state:
        st.session_state.selected_letters = []

        setCheckLetter(False)
        addAmountToContestantScore(0)
        setMustSpinWheel(True)
        setHasEnoughMoneyToBuyVowel()
        setPuzzleSolved(False)

        # Play the new puzzle sound
        autoplay_audio(new_puzzle_b64)
    else:
        setHasEnoughMoneyToBuyVowel()

    if st.session_state.MustSpinWheel:
        host_message_container.warning("You must spin the wheel before selecting a letter.")
    else:
        host_message_container.success("You may now select a letter.")

    if st.button("Spin Wheel", key="spin_wheel"):
        setMustSpinWheel(False)

    if st.sidebar.button("New Puzzle", key="new_puzzle"):
        getRandomPuzzle.clear()

        for key in st.session_state.keys():
            del st.session_state[key]

        st.rerun()

#    st.write(
#        """<style>
#            [data-testid="column"] {
#                width: calc(14% - 1rem) !important;
#                flex: 1 1 calc(14% - 1rem) !important;
#                min-width: calc(14% - 1rem) !important;
#            }
#            </style>""",
#        unsafe_allow_html=True,
#    )

    consonants = st.container()

    # Display the consontant buttons
    consonants.write("Consonants")

    consonant_1, consonant_2, consonant_3, consonant_4, consonant_5, consonant_6, consonant_7 = consonants.columns(7)

    if consonant_1.button(
        "B",
        key="B",
        disabled="B" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("B")

    if consonant_2.button(
        "C",
        key="C",
        disabled="C" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("C")

    if consonant_3.button(
        "D",
        key="D",
        disabled="D" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("D")

    if consonant_4.button(
        "F",
        key="F",
        disabled="F" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("F")

    if consonant_5.button(
        "G",
        key="G",
        disabled="G" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("G")

    if consonant_6.button(
        "H",
        key="H",
        disabled="H" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("H")

    if consonant_7.button(
        "J",
        key="J",
        disabled="J" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("J")

    if consonant_1.button(
        "K",
        key="K",
        disabled="K" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("K")

    if consonant_2.button(
        "L",
        key="L",
        disabled="L" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("L")

    if consonant_3.button(
        "M",
        key="M",
        disabled="M" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("M")

    if consonant_4.button(
        "N",
        key="N",
        disabled="N" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("N")

    if consonant_5.button(
        "P",
        key="P",
        disabled="P" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("P")

    if consonant_6.button(
        "Q",
        key="Q",
        disabled="Q" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("Q")

    if consonant_7.button(
        "R",
        key="R",
        disabled="R" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("R")

    if consonant_1.button(
        "S",
        key="S",
        disabled="S" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("S")

    if consonant_2.button(
        "T",
        key="T",
        disabled="T" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("T")

    if consonant_3.button(
        "V",
        key="V",
        disabled="V" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("V")

    if consonant_4.button(
        "W",
        key="W",
        disabled="W" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("W")

    if consonant_5.button(
        "X",
        key="X",
        disabled="X" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("X")

    if consonant_6.button(
        "Y",
        key="Y",
        disabled="Y" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("Y")

    if consonant_7.button(
        "Z",
        key="Z",
        disabled="Z" in st.session_state.selected_letters or st.session_state.MustSpinWheel or st.session_state.PuzzleSolved,
    ):
        checkLetter("Z")

    vowels = st.container()

    # Display the consontant buttons
    vowels.write("Vowels")

    vowel_1, vowel_2, vowel_3, vowel_4, vowel_5, vowel_6, vowel_7 = vowels.columns(7)

    if vowel_1.button(
        "A",
        key="A",
        disabled="A" in st.session_state.selected_letters or not st.session_state.HasEnoughMoneyToBuyVowel or st.session_state.PuzzleSolved,
    ):
        checkLetter("A")

    if vowel_2.button(
        "E",
        key="E",
        disabled="E" in st.session_state.selected_letters or not st.session_state.HasEnoughMoneyToBuyVowel or st.session_state.PuzzleSolved,
    ):
        checkLetter("E")

    if vowel_3.button(
        "I",
        key="I",
        disabled="I" in st.session_state.selected_letters or not st.session_state.HasEnoughMoneyToBuyVowel or st.session_state.PuzzleSolved,
    ):
        checkLetter("I")

    if vowel_4.button(
        "O",
        key="O",
        disabled="O" in st.session_state.selected_letters or not st.session_state.HasEnoughMoneyToBuyVowel or st.session_state.PuzzleSolved,
    ):
        checkLetter("O")

    if vowel_5.button(
        "U",
        key="U",
        disabled="U" in st.session_state.selected_letters or not st.session_state.HasEnoughMoneyToBuyVowel or st.session_state.PuzzleSolved,
    ):
        checkLetter("U")

    # Generate the puzzle board
    puzzle_lines = generatePuzzleBoard(puzzle)

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

    if st.session_state.CheckLetter:
        setCheckLetter(False)

        selected_letter = st.session_state.selected_letter

        # Check if the selected letter is in the puzzle
        if selected_letter in puzzle:
            # Check if the puzzle has been solved
            if puzzle_letter_set.issubset(set(st.session_state.selected_letters)):
                st.balloons()
                host_message = "Congratulations!  You solved the puzzle!"
                host_message_container.success(host_message)
                autoplay_audio(solved_puzzle_b64)
                setPuzzleSolved(True)
            else:
                host_message = "Correct!  There are " + str(puzzle.count(selected_letter)) + " " + selected_letter + "'s in the puzzle."
                host_message_container.success(host_message)
                if selected_letter in ["A", "E", "I", "O", "U"]:
                    addAmountToContestantScore(-250)
                for i in range(puzzle.count(selected_letter)):
                    if selected_letter not in ["A", "E", "I", "O", "U"]:
                        addAmountToContestantScore(250)
                    autoplay_audio(ding_b64)
                    time.sleep(1.50)
                # st.toast(host_message)
                # st.rerun()
        elif selected_letter.isalpha() and selected_letter not in puzzle:
            if selected_letter in ["A", "E", "I", "O", "U"]:
                addAmountToContestantScore(-250)
            host_message = "Sorry, there are no " + selected_letter + "'s in the puzzle."
            host_message_container.error(host_message)
            autoplay_audio(buzzer_b64)
            # st.toast(host_message)

    st.sidebar.write("Contestant Score: $" + str(st.session_state.ContestantScore))
