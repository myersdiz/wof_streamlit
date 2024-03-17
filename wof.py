import streamlit as st
import json, random, time


@st.cache_data
def getRandomPuzzle():
    with open("puzzles.json", "r") as f:
        # Load the puzzles from the JSON file
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
    st.session_state.last_selected_letter = letter

    if "last_selected_letter" in st.session_state:
        last_selected_letter = st.session_state.last_selected_letter

        if last_selected_letter in puzzle:
            if last_selected_letter not in st.session_state.selected_letters:
                st.session_state.selected_letters.append(last_selected_letter)

                # Check if the puzzle has been solved
                if puzzle_letter_set.issubset(set(st.session_state.selected_letters)):
                    st.balloons()
                    st.success("Congratulations!  You solved the puzzle!")
                else:
                    host_message = (
                        "Correct!  There are "
                        + str(puzzle.count(last_selected_letter))
                        + " "
                        + last_selected_letter
                        + "'s in the puzzle."
                    )
                    st.success(host_message)
                    st.toast(host_message)
        else:
            st.session_state.selected_letters.append(last_selected_letter)
            host_message = "Sorry, there are no " + last_selected_letter + "'s in the puzzle."
            st.error(host_message)
            st.toast(host_message)


if __name__ == "__main__":
    # Display the title
    st.title("Wheel of Disney")

    # Get a random puzzle
    category, puzzle, puzzle_letter_set = getRandomPuzzle()

    # Create a container to hold the Wheel of Fortune puzzle board (later in the script)
    container_1 = st.container()

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

    # Display the letter buttons
    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9 = st.columns(9)

    if "selected_letters" not in st.session_state:
        st.session_state.selected_letters = []

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

    # Start a new puzzle
    if st.button("New Puzzle", key="new_puzzle"):
        getRandomPuzzle.clear()
        st.session_state.selected_letters = []
        st.rerun()

    # Generate the puzzle board
    puzzle_lines = generatePuzzleBoard(puzzle)

    # Display the Wheel of Fortune puzzle board
    container_1.image(
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
