import streamlit as st
import altair as alt
import pandas as pd
from pf2e import calculations

def main():
    attack = st.sidebar.slider("Attack", 0, 50, 12)
    ac = st.sidebar.slider("AC", 0, 50, 20)

    mh_damage = float(st.sidebar.text_input("MH damage", "8.5"))
    oh_damage = float(st.sidebar.text_input("OH damage", "7.5"))
    mh_crit_damage = float(st.sidebar.text_input("MH crit damage", "34"))
    oh_crit_damage = float(st.sidebar.text_input("OH crit damage", "15"))

    mh_striking_damage = float(st.sidebar.text_input("MH striking damage", "13"))
    oh_striking_damage = float(st.sidebar.text_input("OH striking damage", "11"))
    mh_crit_striking_damage = float(st.sidebar.text_input("MH striking crit damage", "47"))
    oh_crit_striking_damage = float(st.sidebar.text_input("OH striking crit damage", "22"))

    vicious_damage = float(st.sidebar.text_input("Vicious damage", "4.5"))
    vicious_crit_damage = float(st.sidebar.text_input("Vicious crit damage", "13"))

    st.title("Vicious Strike vs Double Slice")

    hit_distritution_df = pd.DataFrame(
        [
            {"Strike": "Vicious", "Type": "Misses", "Count": calculations.misses(attack, ac)},
            {"Strike": "Vicious", "Type": "Hits", "Count": calculations.hits(attack, ac)},
            {"Strike": "Vicious", "Type": "Crits", "Count": calculations.crits(attack, ac)},
            {"Strike": "Double Slice (mh)", "Type": "Misses", "Count": calculations.misses(attack, ac)},
            {"Strike": "Double Slice (mh)", "Type": "Hits", "Count": calculations.hits(attack, ac)},
            {"Strike": "Double Slice (mh)", "Type": "Crits", "Count": calculations.crits(attack, ac)},
            {"Strike": "Double Slice (oh)", "Type": "Misses", "Count": calculations.misses(attack-2, ac)},
            {"Strike": "Double Slice (oh)", "Type": "Hits", "Count": calculations.hits(attack-2, ac)},
            {"Strike": "Double Slice (oh)", "Type": "Crits", "Count": calculations.crits(attack-2, ac)},
        ])
    hit_distribution_sort = ["Misses", "Hits", "Crits"]
    hit_distribution_chart = alt.Chart(hit_distritution_df).mark_bar().encode(
        x="Count", y="Strike",
        color=alt.Color(field="Type", sort=hit_distribution_sort).scale(domain=hit_distribution_sort, range=["#FF7F7F", "#7FC9FF", "#0094FF"]),
        order=alt.Order("color_Type_sort_index:Q")
    )

    st.header("Hit distribution")
    st.altair_chart(hit_distribution_chart, use_container_width=True)


    normalized_damage_df = pd.DataFrame(
        [
            {"Strike": "Vicious", "Type": "Hits MH", "Damage": calculations.hits(attack, ac) * (mh_damage + vicious_damage)},
            {"Strike": "Vicious", "Type": "Crits MH", "Damage": calculations.crits(attack, ac) * (mh_crit_damage + vicious_crit_damage)},
            {"Strike": "Double Slice", "Type": "Hits MH", "Damage": calculations.hits(attack, ac) * (mh_damage)},
            {"Strike": "Double Slice", "Type": "Crits MH", "Damage": calculations.crits(attack, ac) * (mh_crit_damage)},
            {"Strike": "Double Slice", "Type": "Hits OH", "Damage": calculations.hits(attack - 2, ac) * (oh_damage)},
            {"Strike": "Double Slice", "Type": "Crits OH", "Damage": calculations.crits(attack - 2, ac) * (oh_crit_damage)},
        ]
    )
    normalized_damage_sort = ["Hits MH", "Crits MH", "Hits OH", "Crits OH"]
    normalized_damage_chart = alt.Chart(normalized_damage_df).mark_bar().encode(
        x="Strike", y="Damage",
        color=alt.Color(field="Type", sort=normalized_damage_sort).scale(domain=normalized_damage_sort, range=["#7FC9FF", "#0094FF", "#7FFF8E", "#007F0E"]),
        order=alt.Order("color_Type_sort_index:Q")
    )

    st.header("Normalized Damage (non-striking)")
    st.altair_chart(normalized_damage_chart, use_container_width=True)


    normalized_striking_damage_df = pd.DataFrame(
        [
            {"Strike": "Vicious", "Type": "Hits MH", "Damage": calculations.hits(attack, ac) * (mh_striking_damage + vicious_damage)},
            {"Strike": "Vicious", "Type": "Crits MH", "Damage": calculations.crits(attack, ac) * (mh_crit_striking_damage + vicious_crit_damage)},
            {"Strike": "Double Slice", "Type": "Hits MH", "Damage": calculations.hits(attack, ac) * (mh_striking_damage)},
            {"Strike": "Double Slice", "Type": "Crits MH", "Damage": calculations.crits(attack, ac) * (mh_crit_striking_damage)},
            {"Strike": "Double Slice", "Type": "Hits OH", "Damage": calculations.hits(attack - 2, ac) * (oh_striking_damage)},
            {"Strike": "Double Slice", "Type": "Crits OH", "Damage": calculations.crits(attack - 2, ac) * (oh_crit_striking_damage)},
        ]
    )
    normalized_striking_damage_chart = alt.Chart(normalized_striking_damage_df).mark_bar().encode(
        x="Strike", y="Damage",
        color=alt.Color(field="Type", sort=normalized_damage_sort).scale(domain=normalized_damage_sort, range=["#7FC9FF", "#0094FF", "#7FFF8E", "#007F0E"]),
        order=alt.Order("color_Type_sort_index:Q")
    )

    st.header("Normalized Damage (striking)")
    st.altair_chart(normalized_striking_damage_chart, use_container_width=True)


if __name__ == "__main__":
    main()