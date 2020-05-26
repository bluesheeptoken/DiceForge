from models.dice import Proba
import streamlit as st


def gold_dice_definition(label: str, default: str):
    gold_faces = st.text_input(label, value=default)
    return eval(gold_faces)

def graph_resources(resource: str):
    st.write(f"# {resource}")
    number_turns = st.number_input(f"Number of turns ? ({resource})", min_value=1, max_value=9)
    if resource == "GOLD":
        dice1 = Proba.from_list(gold_dice_definition("Dice 1 gold faces", "[1, 1, 1, 1, 1, 0]"))
        dice2 = Proba.from_list(gold_dice_definition("Dice 2 gold faces", "[1, 1, 1, 1, 0, 0]"))
    elif resource == "RED":
        dice1 = Proba.from_list(gold_dice_definition("Dice 1 red faces", "[1, 0, 0, 0, 0, 0]"))
        dice2 = Proba.from_list(gold_dice_definition("Dice 2 red faces", "[0, 0, 0, 0, 0, 0]"))
    elif resource == "BLUE":
        dice1 = Proba.from_list(gold_dice_definition("Dice 1 blue faces", "[0, 0, 0, 0, 0, 0]"))
        dice2 = Proba.from_list(gold_dice_definition("Dice 2 blue faces", "[1, 0, 0, 0, 0, 0]"))


    turn = (dice1 + dice2) * 4

    cum_sum = (turn * number_turns).inverse_cum_sum()
    show = st.checkbox(f"Show detailed cumulative sum for {resource}")
    if show:
        st.write(cum_sum)
    st.line_chart(cum_sum)

graph_resources("GOLD")
graph_resources("RED")
graph_resources("BLUE")
