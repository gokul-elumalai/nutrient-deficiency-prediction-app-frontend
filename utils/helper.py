


def get_bmi_color(bmi_class: str) -> str:
    """"
    Function to assign color based on BMI category
    """
    return {
        "Underweight": "#FFC107",   # Amber
        "Normal": "#4CAF50",        # Green
        "Overweight": "#FF9800",    # Orange
        "Obese": "#F44336",         # Red
    }.get(bmi_class, "#9E9E9E")     # Grey fallback


def prepare_view(row: dict) -> str:
    """
    Function to display Food Log Details
    """
    view = f'<div style="font-size:16px">'
    for k, v in row.items():
        row_view = f'<br><b>{k.capitalize()}:</b> {v}'
        view += row_view

    view += "</div>"

    return view

