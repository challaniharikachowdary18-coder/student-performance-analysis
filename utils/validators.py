def parse_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a whole number.")

def validate_marks(score, max_marks):
    if score < 0 or score > max_marks:
        raise ValueError(f"Marks must be between 0 and {max_marks}.")
