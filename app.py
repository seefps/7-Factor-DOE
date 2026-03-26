"""Streamlit interface for 7-factor DOE simulator."""
from io import StringIO

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from doe_model import generate_seeded_model, calculate_response, model_equation


def init_state() -> None:
    if "seed" not in st.session_state:
        st.session_state.seed = 12345678
    if "model_type" not in st.session_state:
        st.session_state.model_type = "regression"
    if "model" not in st.session_state:
        st.session_state.model = generate_seeded_model(st.session_state.seed, model_type=st.session_state.model_type)
    if "history" not in st.session_state:
        st.session_state.history = pd.DataFrame(
            columns=["A", "B", "C", "D", "E", "F", "G", "Response"]
        )
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "show_plot" not in st.session_state:
        st.session_state.show_plot = True


def reset_history() -> None:
    st.session_state.history = pd.DataFrame(
        columns=["A", "B", "C", "D", "E", "F", "G", "Response"]
    )


def reset_model(seed: int, model_type: str = "regression") -> None:
    st.session_state.seed = seed
    st.session_state.model_type = model_type
    st.session_state.model = generate_seeded_model(seed, model_type=model_type)
    st.session_state.show_answer = False


def plot_response_surface(model, factors_fixed, grid_points=81):
    sig1, sig2 = model.sig_factors
    x = np.linspace(-50, 50, grid_points)
    y = np.linspace(-50, 50, grid_points)
    X, Y = np.meshgrid(x, y)

    # Create factor dict for calculation
    factors_grid = {f: 0.0 for f in ['A','B','C','D','E','F','G']}
    factors_grid[sig1] = X
    factors_grid[sig2] = Y

    Z = np.zeros_like(X)
    for i in range(grid_points):
        for j in range(grid_points):
            factors_grid[sig1] = X[i,j]
            factors_grid[sig2] = Y[i,j]
            Z[i,j] = calculate_response(factors_grid, model)

    fig = go.Figure(
        data=[
            go.Surface(x=x, y=y, z=Z, colorscale="Viridis", opacity=0.8),
            go.Scatter3d(
                x=np.array([factors_fixed[sig1]]),
                y=np.array([factors_fixed[sig2]]),
                z=np.array([calculate_response(factors_fixed, model)]),
                mode="markers",
                marker=dict(size=5, color="red"),
                name="Current point",
            ),
        ]
    )
    fig.update_layout(
        title=f"{sig1}/{sig2} Response Surface",
        scene=dict(xaxis_title=sig1, yaxis_title=sig2, zaxis_title="Response"),
        height=600,
    )
    return fig


def main() -> None:
    st.set_page_config(page_title="7-Factor DOE Simulator", layout="wide")
    st.title("7-Factor DOE Simulator for Process Optimization")
    st.markdown(
        "Use factors A-G to evaluate response. Two factors are highly significant with complex effects."
    )

    init_state()

    with st.sidebar:
        st.header("Model Settings")

        seed_input = st.text_input(
            "8-digit seed (for reproducibility)",
            value=str(st.session_state.seed).zfill(8),
            max_chars=8,
        )

        model_type = st.radio(
            "Model Type",
            options=["gaussian", "regression"],
            format_func=lambda x: "Gaussian Peaks" if x == "gaussian" else "Regression (Main + Interactions)"
        )

        if st.button("Apply Seed"):
            try:
                seed_value = int(seed_input)
                reset_model(seed_value, model_type=model_type)
                st.success(f"Model regenerated with seed {seed_value}")
            except ValueError:
                st.error("Seed must be an integer up to 8 digits.")

        st.write("**Current model equation (hidden until Answer pressed)**")
        if st.session_state.show_answer:
            st.write(model_equation(st.session_state.model))

        st.button("Clear saved trials", on_click=reset_history)

    st.subheader("Trial Input")
    cols = st.columns(7)

    factor_values = {}
    for i, factor in enumerate(["A", "B", "C", "D", "E", "F", "G"]):
        with cols[i]:
            factor_values[factor] = st.number_input(
                f"{factor}", -50.0, 50.0, 0.0, step=1.0, key=f"input_{factor}"
            )

    if st.button("Run Trial"):
        response_val = calculate_response(factor_values, st.session_state.model)
        new_row = pd.DataFrame([{**factor_values, "Response": round(response_val, 6)}])
        st.session_state.history = pd.concat(
            [st.session_state.history, new_row], ignore_index=True
        )

    if st.button("Answer"):
        st.session_state.show_answer = True

    st.subheader("Batch Response Calculator")
    st.write(
        "Paste a table with factor columns A-G (comma, tab, or space delimited). "
        "Responses will be calculated using the current hidden model."
    )
    pasted_table = st.text_area(
        "Paste factor table",
        value="A,B,C,D,E,F,G\n0,0,0,0,0,0,0\n10,-5,0,0,0,0,0",
        height=180,
        key="pasted_factor_table",
    )

    if st.button("Compute Responses from Pasted Table"):
        try:
            batch_df = pd.read_csv(StringIO(pasted_table.strip()), sep=None, engine="python")
            if batch_df.shape[1] == 1:
                batch_df = pd.read_csv(
                    StringIO(pasted_table.strip()),
                    sep=r"[\s,;\t]+",
                    engine="python",
                )

            expected_factors = ["A", "B", "C", "D", "E", "F", "G"]
            upper_map = {col.upper(): col for col in batch_df.columns}

            normalized = pd.DataFrame()
            for factor in expected_factors:
                if factor in upper_map:
                    normalized[factor] = pd.to_numeric(
                        batch_df[upper_map[factor]], errors="coerce"
                    ).fillna(0.0)
                else:
                    normalized[factor] = 0.0

            normalized["Response"] = normalized.apply(
                lambda row: round(
                    calculate_response(
                        {f: float(row[f]) for f in expected_factors},
                        st.session_state.model,
                    ),
                    6,
                ),
                axis=1,
            )

            st.success(f"Computed responses for {len(normalized)} rows.")
            st.dataframe(normalized, use_container_width=True)
            st.download_button(
                label="Download Batch Results CSV",
                data=normalized.to_csv(index=False),
                file_name="batch_responses.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"Could not parse table. Check delimiters/header format. Error: {exc}")


    st.subheader("Effects Reference")
    st.write(
        "Model includes seeded significant main effects for 2 factors plus first-order and second-order interactions."
    )

    st.subheader("Trial History")
    st.dataframe(st.session_state.history, use_container_width=True)

    if st.session_state.show_answer:
        st.subheader("Response Surface Plot")
        show_plot = st.checkbox("Show response surface plot", value=st.session_state.show_plot)
        st.session_state.show_plot = show_plot
        if show_plot:
            fig = plot_response_surface(
                st.session_state.model,
                factor_values,
            )
            st.plotly_chart(fig, use_container_width=True)


    st.subheader("Peer Reproducibility")
    st.write(
        "Give this seed to another student to be in the same hidden model space: "
        f"{st.session_state.model.seed:08d}"
    )


if __name__ == "__main__":
    main()
