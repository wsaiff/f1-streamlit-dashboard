import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timeit import default_timer as timer


conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)

TABLES = [
    "races",
    "circuits",
    "constructor_results",
    "constructor_standings",
    "constructors",
    "driver_standings",
    "drivers",
    "lap_times",
    "pit_stops",
    "qualifying",
    "results",
    "seasons",
    "status",
]


@st.cache_data
def load_data(table_name):
    """
    Loads data from the selected F1 database table.
    """
    data = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )

    return data


def create_main_page():
    """
    Creates the main Streamlit page and sidebar.
    Allows the user to select a table from TABLES.
    """

    st.title("Formula 1 Dashboard")
    st.subheader("Explore Formula 1 Data")

    st.sidebar.title("Formula 1")
    st.sidebar.markdown("Select a table to explore")

    selected_table = st.sidebar.selectbox(
        "Select a table",
        TABLES,
    )

    return selected_table


def summary_statistics(data):
    """
    Displays summary statistics for the selected data.
    """

    st.subheader("Summary statistics")

    st.write(data.describe())


@st.cache_data
def top_drivers():
    """
    Get the top 5 drivers with the most points.
    """

    query = """
        SELECT
            CONCAT(d.forename, ' ', d.surname) AS driver_name,
            SUM(ds.points) AS total_points
        FROM drivers d
        JOIN driver_standings ds
            ON d.driver_id = ds.driver_id
        GROUP BY
            d.driver_id,
            d.forename,
            d.surname
        ORDER BY total_points DESC
        LIMIT 5;
    """

    top_driver_data = pd.read_sql_query(
        query,
        conn
    )

    return top_driver_data


@st.cache_data
def lewis_over_the_years():
    """
    Get Lewis Hamilton's points between 2007 and 2018.
    """

    query = """
        SELECT
            r.year,
            MAX(ds.points) AS total_points
        FROM drivers d
        JOIN driver_standings ds
            ON d.driver_id = ds.driver_id
        JOIN races r
            ON ds.race_id = r.race_id
        WHERE
            d.forename = 'Lewis'
            AND d.surname = 'Hamilton'
            AND r.year BETWEEN 2007 AND 2018
        GROUP BY r.year
        ORDER BY r.year;
    """

    lewis_years = pd.read_sql_query(
        query,
        conn
    )

    return lewis_years


def session_state(data):
    """
    Store the dataframe in Streamlit session state.
    """

    if "data" not in st.session_state:
        st.session_state["data"] = None

    st.session_state["data"] = data


if __name__ == "__main__":

    selected_table = create_main_page()

    # Time how long loading the selected table takes
    start = timer()

    data = load_data(selected_table)

    end = timer()

    st.sidebar.info(
        f"{round(end - start, 4)} seconds to load the data"
    )

    # Display selected table
    st.dataframe(data)

    # Summary statistics
    summary_statistics(data)

    # Store data in session state
    session_state(data)

    # -----------------------------
    # Top 5 Drivers
    # -----------------------------

    st.subheader("Top 5 Drivers")

    top_driver_data = top_drivers()

    st.write(top_driver_data)

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
                "driver_name",
                "total_points"
            ],
        )
    )

    st.altair_chart(
        bar_chart,
        use_container_width=True
    )

    # -----------------------------
    # Lewis Hamilton over the years
    # -----------------------------

    st.subheader("Lewis Hamilton over the years")

    lewis_years = lewis_over_the_years()

    # Convert year to datetime
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
