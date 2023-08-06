from mocca_lists.models import ArvRegimens


class Rx(ArvRegimens):
    """Declared as a proxy model for the autocomplete.

    turns out this was not necessary.
    """

    class Meta:
        proxy = True
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"
