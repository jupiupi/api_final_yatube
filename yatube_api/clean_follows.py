"""Скрипт для очистки всех подписок."""
import os
import sys
import django

# Добавляем проект в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube_api.settings')
django.setup()

from posts.models import Follow

def clean_follows():
    """Удаление всех подписок."""
    count = Follow.objects.all().count()
    Follow.objects.all().delete()
    print(f"Удалено {count} подписок.")

if __name__ == "__main__":
    clean_follows() 