from django.contrib import admin
from django.db.models.base import Model
from .models import Musics,OwnedMusics, RequestMusic, SoldMusics, AddMusicToCart, TopMusicList, AddField
# Register your models here.
admin.site.register(Musics)
admin.site.register(OwnedMusics)
admin.site.register(RequestMusic)
admin.site.register(SoldMusics)
admin.site.register(AddMusicToCart)
admin.site.register(TopMusicList)
admin.site.register(AddField)
