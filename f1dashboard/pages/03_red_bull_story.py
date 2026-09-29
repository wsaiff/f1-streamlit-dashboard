import altair as alt
import pandas as pd
import streamlit as st

from f1dashboard.advanced.state import F1State


class RedBullStory:
    def __init__(self) -> None:
        self.f1_state = F1State()

    def points_over_the_years(self):
        st.header("📈 How has Red Bull performed over the years?")

        points = self.f1_state.get_query_result(
            "red_bull_points_over_the_years"
        )

        points["year"] = pd.to_datetime(
            points["year"],
            format="%Y"
        )

        chart = (
            alt.Chart(points)
            .mark_line(
                point=True,
                strokeWidth=3
            )
            .encode(
                x=alt.X(
                    "year:T",
                    title="Season"
                ),
                y=alt.Y(
                    "total_points:Q",
                    title="Constructor Points"
                ),
                tooltip=[
                    alt.Tooltip(
                        "year:T",
                        title="Season",
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
            chart,
            use_container_width=True
        )

        st.markdown(
            """
            This chart shows how Red Bull's constructor points
            have changed across Formula 1 seasons.

            The historical trend helps us understand whether the
            team entered 2019 with a strong recent performance.
            """
        )

    def current_drivers(self):
        st.header("🏎️ Who were Red Bull's 2018 drivers?")

        drivers = self.f1_state.get_query_result(
            "red_bull_2018_drivers"
        )

        for driver in drivers["driver_name"]:
            st.markdown(f"### {driver}")

    def driver_performance(self):
        st.header("👥 How did the Red Bull drivers perform?")

        drivers = self.f1_state.get_query_result(
            "red_bull_driver_performance"
        )

        chart = (
            alt.Chart(drivers)
            .mark_bar()
            .encode(
                x=alt.X(
                    "driver_name:N",
                    title="Driver"
                ),
                y=alt.Y(
                    "total_points:Q",
                    title="2018 Points"
                ),
                tooltip=[
                    "driver_name",
                    "total_points"
                ],
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

        st.markdown(
            """
            Comparing the two drivers helps us understand
            how much each driver contributed to the team's
            performance before the 2019 season.
            """
        )

    def drivers_to_consider(self):
        st.header("🔎 Which drivers could Red Bull consider?")

        candidates = self.f1_state.get_query_result(
            "red_bull_best_drivers_to_consider"
        )

        st.dataframe(
            candidates,
            use_container_width=True
        )

        st.markdown(
            """
            These are high-scoring drivers from the 2018 season
            who were not racing for Red Bull.

            This does not mean they should automatically be signed.
            It provides a data-driven shortlist for further analysis.
            """
        )

    def circuit_performance(self):
        st.header("🏁 What are Red Bull's best and worst circuits?")

        circuits = self.f1_state.get_query_result(
            "red_bull_circuit_performance"
        )

        best = circuits.iloc[0]

        worst = circuits.sort_values(
            ["wins", "average_finish"],
            ascending=[True, False]
        ).iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "👍 Strongest Circuit",
                best["circuit_name"]
            )

            st.write(
                f"Historical wins: {int(best['wins'])}"
            )

        with col2:
            st.metric(
                "👎 Weakest Circuit",
                worst["circuit_name"]
            )

            st.write(
                f"Average finish: {worst['average_finish']:.2f}"
            )

        st.markdown(
            """
            Circuit performance can highlight tracks where
            Red Bull has historically performed strongly or
            struggled relative to its other races.
            """
        )

    def closest_competitors(self):
        st.header("💥 Who are Red Bull's closest competitors?")

        competitors = self.f1_state.get_query_result(
            "red_bull_closest_competitors"
        )

        chart = (
            alt.Chart(competitors)
            .mark_bar()
            .encode(
                x=alt.X(
                    "team_name:N",
                    title="Team"
                ),
                y=alt.Y(
                    "total_points:Q",
                    title="2018 Constructor Points"
                ),
                tooltip=[
                    "team_name",
                    "total_points",
                    "points_difference"
                ],
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

        st.dataframe(
            competitors,
            use_container_width=True
        )

    def conclusion(self):
        st.header("🔮 Looking Ahead to 2019")

        st.markdown(
            """
            ### What can we take from the historical data?

            Our analysis gives us several signals to consider
            when discussing Red Bull's prospects for 2019:

            - Historical constructor points show how the team's
              performance has evolved.
            - Driver performance shows the contribution of the
              2018 driver lineup.
            - Circuit results identify areas of historical
              strength and weakness.
            - Competitor analysis shows where Red Bull stood
              relative to nearby teams.
            - Driver comparisons can help identify possible
              alternatives when evaluating the lineup.

            These historical patterns can support a discussion
            about 2019, but they do not guarantee future results.
            """
        )


if __name__ == "__main__":
    st.title("🐂 Red Bull Racing: Road to 2019")

    st.markdown(
        """
        ## Can Red Bull challenge at the top in 2019?

        We explore Red Bull Racing's historical Formula 1 data
        to understand the team's position heading into the
        **2019 season**.

        Rather than looking at one number, we will explore the
        team's points, drivers, circuits and competitors.
        """
    )

    story = RedBullStory()

    story.points_over_the_years()

    st.divider()

    story.current_drivers()

    st.divider()

    story.driver_performance()

    st.divider()

    story.drivers_to_consider()

    st.divider()

    story.circuit_performance()

    st.divider()

    story.closest_competitors()

    st.divider()

    story.conclusion()
