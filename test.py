import marimo

__generated_with = "0.14.16"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    return (pd,)


@app.cell
def _(pd):
    url = 'https://www.ecfr.gov/api/renderer/v1/content/enhanced/2025-08-01/title-15?subtitle=B&chapter=VII&subchapter=C&part=744&appendix=Supplement%20No.%204%20to%20Part%20744'
    df = pd.read_html(url)[0]
    for i, r in df.iterrows():
        if not pd.isna(r['Country']):
            country = r['Country']
        else:
            df.loc[i, 'Country'] = country
    df_washed = df[~df['Country'].str.match('^\\d')]
    df_washed
    return


if __name__ == "__main__":
    app.run()
