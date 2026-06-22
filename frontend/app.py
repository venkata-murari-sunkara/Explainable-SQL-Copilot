import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.title("🤖 Explainable SQL Copilot")

st.subheader("Upload Dataset")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if st.button("Upload and Ingest"):
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        result = response.json()

        if result["success"]:
            st.success("CSV uploaded and ingested successfully.")

            st.session_state["table_name"] = result["table_name"]
            st.session_state["rows"] = result["rows"]
            st.session_state["columns"] = result["columns"]

            st.session_state.pop("sql", None)
            st.session_state.pop("explanation", None)
            st.session_state.pop("result", None)

        else:
            st.error(result["error"])

if "table_name" in st.session_state:
    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Table", st.session_state["table_name"])
    col2.metric("Rows", st.session_state["rows"])
    col3.metric("Columns", len(st.session_state["columns"]))

    with st.expander("View Columns"):
        st.write(", ".join(st.session_state["columns"]))

st.set_page_config(
    page_title="Explainable SQL Copilot",
    layout="wide"
)


question = st.text_input(
    "Ask a question about your data"
)

if st.button("Generate Query"):

    response = requests.post(
        f"{API_URL}/generate-query",
        json={"question": question}
    )

    result = response.json()

    if result["success"]:

        st.session_state["sql"] = result["sql"]
        st.session_state["explanation"] = result["explanation"]

    else:
        st.error(result["error"])

if "sql" in st.session_state:

    st.subheader("Generated SQL")

    st.code(
        st.session_state["sql"],
        language="sql"
    )

    st.subheader("Explanation")

    st.info(
        st.session_state["explanation"]
    )

if "sql" in st.session_state:

    if st.button("Approve & Execute"):

        response = requests.post(
            f"{API_URL}/execute-query",
            json={
                "sql": st.session_state["sql"]
            }
        )

        result = response.json()

        st.session_state["result"] = result

if "result" in st.session_state:
    result = st.session_state["result"]

    if result.get("success"):
        st.subheader("Results")

        df = pd.DataFrame(result["rows"])

        tab1, tab2 = st.tabs(["Table", "Chart"])

        with tab1:
            st.dataframe(df, use_container_width=True)

        with tab2:
            if len(df.columns) == 2:
                x_col = df.columns[0]
                y_col = df.columns[1]

                if pd.api.types.is_numeric_dtype(df[y_col]):
                    fig = px.bar(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f"{y_col} by {x_col}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Chart not available because the second column is not numeric.")
            else:
                st.info("Chart available only for two-column results.")

    else:
        st.error(result.get("error", "Query execution failed."))