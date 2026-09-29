"""
The page with the descriptive statistics allows a user of this dashboard
to get the summary statistics of the tables in the database.
"""

import streamlit as st

from f1dashboard.advanced.state import F1State
from f1dashboard.advanced.constants import F1Constants
from f1dashboard.advanced.database import F1Database
from f1dashboard.advanced.queries import F1Queries


class DescriptiveStatistics:
    def __init__(self) -> None:
        """Initialize the class"""
        self.f1_state = F1State()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries()

    def select_table(self):
        """Select the table to explore"""

        with st.sidebar:
            st.subheader("Select table to explore")

            self.selected_table = st.selectbox(
                "Select a table",
                F1Constants.table_names(),
            )

    def summary_statistics(self):
        """Write summary statistics of the selected table"""

        st.title("Descriptive statistics")

        if self.selected_table in st.session_state:
            st.info(
                f"Retrieve the {self.selected_table} table from state..."
            )

            table_results = self.f1_state.get_data_from_state(
                self.selected_table
            )

        else:
            st.info(
                f"Retrieve the {self.selected_table} table from the database..."
            )

            table_results = self.f1_queries.retrieve_table(
                self.selected_table
            )

            st.info(
                f"Saving the {self.selected_table} table to state..."
            )

            self.f1_state.store_in_state(
                self.selected_table,
                table_results
            )

        st.dataframe(table_results)

        st.subheader("Summary statistics")

        st.write(
            table_results.describe()
        )


if __name__ == "__main__":
    descriptive_statistics = DescriptiveStatistics()

    descriptive_statistics.select_table()

    descriptive_statistics.summary_statistics()
