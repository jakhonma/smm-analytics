from django.core.exceptions import ValidationError
import datetime


def validate_year(value):
    today = datetime.date.today()
    if value < 2000 or value > today.year:
        raise ValidationError(
            f"Yil 2000 va {today.year} oralig‘ida bo‘lishi kerak."
        )


def validate_month(value):
    if value < 1 or value > 12:
        raise ValidationError("Oy 1 dan 12 gacha bo‘lishi kerak.")


def validate_not_future_year_month(year, month):
    today = datetime.date.today()
    if year > today.year or (year == today.year and month > today.month):
        raise ValidationError("Kelajak vaqt uchun statistika kiritib bo‘lmaydi.")
