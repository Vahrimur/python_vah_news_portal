from news_portal.newsapp.models import *

# 1. Создать двух пользователей.
u1 = User.objects.create_user(username='Игорь Гром')
u2 = User.objects.create_user(username='Бегемот Бегемотович')

# 2. Создать два объекта модели Author, связанных с пользователями.
au1 = Author.objects.create(authorUser=u1)
au2 = Author.objects.create(authorUser=u2)

# 3. Добавить 4 категории в модель Category.
Category.objects.create(name='Цифровые технологии')
Category.objects.create(name='Экономика')
Category.objects.create(name='Природа')
Category.objects.create(name='Культура')

# 4. Добавить 2 статьи и 1 новость.
Post.objects.create(author=au1, categoryType='NW', title='Встреча с тигром',
                    text='Краснокнижного хищника встретили автомобилисты ранним утром в Тернейском районе Приморского края. Тигр остановился прямо посреди дороги, задумался. И неторопливо — по-хозяйски, пошел по своим тигриным делам, сообщает РИА VladNews со ссылкой на Telegram-канал Новости Приморья.')
Post.objects.create(author=au2, categoryType='AR', title='IT в современной экономике',
                    text='В данной статье исследуется роль информационной технологии в современной экономике, так же определяется суть информационных технологий, которые в связи с всеобщей компьютеризацией вышли на более глобальный уровень развития. Определяются актуальные вопросы информационной экономики, которые влияют и изменяют экономику в целом.')
Post.objects.create(author=au2, categoryType='AR', title='IT как новый метод популяризации культурного наследия', text='В наше время мир реальности пересекается с миром виртуальности. Один мир живет в другом. Массовое и повсеместное внедрение информационных технологий заставляет иначе посмотреть и на феномен культуры. Сможет ли культура адаптироваться в новой реальности или ее будущее под вопросом вот актуальная проблема для современного социо-гуманитарного знания. Авторы приходят к выводу, что данное явление нельзя оценивать однозначно в негативном ключе, так как применение информационных технологий позволяет упростить процесс хранения и популяризации культурного наследия. Разрабатываемые исследователями-программистами компьютерные приложения уже сейчас создают особую «моду на культуру».')

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post.objects.get(id=1).postCategory.add(Category.objects.get(id=3))
Post.objects.get(id=2).postCategory.add(Category.objects.get(id=1))
Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))
Post.objects.get(id=3).postCategory.add(Category.objects.get(id=1))
Post.objects.get(id=3).postCategory.add(Category.objects.get(id=4))

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=u2, text='Я тоже видел тигра у дороги!')
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=u1, text='Ух ты! Давно?')
Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=u1, text='Очень интересная статья.')
Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=u1, text='Что-то не нравятся мне все эти цифровые новшества в музеях и искусстве...')

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(id=1).like()
Post.objects.get(id=1).like()
Post.objects.get(id=2).like()
Post.objects.get(id=3).dislike()
Comment.objects.get(id=1).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=4).dislike()

# 8. Обновить рейтинги пользователей.
au1.update_rating()
au2.update_rating()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
auWin = Author.objects.order_by('-ratingAuthor')[:1]
for i in auWin:
    i.authorUser.username
    i.ratingAuthor

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дизлайках к этой статье.
pWin = Post.objects.order_by('-rating')[:1]
for i in pWin:
    i.dateCreation
    i.author.authorUser.username
    i.rating
    i.title
    i.preview()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(commentPost=pWin).values('dateCreation', 'commentUser', 'rating', 'text')
