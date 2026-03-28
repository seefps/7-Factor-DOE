# 7-Factor DOE Simulator

A small educational simulator for process optimization in a browser using Streamlit.

## Setup

https://7-factor-doe-colin.streamlit.app/

## Run

```bash
streamlit run app.py
```

## Usage

<img width="417" height="391" alt="image" src="https://github.com/user-attachments/assets/8964b6eb-1d15-4d9d-b11a-c27cca30cdc0" />
<br><br>
1. Enter an 8-digit seed for model reproducibility.<br><br>
2. Select `Regression`<br><br>
3. Click `Apply Seed` to generate the problem.<br><br>

<br><br>
<br><br>

<img width="638" height="938" alt="image" src="https://github.com/user-attachments/assets/b13a036c-94b8-413c-9677-964c439fe285" />
<br><br>
4. ***Don't click until you want to see the answer!***<br><br>  
5. Run Trials by inputing factors and Clicking `Run Trial`<br><br>
6. Import a batch of trial settings as CSV or Paste Table and click `Comupte Responses from Pasted Table`<br><br>
7. Results are displayed in the Trial History. Click `Clear saved trials` in the sidebar to reset history.<br><br>

<br><br>
<br><br>

<img width="652" height="915" alt="image" src="https://github.com/user-attachments/assets/1b7e5073-584c-4b86-b425-e0f95f7dc7a0" />
<br><br>
8. Generate Contour Map by adding data from 2 factors and their response

<br><br>
<br><br>

<img width="652" height="753" alt="image" src="https://github.com/user-attachments/assets/46534b40-8959-4d39-8d62-12f401401ebd" />
<br><br>
9. Click `Answer` to reveal the full equation in the sidebar, two significant factors, the levels that generate the maximum response, and response surface plot.  The graph will display the point from the last trial run and can be manipulated for a better view.


## Notes


- All factors have linear effects, but only the significant ones have higher-order terms.
- The model returns identical results for the same seed.
- The response surface plot shows the two significant factors (not revealed until Answer).
