# Generated by Django 3.2.6 on 2021-09-10 17:27

from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add1', models.TextField()),
                ('add2', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Musics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('artist', models.CharField(max_length=500)),
                ('key', models.CharField(max_length=100)),
                ('bpm', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=100)),
                ('artWork', models.CharField(max_length=500)),
                ('spotifyId', models.CharField(max_length=250)),
                ('price', models.FloatField(default=0)),
                ('path', models.CharField(max_length=500)),
                ('song', models.FileField(upload_to=music.models.upload_Music)),
                ('youtubeId', models.CharField(max_length=250)),
                ('is_shortList', models.BooleanField(default=False)),
                ('sortNumber', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('spotifyId', models.CharField(max_length=250)),
                ('spotifyLink', models.CharField(max_length=2000)),
                ('count', models.IntegerField(default=1)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopMusicList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music', models.ManyToManyField(related_name='topMusicList', to='music.Musics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='topMusic', to='accounts.newusers')),
            ],
        ),
        migrations.CreateModel(
            name='SoldMusics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soldMusic', to='music.musics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyingUser', to='accounts.newusers')),
            ],
        ),
        migrations.CreateModel(
            name='OwnedMusics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('music', models.ManyToManyField(related_name='ownedMusics', to='music.Musics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='accounts.newusers')),
            ],
        ),
        migrations.CreateModel(
            name='AddMusicToCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('music', models.ManyToManyField(related_name='musicInCart', to='music.Musics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cartOwner', to='accounts.newusers')),
            ],
        ),
    ]
