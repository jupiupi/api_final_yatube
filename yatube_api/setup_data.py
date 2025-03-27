"""Скрипт для создания тестовых данных."""
import os
import sys
import django

# Добавляем проект в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment, Follow

User = get_user_model()

def setup_test_data():
    """Создание тестовых пользователей и данных."""
    print('Создание пользователей...')
    
    # Создаем админа
    admin, created = User.objects.get_or_create(username='root')
    admin.is_superuser = True
    admin.is_staff = True
    admin.email = 'root@admin.ru'
    admin.set_password('5eCretPaSsw0rD')
    admin.save()
    print(f"Пользователь 'root' {'создан' if created else 'обновлен'}")
    
    # Создаем обычного пользователя
    user, created = User.objects.get_or_create(username='regular_user')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'user@not-admin.ru'
    user.set_password('iWannaBeAdmin')
    user.save()
    print(f"Пользователь 'regular_user' {'создан' if created else 'обновлен'}")
    
    # Создаем второго пользователя
    second_user, created = User.objects.get_or_create(username='second_user')
    second_user.is_superuser = False
    second_user.is_staff = False
    second_user.email = 'second@not-admin.ru'
    second_user.set_password('5eCretPaSsw0rD')
    second_user.save()
    print(f"Пользователь 'second_user' {'создан' if created else 'обновлен'}")
    
    # Создаем тестовую группу
    group, created = Group.objects.get_or_create(
        title='TestGroup',
        slug='test-group',
        description='Some text.'
    )
    print(f"Группа 'TestGroup' {'создана' if created else 'обновлена'}")
    
    # Создаем пост от имени админа
    post, created = Post.objects.get_or_create(
        text='Тестовый пост от админа',
        author=admin,
        group=group
    )
    print(f"Пост от админа {'создан' if created else 'обновлен'}")
    
    # Создаем пост от имени обычного пользователя
    post, created = Post.objects.get_or_create(
        text='Тестовый пост от обычного пользователя',
        author=user,
        group=group
    )
    print(f"Пост от обычного пользователя {'создан' if created else 'обновлен'}")
    
    # Создаем комментарий
    comment, created = Comment.objects.get_or_create(
        post=post,
        author=second_user,
        text='Тестовый комментарий'
    )
    print(f"Комментарий {'создан' if created else 'обновлен'}")
    
    # Создаем подписку
    follow, created = Follow.objects.get_or_create(
        user=user,
        following=admin
    )
    print(f"Подписка {'создана' if created else 'обновлена'}")
    
    print('Настройка тестовых данных завершена.')

if __name__ == '__main__':
    setup_test_data() 