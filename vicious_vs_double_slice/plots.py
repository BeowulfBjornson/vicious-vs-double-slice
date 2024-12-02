from functools import partial

import altair as alt
import pandas as pd
import streamlit as st
from dyce import H
from dyce.evaluation import HResult, foreach as dyce_foreach, expandable

from vicious_vs_double_slice.parameters import UserParameters
from vicious_vs_double_slice.pf2e import calculations, dice, degrees

_HISTOGRAM_BIN_SIZE = 1


def plot_normalized_damage(user_parameters: UserParameters) -> None:
    mh_damage_avg = dice.average_value(user_parameters.mh_damage)
    oh_damage_avg = dice.average_value(user_parameters.oh_damage)
    mh_crit_damage_avg = dice.average_value(user_parameters.mh_crit_damage)
    oh_crit_damage_avg = dice.average_value(user_parameters.oh_crit_damage)
    vicious_damage_avg = dice.average_value(user_parameters.vicious_damage)
    vicious_crit_damage_avg = dice.average_value(user_parameters.vicious_crit_damage)

    normalized_damage_df = pd.DataFrame(
        [
            {"Strike": "Vicious Swing", "Type": "Hits MH", "Damage": calculations.hits(user_parameters.attack, user_parameters.ac) * (mh_damage_avg + vicious_damage_avg)},
            {"Strike": "Vicious Swing", "Type": "Crits MH", "Damage": calculations.crits(user_parameters.attack, user_parameters.ac) * (mh_crit_damage_avg + vicious_crit_damage_avg)},
            {"Strike": "Double Slice", "Type": "Hits MH", "Damage": calculations.hits(user_parameters.attack, user_parameters.ac) * (mh_damage_avg)},
            {"Strike": "Double Slice", "Type": "Crits MH", "Damage": calculations.crits(user_parameters.attack, user_parameters.ac) * (mh_crit_damage_avg)},
            {"Strike": "Double Slice", "Type": "Hits OH", "Damage": calculations.hits(user_parameters.attack + user_parameters.oh_penalty, user_parameters.ac) * (oh_damage_avg)},
            {"Strike": "Double Slice", "Type": "Crits OH", "Damage": calculations.crits(user_parameters.attack + user_parameters.oh_penalty, user_parameters.ac) * (oh_crit_damage_avg)},
        ]
    )
    normalized_damage_sort = ["Hits MH", "Crits MH", "Hits OH", "Crits OH"]
    normalized_damage_chart = alt.Chart(normalized_damage_df).mark_bar().encode(
        x="Strike", y="Damage",
        color=alt.Color(field="Type", sort=normalized_damage_sort).scale(domain=normalized_damage_sort, range=["#7FC9FF", "#0094FF", "#7FFF8E", "#007F0E"]),
        order=alt.Order("color_Type_sort_index:Q")
    )

    st.markdown("### Normalized Damage, no resistance applied")
    st.markdown("This is a misleading 'metric', kept here for historical purposes")
    st.altair_chart(normalized_damage_chart, use_container_width=True)

