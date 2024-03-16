import streamlit as st
import json, random


@st.cache_data
def getRandomPuzzle():
    with open("puzzles.json", "r") as f:
        puzzles = json.loads(f.read())

        category = random.choice(list(puzzles.keys()))
        puzzle = random.choice(puzzles[category]).upper()

        return (category, puzzle)


def generatePuzzleBoard(puzzle):
    # Replace periods with nothing
    puzzle = puzzle.replace(".", "").replace(",", "").replace(" - ", " ")

    # Replace letters with underscores
    puzzle_with_underscores = "".join(
        ["_" if c.isalpha() and c not in st.session_state.selected_letters else c for c in puzzle]
    )

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
    if letter in puzzle:
        if letter not in st.session_state.selected_letters:
            st.session_state.selected_letters.append(letter)
            host_message = "Correct!  There are " + str(puzzle.count(letter)) + " " + letter + "'s in the puzzle."
            st.success(host_message)
            st.toast(host_message)
    else:
        st.session_state.selected_letters.append(letter)
        host_message = "Sorry, there are no " + letter + "'s in the puzzle."
        st.error(host_message)
        st.toast(host_message)

    st.rerun()


if "selected_letters" not in st.session_state:
    st.session_state.selected_letters = []

# Display the title
st.title("Wheel of Disney")

# Get a random puzzle
category, puzzle = getRandomPuzzle()

# Generate the puzzle board
puzzle_lines = generatePuzzleBoard(puzzle)

# Display the Wheel of Fortune puzzle board
st.image(
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

# Display the letter buttons
col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10 = st.columns(10)

button_a = col_1.button("A", key="A", disabled="A" in st.session_state.selected_letters)
button_b = col_2.button("B", key="B", disabled="B" in st.session_state.selected_letters)
button_c = col_3.button("C", key="C", disabled="C" in st.session_state.selected_letters)
button_d = col_4.button("D", key="D", disabled="D" in st.session_state.selected_letters)
button_e = col_5.button("E", key="E", disabled="E" in st.session_state.selected_letters)
button_f = col_6.button("F", key="F", disabled="F" in st.session_state.selected_letters)
button_g = col_7.button("G", key="G", disabled="G" in st.session_state.selected_letters)
button_h = col_8.button("H", key="H", disabled="H" in st.session_state.selected_letters)
button_i = col_9.button("I", key="I", disabled="I" in st.session_state.selected_letters)
button_j = col_10.button("J", key="J", disabled="J" in st.session_state.selected_letters)

button_k = col_1.button("K", key="K", disabled="K" in st.session_state.selected_letters)
button_l = col_2.button("L", key="L", disabled="L" in st.session_state.selected_letters)
button_m = col_3.button("M", key="M", disabled="M" in st.session_state.selected_letters)
button_n = col_4.button("N", key="N", disabled="N" in st.session_state.selected_letters)
button_o = col_5.button("O", key="O", disabled="O" in st.session_state.selected_letters)
button_p = col_6.button("P", key="P", disabled="P" in st.session_state.selected_letters)
button_q = col_7.button("Q", key="Q", disabled="Q" in st.session_state.selected_letters)
button_r = col_8.button("R", key="R", disabled="R" in st.session_state.selected_letters)
button_s = col_9.button("S", key="S", disabled="S" in st.session_state.selected_letters)
button_t = col_10.button("T", key="T", disabled="T" in st.session_state.selected_letters)

button_u = col_1.button("U", key="U", disabled="U" in st.session_state.selected_letters)
button_v = col_2.button("V", key="V", disabled="V" in st.session_state.selected_letters)
button_w = col_3.button("W", key="W", disabled="W" in st.session_state.selected_letters)
button_x = col_4.button("X", key="X", disabled="X" in st.session_state.selected_letters)
button_y = col_5.button("Y", key="Y", disabled="Y" in st.session_state.selected_letters)
button_z = col_6.button("Z", key="Z", disabled="Z" in st.session_state.selected_letters)

# Check if a letter button was clicked
if button_a:
    checkLetter("A")

if button_b:
    checkLetter("B")

if button_c:
    checkLetter("C")

if button_d:
    checkLetter("D")

if button_e:
    checkLetter("E")

if button_f:
    checkLetter("F")

if button_g:
    checkLetter("G")

if button_h:
    checkLetter("H")

if button_i:
    checkLetter("I")

if button_j:
    checkLetter("J")

if button_k:
    checkLetter("K")

if button_l:
    checkLetter("L")

if button_m:
    checkLetter("M")

if button_n:
    checkLetter("N")

if button_o:
    checkLetter("O")

if button_p:
    checkLetter("P")

if button_q:
    checkLetter("Q")

if button_r:
    checkLetter("R")

if button_s:
    checkLetter("S")

if button_t:
    checkLetter("T")

if button_u:
    checkLetter("U")

if button_v:
    checkLetter("V")

if button_w:
    checkLetter("W")

if button_x:
    checkLetter("X")

if button_y:
    checkLetter("Y")

if button_z:
    checkLetter("Z")

# Check if the puzzle has been solved
puzzle_set = set(puzzle)

if " " in puzzle_set:
    puzzle_set.remove(" ")

if puzzle_set.issubset(set(st.session_state.selected_letters)):
    st.balloons()
    st.success("Congratulations!  You solved the puzzle!")

# Start a new puzzle
if st.button("New Puzzle"):
    getRandomPuzzle.clear()
    st.session_state.selected_letters = []
    st.rerun()
