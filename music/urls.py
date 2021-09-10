
from django.urls import path
from .views import( UploadNewMusic, MusicListView, MusicRUDView, buyMusicView,
            OwnMusicListView, removeSongFormOwnedList, CreateMusicRequest,
            MusicRequestList, deleteRequestList, MusicSoldHistoy, deleteSoldHistory,
            addMusicToCart, AddToCartItems, purchaseMusic, CheckMusicListed, textView, 
            TopMusicList, topMusicList, LatestMusicList, addToCartItemsCount,
             RemoveMusicToCart, deleteListOfMusic, createTopMusicList, MusicListForTopListView, 
             MusicListWithFilterView, CreateAddView, AddListView, SearchSongView, sellReportSellAndRevenue,
             sellReportSellAndRevenueWithGivenDate, getSingleSong
             )


urlpatterns = [
    path('uplaod/', UploadNewMusic.as_view(), name="uploadMusic"),
    path('list/', MusicListView.as_view(), name="musicListView"),
    path('listwithfilter/<str:title>', MusicListWithFilterView.as_view(), name="musicListView"),
    path('listfortoplist/<str:title>', MusicListForTopListView.as_view(), name="listForTopView"),
    path('deletelistofmusic/', deleteListOfMusic, name="deleteListOfMusic"),
    path('toplist/', topMusicList, name="topList"),
    path('newtoplist/', createTopMusicList, name="newTopList"),
    path('latestmusic/', LatestMusicList.as_view(), name="LatestMusicList"),
    path('rud/<int:pk>/', MusicRUDView.as_view(), name="musicRUDView"),
    path('buymusic/<int:music_id>/', buyMusicView, name="owanMusicView"),
    path('removemusicfromownedlist/<int:music_id>/', removeSongFormOwnedList, name="removemusic"),
    path('ownedmusics/', OwnMusicListView.as_view(), name="owanMusicView"),
    path('createmusicrequest/', CreateMusicRequest.as_view(), name="createRequest"),
    path('musicrequestlist/', MusicRequestList.as_view(), name="requestList"),
    path('soldmusichistory/', MusicSoldHistoy.as_view(), name="soldMusichistory"),
    path('deletemusicrequestlist/', deleteRequestList, name="deleteRequestList"),
    path('deletesoldhistry/', deleteSoldHistory, name="deleteSoldHistry"),
    path('addremovetocart/<int:music_id>/', addMusicToCart, name="addToCart"),
    path('removeitemfromcart/<int:music_id>/', RemoveMusicToCart, name="addToCart"),
    path('addtocartitems/', AddToCartItems.as_view(), name="addToCart"),
    path('addtocartitemscount/', addToCartItemsCount, name="addToCartItemscount"),
    path('purchasemusic/', purchaseMusic, name="purchaseMusic"),
    path('checkmusiclisted/<str:spoftifyId>/', CheckMusicListed, name="CheckMusicListed"),
    path('test/<str:value>/', textView, name="test"),
    path('createadd/', CreateAddView.as_view(), name="createAdd"),
    path('listofadd/', AddListView.as_view(), name="createAdd"),
    path('searchMusic/', SearchSongView, name='searchMusic'),
    path('sellreport/', sellReportSellAndRevenue, name='sellreport'),
    path('sellreportwithgivendate/', sellReportSellAndRevenueWithGivenDate, name='sellreportwithgivendate'),
    path('singleSong/<int:id>', getSingleSong, name='singleSong'),
    

]
