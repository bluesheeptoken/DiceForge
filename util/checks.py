from typing import NoReturn
import streamlit as st


def check_value(predicate: bool, error_message: str) -> NoReturn:
    if not predicate:
        st.write(error_message)
        raise ValueError(error_message)
