# from django.db.models.signals import post_save, pre_delete, post_delete
# from django.dispatch import receiver
# from .models import Book

# @receiver(post_save, sender = Book)
# def signaler_nouvel_emprunt(sender, instance, created, **kwargs):
#     if created:
#         print(f"[SIGNAL] nouvel emprunt cree : {instance}")

# @receiver(pre_delete, sender=Book)
# def signaler_une_suppression(sender, instance, **kwargs):
#         print(f"[SIGNAL]Vous etes entrain de vouloir supprimer le livre: { instance.pk }")
# @receiver(post_delete, sender=Book)
# def notifier(sender, instance, **kwargs):
#     print(f"[SIGNAL]Vous avez supprime le livre: { instance.pk }")
#     still_exists = sender.objects.filter(id=instance.id).exists()    
#     if not still_exists:
#         print("La suppression en base de données est confirmée.")