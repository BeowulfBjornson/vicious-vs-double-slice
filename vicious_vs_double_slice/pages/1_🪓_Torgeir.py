import streamlit as st
from vicious_vs_double_slice.parameters import UserParameters
from vicious_vs_double_slice import plots


def main():
    st.set_page_config(
        page_title="Torgeir",
        page_icon="🪓",
    )
    
    st.title("Practical scenarios")
    st.markdown("These are concrete scenarios at specific levels vs an on-level creature")

    st.header("Lv 5")
    lv5_params = UserParameters(
        attack=16,
        ac=21,
        mh_damage="2d8+4",
        oh_damage="2d6+4",
        oh_penalty=-4,
        mh_crit_damage="5d12+8",
        oh_crit_damage="4d6+4",
        vicious_damage="1d8",
        vicious_crit_damage="2d12",
        enemy_resistance=5
    )
    plots.plot_hit_distribution(lv5_params)
    plots.plot_damage_distributions(lv5_params, with_resistance=True)

    st.header("Lv 8")
    lv8_params = UserParameters(
        attack=20,
        ac=28,
        mh_damage="2d8+8",
        oh_damage="2d6+7",
        oh_penalty=-4,
        mh_crit_damage="5d12+16",
        oh_crit_damage="4d6+14",
        vicious_damage="1d8",
        vicious_crit_damage="2d12",
        enemy_resistance=10
    )
    plots.plot_hit_distribution(lv8_params)
    plots.plot_damage_distributions(lv8_params, with_resistance=True)

    st.header("Lv 10")
    lv10_params = UserParameters(
        attack=23,
        ac=29,
        mh_damage="2d8+8",
        oh_damage="2d6+7",
        oh_penalty=-4,
        mh_crit_damage="5d12+16",
        oh_crit_damage="4d6+14",
        vicious_damage="2d8",
        vicious_crit_damage="4d12",
        enemy_resistance=10
    )
    plots.plot_hit_distribution(lv10_params)
    plots.plot_damage_distributions(lv10_params, with_resistance=True)

    st.header("Lv 12")
    lv12_params = UserParameters(
        attack=25,
        ac=31,
        mh_damage="3d8+8",
        oh_damage="3d6+7",
        oh_penalty=-4,
        mh_crit_damage="7d12+16",
        oh_crit_damage="6d6+14",
        vicious_damage="2d8",
        vicious_crit_damage="4d12",
        enemy_resistance=10
    )
    plots.plot_hit_distribution(lv12_params)
    plots.plot_damage_distributions(lv12_params, with_resistance=True)


if __name__ == "__main__":
    main()
