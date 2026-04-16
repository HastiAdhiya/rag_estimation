import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
    print('Created superuser: admin / admin123')
else:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Updated superuser: admin / admin123')
