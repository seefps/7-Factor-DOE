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


def calculate_maximum_point(model, grid_points: int = 121):
    """Grid-search the maximum response within the factor bounds [-50, 50]."""
    sig1, sig2 = model.sig_factors
    expected_factors = ["A", "B", "C", "D", "E", "F", "G"]

    best_response = -np.inf
    best_factors = {f: 0.0 for f in expected_factors}

    grid = np.linspace(-50, 50, grid_points)
    for x_val in grid:
        for y_val in grid:
            candidate = {f: 0.0 for f in expected_factors}
            candidate[sig1] = float(x_val)
            candidate[sig2] = float(y_val)

            response = calculate_response(candidate, model)
            if response > best_response:
                best_response = float(response)
                best_factors = candidate

    return best_factors, best_response


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
        "Regression mode uses two significant factors with linear, quadratic, and one first-order interaction term; other factors add only small linear noise."
    )

    st.subheader("Trial History")
    st.dataframe(st.session_state.history, use_container_width=True)

    st.subheader("Compute Contour Graph")
    st.write(
        "Paste 3 columns: factor 1, factor 2, and response. "
        "A contour map with 10 gradients will be generated from the pasted data."
    )
    contour_table = st.text_area(
        "Paste contour data table",
        value="D,F,Response\n-20,-20,120\n-20,0,140\n-20,20,130\n0,-20,160\n0,0,180\n0,20,170\n20,-20,150\n20,0,165\n20,20,155",
        height=180,
        key="pasted_contour_table",
    )

    if st.button("Compute Contour Graph"):
        try:
            contour_df = pd.read_csv(StringIO(contour_table.strip()), sep=None, engine="python")
            if contour_df.shape[1] == 1:
                contour_df = pd.read_csv(
                    StringIO(contour_table.strip()),
                    sep=r"[\s,;\t]+",
                    engine="python",
                )

            if contour_df.shape[1] < 3:
                st.error("Please paste at least 3 columns: factor1, factor2, response.")
            else:
                contour_df = contour_df.iloc[:, :3].copy()
                x_name, y_name, z_name = contour_df.columns

                contour_df[x_name] = pd.to_numeric(contour_df[x_name], errors="coerce")
                contour_df[y_name] = pd.to_numeric(contour_df[y_name], errors="coerce")
                contour_df[z_name] = pd.to_numeric(contour_df[z_name], errors="coerce")
                contour_df = contour_df.dropna()

                if len(contour_df) < 6:
                    st.error("Need at least 6 valid rows to build a contour graph.")
                else:
                    bins = 25
                    x_edges = np.linspace(contour_df[x_name].min(), contour_df[x_name].max(), bins)
                    y_edges = np.linspace(contour_df[y_name].min(), contour_df[y_name].max(), bins)

                    binned = contour_df.assign(
                        x_bin=pd.cut(contour_df[x_name], bins=x_edges, include_lowest=True),
                        y_bin=pd.cut(contour_df[y_name], bins=y_edges, include_lowest=True),
                    )

                    pivot = binned.groupby(["y_bin", "x_bin"], observed=False)[z_name].mean().unstack()
                    z_grid_df = pivot.copy()
                    z_grid_df = z_grid_df.interpolate(axis=0, limit_direction="both")
                    z_grid_df = z_grid_df.interpolate(axis=1, limit_direction="both")
                    z_grid_df = z_grid_df.fillna(z_grid_df.stack().mean())

                    x_centers = [interval.mid for interval in z_grid_df.columns]
                    y_centers = [interval.mid for interval in z_grid_df.index]
                    z_grid = z_grid_df.to_numpy(dtype=float)

                    contour_fig = go.Figure(
                        data=go.Contour(
                            x=x_centers,
                            y=y_centers,
                            z=z_grid,
                            colorscale="Viridis",
                            ncontours=10,
                            contours=dict(coloring="heatmap", showlines=True),
                            colorbar=dict(title=z_name),
                        )
                    )
                    contour_fig.add_trace(
                        go.Scatter(
                            x=contour_df[x_name],
                            y=contour_df[y_name],
                            mode="markers",
                            marker=dict(size=6, color="white", line=dict(color="black", width=1)),
                            name="Pasted points",
                        )
                    )
                    contour_fig.update_layout(
                        title=f"Contour Map: {z_name} vs {x_name}/{y_name}",
                        xaxis_title=x_name,
                        yaxis_title=y_name,
                        height=550,
                    )
                    st.plotly_chart(contour_fig, use_container_width=True)
                    st.success(f"Contour graph generated from {len(contour_df)} rows.")
        except Exception as exc:
            st.error(f"Could not parse contour table. Check format and delimiters. Error: {exc}")

    if st.session_state.show_answer:
        max_factors, max_response = calculate_maximum_point(st.session_state.model)
        sig1, sig2 = st.session_state.model.sig_factors

        st.subheader("Calculated Maximum Point")
        st.write(
            f"Best predicted settings in bounds: {sig1} = {max_factors[sig1]:.2f}, "
            f"{sig2} = {max_factors[sig2]:.2f}, Response = {max_response:.4f}"
        )

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
