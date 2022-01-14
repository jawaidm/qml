import os
import sys
import django
proj_path='/var/www/qml'
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qml.settings")
django.setup()


from qml.components.proposals.models import Proposal

p=Proposal.objects.last()

print(p.__dict__)

