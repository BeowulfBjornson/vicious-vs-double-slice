from dataclasses import dataclass
import streamlit as st


@dataclass
class UserParameters:
    attack: int
    ac: int
    mh_damage: str
    oh_damage: str
    oh_penalty: int
    mh_crit_damage: str
    oh_crit_damage: str
    vicious_damage: str
    vicious_crit_damage: str
    enemy_resistance: int

def get_user_parameters() -> UserParameters:
    return UserParameters(
        attack=st.sidebar.slider("Attack", 0, 50, 12),
        ac=st.sidebar.slider("AC", 0, 50, 20),
        mh_damage=st.sidebar.text_input("MH damage", "1d8+4"),
        oh_damage=st.sidebar.text_input("OH damage", "1d6+4"),
        oh_penalty=st.sidebar.slider("OH penality", -10, 0, -2),
        mh_crit_damage=st.sidebar.text_input("MH crit damage", "3d12+8"),
        oh_crit_damage=st.sidebar.text_input("OH crit damage", "2d6+8"),
        vicious_damage=st.sidebar.text_input("Vicious damage", "1d8"),
        vicious_crit_damage=st.sidebar.text_input("Vicious crit damage", "2d12"),
        enemy_resistance=st.sidebar.slider("Enemy Resistance", 0, 50, 10)
    )