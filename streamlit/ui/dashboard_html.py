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
        if "buy" in c or "bullish" in c:
            return "#d4f4dd"
        elif "sell" in c or "bearish" in c:
            return "#f9d6d5"
        elif "hold" in c or "neutral" in c:
            return "#f0f0f0"
        return "white"

    rows = ""
    for name, (value, comment) in indicators.items():
        bg = get_comment_color(comment)
        rows += f"<tr><td>{name}</td><td>{value}</td><td style='background-color:{bg};'>{comment}</td></tr>"

    return f"""
    <table style='width:100%; font-size:0.9rem;'>
        <tr><th>Indicator</th><th>Value</th><th>Comment</th></tr>
        {rows}
    </table>
    """
