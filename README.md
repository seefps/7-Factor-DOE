# 7-Factor DOE Simulator

A small educational simulator for process optimization in a browser using Streamlit.

## Setup

```bash
cd doe_simulator_project
python -m pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Usage

1. Enter an 8-digit seed for model reproducibility.
2. Move sliders or enter values for factors A..G (-50..50).
3. Click `Run Trial` to append a row to the table.
4. Click `Answer` to reveal the full equation and response surface plot for the two significant factors.
5. Use the checkbox to hide/show the response surface plot.
6. Click `Clear saved trials` to reset history.

## Notes

- Two randomly selected factors are highly significant with quadratic and cubic effects, plus interactions.
- All factors have linear effects, but only the significant ones have higher-order terms.
- The model includes false peaks to encourage systematic DOE testing.
- The model returns identical results for the same seed.
- The response surface plot shows the two significant factors (not revealed until Answer).
