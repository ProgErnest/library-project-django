from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author
@receiver(post_save,sender=Author)
def added_author(sender, instance, created,**kwargs):
    if created:
        print("[SIGNAL]: Un auteur cree ", instance.surname, instance.name)
    else:
        print("[SIGNAL]: Un auteur modifie ", instance.surname, instance.name)
