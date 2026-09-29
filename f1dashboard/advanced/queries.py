import pandas as pd
import streamlit as st
from f1dashboard.advanced.database import F1Database


class F1Queries:
    def __init__(self) -> None:
        self.conn = F1Database().db_connection

    @st.cache_data(ttl=600)
    def _run_query(_self, query):
        """
        Run a SQL query and return the result as a DataFrame.
        Cached for 10 minutes to avoid unnecessary database queries.
        """
        return pd.read_sql_query(query, _self.conn)

    def retrieve_table(self, table_name):
        """Retrieve all data from a selected table."""

        return self._run_query(
            f"""
            SELECT *
            FROM {table_name};
            """
        )

    def top_drivers(self):
        """Get the top 5 drivers with the most points."""

        return self._run_query(
            """
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
        )

    def lewis_over_the_years(self):
        """Get Lewis Hamilton's season points from 2007 to 2018."""

        return self._run_query(
            """
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
        )

    def red_bull_points_over_the_years(self):
        """Get Red Bull constructor points for each season."""

        return self._run_query(
            """
            SELECT
                r.year,
                MAX(cs.points) AS total_points
            FROM constructors c
            JOIN constructor_standings cs
                ON c.constructor_id = cs.constructor_id
            JOIN races r
                ON cs.race_id = r.race_id
            WHERE c.name = 'Red Bull'
            GROUP BY r.year
            ORDER BY r.year;
            """
        )

    def red_bull_2018_drivers(self):
        """Get Red Bull drivers from the 2018 season."""

        return self._run_query(
            """
            SELECT DISTINCT
                CONCAT(d.forename, ' ', d.surname) AS driver_name
            FROM drivers d
            JOIN results res
                ON d.driver_id = res.driver_id
            JOIN constructors c
                ON res.constructor_id = c.constructor_id
            JOIN races r
                ON res.race_id = r.race_id
            WHERE
                c.name = 'Red Bull'
                AND r.year = 2018
            ORDER BY driver_name;
            """
        )

    def red_bull_driver_performance(self):
        """Compare Red Bull drivers during the 2018 season."""

        return self._run_query(
            """
            SELECT
                CONCAT(d.forename, ' ', d.surname) AS driver_name,
                MAX(ds.points) AS total_points
            FROM drivers d
            JOIN driver_standings ds
                ON d.driver_id = ds.driver_id
            JOIN races r
                ON ds.race_id = r.race_id
            JOIN results res
                ON res.race_id = r.race_id
                AND res.driver_id = d.driver_id
            JOIN constructors c
                ON res.constructor_id = c.constructor_id
            WHERE
                c.name = 'Red Bull'
                AND r.year = 2018
            GROUP BY
                d.driver_id,
                d.forename,
                d.surname
            ORDER BY total_points DESC;
            """
        )

    def red_bull_best_drivers_to_consider(self):
        """
        Find high-performing 2018 drivers who were not
        driving for Red Bull.
        """

        return self._run_query(
            """
            SELECT
                CONCAT(d.forename, ' ', d.surname) AS driver_name,
                MAX(ds.points) AS total_points
            FROM drivers d
            JOIN driver_standings ds
                ON d.driver_id = ds.driver_id
            JOIN races r
                ON ds.race_id = r.race_id
            WHERE
                r.year = 2018
                AND d.driver_id NOT IN (
                    SELECT DISTINCT res.driver_id
                    FROM results res
                    JOIN constructors c
                        ON res.constructor_id = c.constructor_id
                    JOIN races r2
                        ON res.race_id = r2.race_id
                    WHERE
                        c.name = 'Red Bull'
                        AND r2.year = 2018
                )
            GROUP BY
                d.driver_id,
                d.forename,
                d.surname
            ORDER BY total_points DESC
            LIMIT 5;
            """
        )

    def red_bull_circuit_performance(self):
        """Get Red Bull's historical performance by circuit."""

        return self._run_query(
            """
            SELECT
                ci.name AS circuit_name,
                SUM(
                    CASE
                        WHEN res.position = 1 THEN 1
                        ELSE 0
                    END
                ) AS wins,
                AVG(res.position::numeric) AS average_finish
            FROM results res
            JOIN constructors c
                ON res.constructor_id = c.constructor_id
            JOIN races r
                ON res.race_id = r.race_id
            JOIN circuits ci
                ON r.circuit_id = ci.circuit_id
            WHERE
                c.name = 'Red Bull'
                AND res.position IS NOT NULL
            GROUP BY ci.circuit_id, ci.name
            ORDER BY
                wins DESC,
                average_finish ASC;
            """
        )

    def red_bull_closest_competitors(self):
        """
        Find the two constructors closest to Red Bull
        in the 2018 constructor standings.
        """

        return self._run_query(
            """
            WITH final_standings AS (
                SELECT
                    c.constructor_id,
                    c.name AS team_name,
                    MAX(cs.points) AS total_points
                FROM constructors c
                JOIN constructor_standings cs
                    ON c.constructor_id = cs.constructor_id
                JOIN races r
                    ON cs.race_id = r.race_id
                WHERE r.year = 2018
                GROUP BY
                    c.constructor_id,
                    c.name
            ),
            red_bull AS (
                SELECT total_points
                FROM final_standings
                WHERE team_name = 'Red Bull'
            )
            SELECT
                fs.team_name,
                fs.total_points,
                ABS(fs.total_points - rb.total_points) AS points_difference
            FROM final_standings fs
            CROSS JOIN red_bull rb
            WHERE fs.team_name <> 'Red Bull'
            ORDER BY points_difference ASC
            LIMIT 2;
            """
        )


if __name__ == "__main__":
    queries = F1Queries()
