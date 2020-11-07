from models.dice import Proba
import streamlit as st
from util.checks import check_value


def number_faces(face: int, default_value: int, dice_id: int) -> int:
    return st.sidebar.number_input(
        f"{face} GOLD",
        value=default_value,
        min_value=0,
        max_value=6,
        key=f"{dice_id}_{face}",
    )


possible_gold_faces = [1, 2, 3, 4, 6]

st.sidebar.write("# Dice 1")
dice_1 = {}
for face in possible_gold_faces:
    value = number_faces(face, 5 if face == 1 else 0, 1)
    dice_1[value] = face
proba_1 = Proba(dice_1)

st.sidebar.write("# Dice 2")
dice_2 = {}
for face in possible_gold_faces:
    value = number_faces(face, 4 if face == 1 else 0, 2)
    dice_2[value] = face
proba_2 = Proba(dice_2)


roll = proba_1 + proba_2

number_turns = st.number_input(
    "Number of turns left", min_value=0.0, max_value=9.0, step=0.5, value=1.0
)
check_value(number_turns % 0.5 == 0, "Please choose an int or half value")
extra_rolls = st.number_input("Both dices extra rolls", min_value=0, value=0)

extra_rolls_dice_1 = st.number_input("Dice 1 extra rolls", min_value=0, value=0)
extra_rolls_dice_2 = st.number_input("Dice 2 extra rolls", min_value=0, value=0)


probas = roll * int((4 * number_turns) + extra_rolls)
if extra_rolls_dice_1:
    probas += proba_1 * extra_rolls_dice_1
if extra_rolls_dice_2:
    probas += proba_2 * extra_rolls_dice_2


check_value(number_turns % 0.5 == 0, "Please choose a multiple of 0.5 for number of turns")

check_value(
    any(
        rolls > 0
        for rolls in (number_turns, extra_rolls, extra_rolls_dice_1, extra_rolls_dice_2)
    ),
    "Cannot compute expected income without any rolls",
)

cum_sum = probas.inverse_cum_sum()
show = st.checkbox("Show detailed probabilities")
if show:
    st.write(cum_sum)
st.line_chart(cum_sum)
