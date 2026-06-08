def normalize_digits(value: str) -> str:

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    translation_table = str.maketrans(
        persian_digits,
        english_digits
    )

    return value.translate(
        translation_table
    )