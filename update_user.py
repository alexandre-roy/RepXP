import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repxp.settings")
django.setup()

from site_web.models import GroupeMusculaire, Exercice, User

def run():
    users = User.objects.all()
    min_birthdate = date.today().replace(year=date.today().year - 15)
    for user in users:
        user.date_naissance = min_birthdate
        user.avatar = 'avatars/default_avatar.png'
        user.save()

    
if __name__ == "__main__":
    run()