import streamlit as st


def verdict_card(title, label, bg_color):
    return f"""
    <div style="
        background-color: {bg_color};
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 1rem; margin-bottom: 0.5rem;">{title}</div>
        {label}
    </div>
"""

# Table formatter


def render_indicator_table(indicators):
    def get_comment_color(comment):
        c = comment.lower()
        if "buy" in c or "bullish" in c or "undervalued" in c or "positive" in c:
            return "#d4f4dd"  # soft green
        elif "sell" in c or "bearish" in c or "overvalued" in c or "risk" in c or "negative" in c:
            return "#f9d6d5"  # soft red
        elif "hold" in c or "neutral" in c or "fair" in c:
            return "#f0f0f0"  # soft gray
        return "white"

    rows = ""
    for name, (value, comment) in indicators.items():
        bg = get_comment_color(comment)
        formatted_value = f"{value:.2f}"  # round to 2 decimal places
        # No multiline strings here, keep it simple
        rows += (
            f"<tr>"
            f"<td style='padding:6px 12px;'>{name}</td>"
            f"<td style='padding:6px 12px;'>{formatted_value}</td>"
            f"<td style='padding:6px 12px; background-color:{bg};'>{comment}</td>"
            f"</tr>"
        )

    table_html = (
        "<table style='width:100%; font-size:0.9rem; border-collapse:separate; border-spacing:0 6px;'>"
        "<thead>"
        "<tr style='background-color:#f0f2f6; text-align:left;'>"
        "<th style='padding:8px;'>Indicator</th>"
        "<th style='padding:8px;'>Value</th>"
        "<th style='padding:8px;'>Comment</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        f"{rows}"
        "</tbody>"
        "</table>"
    )
    return table_html
