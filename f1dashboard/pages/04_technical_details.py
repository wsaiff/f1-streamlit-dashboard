import streamlit as st


st.title("⚙️ Technical Details")

st.markdown(
    """
    ## How do we keep our Streamlit app fast?

    As the Formula 1 dataset grows, repeatedly loading the same
    data and recreating database connections can slow down the
    application.

    Our application uses several techniques to improve performance.

    ---

    ### 1. Database Connection Caching

    We use `@st.cache_resource` when creating the PostgreSQL
    database connection.

    ```python
    @st.cache_resource
    def init_connection(_self, credentials):
        conn = create_engine(credentials, echo=False)
        return conn
    ```

    This allows Streamlit to reuse the same database connection
    instead of creating a new connection every time the app reruns.

    ---

    ### 2. Query Result Caching

    Database queries use:

    ```python
    @st.cache_data(ttl=600)
    ```

    Query results are cached for **600 seconds (10 minutes)**.

    If the same query is requested again during this period,
    Streamlit can reuse the cached result instead of querying
    PostgreSQL again.

    ---

    ### 3. Session State

    We also use `st.session_state` to store data that has already
    been loaded during the user's session.

    Before requesting data again, the application checks whether
    the result already exists in session state.

    ```text
    User requests data
            ↓
    Is it in session_state?
       ↙             ↘
     Yes              No
      ↓                ↓
    Reuse it      Query database
                       ↓
                  Store in state
    ```

    This reduces unnecessary repeated work while the user navigates
    through the application.

    ---

    ### 4. SQL Queries

    Instead of loading every database table into memory for every
    analysis, SQL queries retrieve and aggregate the data required
    for each visualization.

    Operations such as:

    - `WHERE`
    - `GROUP BY`
    - `MAX`
    - `LIMIT`

    are performed in PostgreSQL before the result is returned to
    Streamlit.

    This becomes increasingly useful as the amount of data grows.

    ---

    ## Application Architecture

    The advanced dashboard separates responsibilities into different
    components:

    **F1Database**
    → manages the database connection.

    **F1Queries**
    → contains the SQL and data retrieval logic.

    **F1State**
    → manages session state and reuses query results.

    **Streamlit Pages**
    → handle presentation and visualizations.

    This separation makes the application easier to maintain and
    extend as new analyses are added.
    """
)
