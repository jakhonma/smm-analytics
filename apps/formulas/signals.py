from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Formula
from apps.formulas.formula_cache import RedisFormulaCache


@receiver(post_save, sender=Formula)
@receiver(post_delete, sender=Formula)
def update_formula_cache(sender, **kwargs):
    """Formula o‘zgarganda cache yangilanadi"""
    RedisFormulaCache().refresh()
