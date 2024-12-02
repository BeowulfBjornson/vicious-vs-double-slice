import streamlit as st


from vicious_vs_double_slice.parameters import get_user_parameters
from vicious_vs_double_slice import plots


def main():    
    st.set_page_config(
        page_title="Playground",
        page_icon="🛝",
    )
    user_parameters = get_user_parameters()

    st.title("Vicious Swing vs Double Slice")

    st.markdown(
        """
        I wanted to see which feat between Vicious Swing and Double Slice was better for a sword-and-board fighter in Pathfinder 2E
        for the strict purpose of fighting enemies with resistances (using either a bludgeoning weapon or a slashing weapon with a
        shield augmentation giving Versatile S so the double slice damage is of a single type).

        Turns out, Pathfinder's four degrees of success makes it very complicated to model mathematically -- certainly beyond my skills
        in statistics. The result: this totally overkill project.

        This page is a playground where one can see how the different parameters affect the outcome
    """)

    plots.plot_hit_distribution(user_parameters)

    plots.plot_normalized_damage(user_parameters)

    plots.plot_damage_distributions(user_parameters, with_resistance=False)

    plots.plot_damage_distributions(user_parameters, with_resistance=True)

if __name__ == "__main__":
    main()