def plot_hit_distribution(user_parameters: UserParameters) -> None:
    hit_distritution_df = pd.DataFrame(
        [
            {"Strike": "Vicious Swing", "Type": "Misses", "Count": calculations.misses(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Vicious Swing", "Type": "Hits", "Count": calculations.hits(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Vicious Swing", "Type": "Crits", "Count": calculations.crits(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Double Slice (mh)", "Type": "Misses", "Count": calculations.misses(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Double Slice (mh)", "Type": "Hits", "Count": calculations.hits(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Double Slice (mh)", "Type": "Crits", "Count": calculations.crits(user_parameters.attack, user_parameters.ac)},
            {"Strike": "Double Slice (oh)", "Type": "Misses", "Count": calculations.misses(user_parameters.attack + user_parameters.oh_penalty, user_parameters.ac)},
            {"Strike": "Double Slice (oh)", "Type": "Hits", "Count": calculations.hits(user_parameters.attack + user_parameters.oh_penalty, user_parameters.ac)},
            {"Strike": "Double Slice (oh)", "Type": "Crits", "Count": calculations.crits(user_parameters.attack + user_parameters.oh_penalty, user_parameters.ac)},
        ])
    hit_distribution_sort = ["Misses", "Hits", "Crits"]
    hit_distribution_chart = alt.Chart(hit_distritution_df).mark_bar().encode(
        x="Count", y="Strike",
        color=alt.Color(field="Type", sort=hit_distribution_sort).scale(domain=hit_distribution_sort, range=["#FF7F7F", "#7FC9FF", "#0094FF"]),
        order=alt.Order("color_Type_sort_index:Q")
    )
    st.markdown("### Hit distribution")
    st.altair_chart(hit_distribution_chart, use_container_width=True)

def plot_damage_distributions(user_parameters: UserParameters, with_resistance: bool) -> None:
    mh_damage_dyce = dice.to_dyce_expression(user_parameters.mh_damage)
    oh_damage_dyce = dice.to_dyce_expression(user_parameters.oh_damage)
    mh_crit_damage_dyce = dice.to_dyce_expression(user_parameters.mh_crit_damage)
    oh_crit_damage_dyce = dice.to_dyce_expression(user_parameters.oh_crit_damage)
    vicious_damage_dyce = dice.to_dyce_expression(user_parameters.vicious_damage)
    vicious_crit_damage_dyce = dice.to_dyce_expression(user_parameters.vicious_crit_damage)

    @expandable
    def negative_is_zero(h_result: HResult):
        if h_result.outcome < 0:
            return 0.0
        else:
            return h_result.outcome

    def expected_damage(damage: H, critical_damage: H, attack_modifier: int, resistance: int, d20: HResult):
        degree = degrees.outcome(d20.outcome, user_parameters.attack + attack_modifier, user_parameters.ac)
        if degree == degrees.DegreeOfSuccess.CRITICAL_SUCCESS:
             return critical_damage - resistance
        elif degree == degrees.DegreeOfSuccess.SUCCESS:
             return damage - resistance
        else:
            return 0.0

    d20 = H(20)
    vicious_distribution = negative_is_zero(
        dyce_foreach(
            partial(expected_damage,
                    damage=mh_damage_dyce + vicious_damage_dyce,
                    critical_damage=mh_crit_damage_dyce + vicious_crit_damage_dyce,
                    attack_modifier=0,
                    resistance=user_parameters.enemy_resistance if with_resistance else 0),
            d20=d20))
    double_slice_mh_distribution = dyce_foreach(
        partial(expected_damage,
                damage=mh_damage_dyce,
                critical_damage=mh_crit_damage_dyce,
                attack_modifier=0,
                resistance=0),
        d20=d20)
    double_slice_oh_distribution = dyce_foreach(
        partial(expected_damage,
                damage=oh_damage_dyce,
                critical_damage=oh_crit_damage_dyce,
                attack_modifier=user_parameters.oh_penalty,
                resistance=0),
        d20=d20)
    double_slice_distribution = double_slice_mh_distribution + double_slice_oh_distribution
    if with_resistance:
        double_slice_distribution = double_slice_distribution - user_parameters.enemy_resistance
    double_slice_distribution = negative_is_zero(double_slice_distribution)

    values, frequency = vicious_distribution.distribution_xy()
    vicious_distribution_df = pd.DataFrame({"Damage": values, "Frequency": frequency})
    vicious_distribution_histogram = alt.Chart(vicious_distribution_df).mark_bar().encode(
        x=alt.X("Damage:Q", bin=alt.Bin(step=_HISTOGRAM_BIN_SIZE), title="Damage"),
        y=alt.Y("Frequency", title="Frequency"),
        tooltip=["Damage:Q", "Frequency:Q"]
    )
    st.markdown(f"### Damage Distribution for Vicious Swing, {'' if with_resistance else 'no '}resistance applied")
    st.markdown(f"* Mean: {round(vicious_distribution.mean(), 2)}\n* StDev: {round(vicious_distribution.stdev(), 2)}")
    st.altair_chart(vicious_distribution_histogram, use_container_width=True)

    values, frequency = double_slice_distribution.distribution_xy()
    double_slice_distribution_df = pd.DataFrame({"Damage": values, "Frequency": frequency})
    double_slice_distribution_histogram = alt.Chart(double_slice_distribution_df).mark_bar().encode(
        x=alt.X("Damage:Q", bin=alt.Bin(step=_HISTOGRAM_BIN_SIZE), title="Damage"),
        y=alt.Y("Frequency", title="Frequency"),
        tooltip=["Damage:Q", "Frequency:Q"]
    )
    st.markdown(f"### Damage Distribution for Double Slice, {'' if with_resistance else 'no '}resistance applied")
    st.markdown(f"* Mean: {round(double_slice_distribution.mean(), 2)}\n* StDev: {round(double_slice_distribution.stdev(), 2)}")
    st.altair_chart(double_slice_distribution_histogram, use_container_width=True)
