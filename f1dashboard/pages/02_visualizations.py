"""
In data visualizations the following visualizations are shown:
- A bar chart with the top 5 drivers with the most points
- A line chart with the points of Lewis Hamilton over the years
"""

import altair as alt
import pandas as pd
import streamlit as st

from f1dashboard.advanced.state import F1State
from f1dashboard.advanced.queries import F1Queries


class DataVisualizations:
    def __init__(self) -> None:
        self.f1_state = F1State()
        self.f1_queries = F1Queries()

    def top_drivers(self):
        """Create a bar chart with the top 5 drivers."""

        st.subheader("Top 5 Drivers")

        top_driver_data = self.f1_state.get_query_result(
            "top_drivers"
        )

        st.dataframe(top_driver_data)

        bar_chart = (
            alt.Chart(top_driver_data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "driver_name:N",
                    sort="-y",
                    title="Driver"
                ),
                y=alt.Y(
                    "total_points:Q",
                    title="Total Points"
                ),
                tooltip=[
                    alt.Tooltip(
                        "driver_name:N",
                        title="Driver"
                    ),
                    alt.Tooltip(
                        "total_points:Q",
                        title="Points"
                    ),
                ],
            )
        )

        st.altair_chart(
            bar_chart,
            use_container_width=True
        )

    def lewis_hamilton_over_the_years(self):
        """Create a line chart with Lewis Hamilton's points."""

        st.subheader("Lewis Hamilton over the years")

        lewis_years = self.f1_state.get_query_result(
            "lewis_over_the_years"
        )

        lewis_years["year"] = pd.to_datetime(
            lewis_years["year"],
            format="%Y"
        )

        line_chart = (
            alt.Chart(lewis_years)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "year:T",
                    title="Year"
                ),
                y=alt.Y(
                    "total_points:Q",
                    title="Total Points"
                ),
                tooltip=[
                    alt.Tooltip(
                        "year:T",
                        title="Year",
                        format="%Y"
                    ),
                    alt.Tooltip(
                        "total_points:Q",
                        title="Points"
                    ),
                ],
            )
        )

        st.altair_chart(
            line_chart,
            use_container_width=True
        )


if __name__ == "__main__":
    st.title("Data visualizations")

    data_visualizations = DataVisualizations()

    data_visualizations.top_drivers()

    data_visualizations.lewis_hamilton_over_the_years()
