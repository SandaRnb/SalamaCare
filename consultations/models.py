from django.db import models


class Consultation(models.Model):
    rendez_vous = models.OneToOneField(
        "rendezvous.RendezVous",
        on_delete=models.CASCADE,
        related_name="consultation",
    )
    diagnostic = models.TextField()
    ordonnance = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    date_consultation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ["-date_consultation"]

    def __str__(self):
        return f"Consultation du {self.date_consultation:%d/%m/%Y %H:%M}"
