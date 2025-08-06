import marimo

__generated_with = "0.14.16"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    return mo, pd


@app.cell
def _(mo):
    """
    App Title
    """
    mo.md("# 实体清单数据处理器").center()
    return


@app.cell
def _(mo):
    """
    1. URL Input
    - Creates a text input for the data source URL.
    - It's pre-filled with the example URL.
    """
    url = mo.ui.text(
        label="## 1. 输入数据源HTML的URL",
        value="https://www.ecfr.gov/api/renderer/v1/content/enhanced/2025-08-01/title-15?subtitle=B&chapter=VII&subchapter=C&part=744&appendix=Supplement%20No.%204%20to%20Part%20744",
        full_width=True
    ).form()
    url
    return (url,)


@app.cell
def _(mo, pd, url):
    """
    2. Data Loading and Cleaning
    - This cell is reactive and will re-execute when `url.value` changes.
    - It fetches the HTML table, cleans it, and provides user feedback.
    """

    if not url.value:
        df_washed = pd.DataFrame()
        computation_result = mo.md("...").center()
    else:
        # Show a loading message
        df_list = pd.read_html(url.value, encoding="utf-8")
        if not df_list:
            raise ValueError("未在URL中找到表格。")

        df_html = df_list[0]

        country = ""
        for i, r in df_html.iterrows():
            if pd.notna(r["Country"]):
                country = r["Country"]
            else:
                df_html.loc[i, "Country"] = country

        df_washed = df_html[~df_html["Country"].str.match("^\\d")]
        computation_result = mo.md(
            f"✅成功加载并清洗得到 **{len(df_washed)}** 条记录。"
        )
    mo.vstack((computation_result, mo.ui.table(df_washed)))
    return (df_washed,)


@app.cell
def _(mo):
    mo.md("""
          ---
          ## 2. 数据筛选
          """)
    return


@app.cell
def _(mo):
    mo.md("""### 2.1 只显示来自中国（CHINA, PEOPLE'S REPUBLIC OF）的实体""")
    return


@app.cell
def _(df_washed, mo, pd):
    if "Country" in df_washed.columns:
        df_china = df_washed[df_washed["Country"] == "CHINA, PEOPLE'S REPUBLIC OF"]
    else:
        df_china = pd.DataFrame()
    mo.ui.table(data=df_china)
    return


@app.cell
def _(mo):
    mo.md("""
          ---
          ### 2.2 使用您自己的Pandas代码进行筛选
          """)
    return


@app.cell
def _(mo):
    custom_filter_code = mo.ui.text_area(
        label="在下方输入Pandas筛选代码 (请使用 `df` 指代清洗后的数据):",
        placeholder='例如: df[df["Country"] == "JAPAN"]',
        full_width=True
    ).form()
    custom_filter_code
    return (custom_filter_code,)


@app.cell
def _(mo):
    """
    Helper text for generating code with AI.
    - Placed inside a collapsible details element.
    """

    mo.md(
        """
        您可以利用AI工具（如ChatGPT, Gemini, Copilot等）来生成筛选代码。

        **给AI的提示词示例:**

        *   `用pandas写一行代码，筛选出 df 中 Country 列是 'GERMANY' 的所有行。`
        *   `用pandas写一行代码，筛选出 df 中 Entity 列包含 'Technology' 关键字的所有行。`
        *   `用pandas写一行代码，筛选出 df 中 'Federal Register notice' 列是 '87 FR 32134' 并且 Country 列是 'RUSSIA' 的所有行。`
        """
    )
    return


@app.cell
def _(custom_filter_code, df_washed, mo, pd):
    """
    Logic for Filtering
    - This cell determines which dataframe to display based on user controls.
    - Custom code input takes precedence over the checkbox.
    """
    # Determine which dataframe to show
    if custom_filter_code.value:
        # User has entered custom code, this takes priority
        try:
            df = df_washed
            # Safely evaluate the expression
            final_df = eval(custom_filter_code.value, {"pd": pd, "df": df})
            if not isinstance(final_df, pd.DataFrame):
                filter_status = mo.md(
                    "❌**筛选代码错误:** 表达式未返回Pandas DataFrame。"
                )
                final_df = pd.DataFrame()  # show empty
            else:
                filter_status = mo.md(f"✅自定义筛选成功，找到 **{len(final_df)}** 条记录。")
        except Exception as e:
            filter_status = mo.md(f"**筛选代码错误:** {e}")
            final_df = pd.DataFrame()  # show empty
    else:
        # No filter, show all washed data
        final_df = df_washed
        filter_status = mo.md(f"未检测到筛选代码，显示全部数据")

    mo.vstack((filter_status, mo.ui.table(data=final_df)))

    return


if __name__ == "__main__":
    app.run()
