import streamlit as st
import base64, json, random


@st.cache_data
def loadAudioFiles():
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


def autoplay_audio(audio_file):
    audio_html = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{audio_file}" type="audio/mp3">
        </audio>
        """
    audio_container.write(audio_html, unsafe_allow_html=True, key="audio")


@st.cache_data
def getRandomPuzzle():
    # Load the puzzles from the JSON file
    with open("puzzles.json", "r") as f:
        puzzles = json.loads(f.read())

    # Get a random category
    category = random.choice(list(puzzles.keys()))

    # Get a random puzzle from the category and replace periods with nothing, commas with nothing, and hyphens with a space
    puzzle = random.choice(puzzles[category]).upper().replace(".", "").replace(",", "").replace(" - ", " ")

    # Remove everything but letters from the puzzle and convert it to a set
    puzzle_letter_set = set("".join([c for c in puzzle if c.isalpha()]))

    return (category, puzzle, puzzle_letter_set)


def generatePuzzleBoard(puzzle):
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
                if (
                    len(puzzle_lines["ln" + str(ln + 1)][0]) + len(puzzle_word) + 1
                    <= puzzle_lines["ln" + str(ln + 1)][2]
                ):
                    puzzle_lines["ln" + str(ln + 1)][0] += puzzle_word + " "
                    puzzle_lines["ln" + str(ln + 1)][1] += len(puzzle_word) + 1
                    ln_max = ln
                    break

    return puzzle_lines


def checkLetter(letter):
    if letter not in st.session_state.selected_letters:
        st.session_state.selected_letter = letter
        st.session_state.selected_letters.append(letter)

    st.rerun()


if __name__ == "__main__":
    buzzer_b64, ding_b64, new_puzzle_b64, solved_puzzle_b64 = loadAudioFiles()

    # Display the title
    st.title("Wheel of Disney")

    # Get a random puzzle
    category, puzzle, puzzle_letter_set = getRandomPuzzle()

    # Create a container to hold the Wheel of Fortune puzzle board image
    image_container = st.container()

    # Create a container to hold the host messages
    host_message_container = st.container()

    # Create an empty container to hold the audio
    audio_container = st.empty()

    st.write(
        """<style>
            [data-testid="column"] {
                width: calc(11% - 1rem) !important;
                flex: 1 1 calc(11% - 1rem) !important;
                min-width: calc(11% - 1rem) !important;
            }
           </style>""",
        unsafe_allow_html=True,
    )

    if "selected_letters" not in st.session_state:
        st.session_state.selected_letters = []

        # Play the new puzzle sound
        autoplay_audio(new_puzzle_b64)

    # Display the letter buttons
    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9 = st.columns(9)

    if col_1.button("A", key="A", disabled="A" in st.session_state.selected_letters):
        checkLetter("A")

    if col_2.button("B", key="B", disabled="B" in st.session_state.selected_letters):
        checkLetter("B")

    if col_3.button("C", key="C", disabled="C" in st.session_state.selected_letters):
        checkLetter("C")

    if col_4.button("D", key="D", disabled="D" in st.session_state.selected_letters):
        checkLetter("D")

    if col_5.button("E", key="E", disabled="E" in st.session_state.selected_letters):
        checkLetter("E")

    if col_6.button("F", key="F", disabled="F" in st.session_state.selected_letters):
        checkLetter("F")

    if col_7.button("G", key="G", disabled="G" in st.session_state.selected_letters):
        checkLetter("G")

    if col_8.button("H", key="H", disabled="H" in st.session_state.selected_letters):
        checkLetter("H")

    if col_9.button("I", key="I", disabled="I" in st.session_state.selected_letters):
        checkLetter("I")

    if col_1.button("J", key="J", disabled="J" in st.session_state.selected_letters):
        checkLetter("J")

    if col_2.button("K", key="K", disabled="K" in st.session_state.selected_letters):
        checkLetter("K")

    if col_3.button("L", key="L", disabled="L" in st.session_state.selected_letters):
        checkLetter("L")

    if col_4.button("M", key="M", disabled="M" in st.session_state.selected_letters):
        checkLetter("M")

    if col_5.button("N", key="N", disabled="N" in st.session_state.selected_letters):
        checkLetter("N")

    if col_6.button("O", key="O", disabled="O" in st.session_state.selected_letters):
        checkLetter("O")

    if col_7.button("P", key="P", disabled="P" in st.session_state.selected_letters):
        checkLetter("P")

    if col_8.button("Q", key="Q", disabled="Q" in st.session_state.selected_letters):
        checkLetter("Q")

    if col_9.button("R", key="R", disabled="R" in st.session_state.selected_letters):
        checkLetter("R")

    if col_1.button("S", key="S", disabled="S" in st.session_state.selected_letters):
        checkLetter("S")

    if col_2.button("T", key="T", disabled="T" in st.session_state.selected_letters):
        checkLetter("T")

    if col_3.button("U", key="U", disabled="U" in st.session_state.selected_letters):
        checkLetter("U")

    if col_4.button("V", key="V", disabled="V" in st.session_state.selected_letters):
        checkLetter("V")

    if col_5.button("W", key="W", disabled="W" in st.session_state.selected_letters):
        checkLetter("W")

    if col_6.button("X", key="X", disabled="X" in st.session_state.selected_letters):
        checkLetter("X")

    if col_7.button("Y", key="Y", disabled="Y" in st.session_state.selected_letters):
        checkLetter("Y")

    if col_8.button("Z", key="Z", disabled="Z" in st.session_state.selected_letters):
        checkLetter("Z")

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

    # Check if the selected letter is in the puzzle
    selected_letter = ""

    if "selected_letter" in st.session_state:
        selected_letter = st.session_state.selected_letter

    if selected_letter.isalpha() and selected_letter in puzzle:
        # Check if the puzzle has been solved
        if puzzle_letter_set.issubset(set(st.session_state.selected_letters)):
            st.balloons()
            host_message = "Congratulations!  You solved the puzzle!"
            host_message_container.success(host_message)
            autoplay_audio(solved_puzzle_b64)
        else:
            host_message = (
                "Correct!  There are "
                + str(puzzle.count(selected_letter))
                + " "
                + selected_letter
                + "'s in the puzzle."
            )
            host_message_container.success(host_message)
            autoplay_audio(ding_b64)
            # st.toast(host_message)
    elif selected_letter.isalpha() and selected_letter not in puzzle:
        host_message = "Sorry, there are no " + selected_letter + "'s in the puzzle."
        host_message_container.error(host_message)
        autoplay_audio(buzzer_b64)
        # st.toast(host_message)

    # Start a new puzzle
    if st.button("New Puzzle", key="new_puzzle"):
        getRandomPuzzle.clear()

        for key in st.session_state.keys():
            del st.session_state[key]

        st.rerun()
