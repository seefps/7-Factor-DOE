# 7-Factor DOE Simulator

A small educational simulator for process optimization in a browser using Streamlit.

## Setup

https://7-factor-doe-colin.streamlit.app/

## Run

```bash
streamlit run app.py
```

## Usage

1. Enter an 8-digit seed for model reproducibility.
2. Select "Regression".
3. Click `Apply Seed` to append a row to the table.
<img width="417" height="391" alt="image" src="https://github.com/user-attachments/assets/8964b6eb-1d15-4d9d-b11a-c27cca30cdc0" />
4. **Don't click until you want to see the answer!** Clicking `Answer` will reveal the full equation in the sidebar, two significant factors, the levels that generate the maximum response, and response surface plot.  The graph will display the point from the last trial run and can be manipulated for a better view.
<img width="652" height="753" alt="image" src="https://github.com/user-attachments/assets/46534b40-8959-4d39-8d62-12f401401ebd" />
5. Run Trials by inputing factors and Clicking 'Run Trial'
6. Import a batch of trial settings as CSV or Paste Table and Clicking 'Comupte Responses from Pasted Table'
7. Results are displayed in the Trial History
8. <img width="631" height="964" alt="image" src="https://github.com/user-attachments/assets/34c553ff-1417-40af-9086-c9ac763635a1" />
9.  Generate Contour Map by adding data from 2 factors and their response
<img width="652" height="915" alt="image" src="https://github.com/user-attachments/assets/1b7e5073-584c-4b86-b425-e0f95f7dc7a0" />
10. Click `Clear saved trials` to reset history.


## Notes


- All factors have linear effects, but only the significant ones have higher-order terms.
- The model returns identical results for the same seed.
- The response surface plot shows the two significant factors (not revealed until Answer).
