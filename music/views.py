
import re
import time
import datetime
from django.db.models import Q, Sum
from django.contrib.auth import login
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import( MusicCreateSerializers, MusicRUDSerializers, OwnedMusicSerializer, 
                        RequestMusicSerializers, SoldMusicSerializer, AddToCartSerializer,
                        UserSerializer, TopMusicSerializer, AddSerializer, SearchSongReviewSerializers)
from .models import  AddField, Musics, OwnedMusics, RequestMusic, SoldMusics, AddMusicToCart, RequestMusic, TopMusicList

class UploadNewMusic(CreateAPIView):
    permission_classes=[IsAdminUser, ]
    serializer_class  = MusicCreateSerializers
    queryset = Musics.objects.all()

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def UploadNewMusic(request):
#     song = request.data
#     # for i in range(0, len(song)):
#     #     print(song['song['+str(i)+']'])
#     for i in range(0, len(song)):
#         serializer = MusicCreateSerializers(data={'song':song['song['+str(i)+']']})
#         if serializer.is_valid():
#             serializer.save()
#             if i==len(song)-1:
#                 return Response('success',  status=status.HTTP_201_CREATED) 
            
#     return Response('fail', status=status.HTTP_400_BAD_REQUEST)

class MusicListView(ListAPIView):
    serializer_class = MusicRUDSerializers
    queryset = Musics.objects.all().order_by('createdAt')

class MusicListWithFilterView(ListAPIView):
    serializer_class = MusicRUDSerializers
    def get_queryset(self):
        title = self.kwargs.get('title')
        if title!="'":
             queryset = Musics.objects.filter( Q(title__icontains=title)).order_by('-createdAt')
        else:
            queryset = Musics.objects.all()            

       
        return queryset
    

class MusicListForTopListView(ListAPIView):
    permission_classes=[IsAdminUser, ]
    serializer_class = MusicRUDSerializers
    def get_queryset(self):
        data = TopMusicList.objects.get(id=2)
        title = self.kwargs.get('title')
        if title!="'":
            queryset = Musics.objects.filter( Q(title__icontains=title)).exclude(id__in=data.music.all())
            print(queryset)
        else:
            queryset = Musics.objects.all().exclude(id__in=data.music.all())          
        
        print(queryset)
        return queryset
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def deleteListOfMusic(request):
    id = request.data
    for i in id:
        music = Musics.objects.get(id=int(i))
        music.delete()
    time.sleep(5)
    
    return Response('deleted')


@api_view(['GET'])
def topMusicList(request):
    data = TopMusicList.objects.get(id=2)
    serializer = TopMusicSerializer(data)

    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([IsAdminUser, ])
def createTopMusicList(request):
    data = TopMusicList.objects.get(id=2)

    new_id = request.data
    if new_id[0]=='single':
        for id in new_id[1:]:
            print(id)
            music = Musics.objects.get(id=id)
            data.music.add(music)
    elif new_id[0]=='all':
        data.music.clear()
        for id in new_id[1:]:
            music = Musics.objects.get(id=id)
            print(id)
            data.music.add(music)
    
    return Response('succcess')



class LatestMusicList(ListAPIView):
    serializer_class = MusicRUDSerializers
    queryset = Musics.objects.all().order_by('-createdAt')[:30]

class MusicRUDView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser, ]
    serializer_class = MusicRUDSerializers
    queryset = Musics.objects.all()

@api_view(['GET'])
def buyMusicView(request, music_id):
    user  = request.user
    music = Musics.objects.get(id=music_id)
    SoldMusics.objects.create(user=user, music=music)
    ownMusic = OwnedMusics.objects.get(user=user)
    ownMusic.music.add(music)
    return Response('added')

@api_view(['GET'])
def removeSongFormOwnedList(request, music_id):
    user  = request.user
    music = Musics.objects.get(id=music_id)
    ownMusic = OwnedMusics.objects.get(user=user)
    ownMusic.music.remove(music)
    return Response('removed')

class OwnMusicListView(ListAPIView):
    permission_classes=[IsAuthenticated, ]
    serializer_class = OwnedMusicSerializer
    def get_queryset(self):
        return OwnedMusics.objects.filter(user=self.request.user)


class CreateMusicRequest(CreateAPIView):

    serializer_class = RequestMusicSerializers
    queryset = RequestMusic.objects.all()

class MusicRequestList(ListAPIView):
    # permission_classes=[IsAdminUser, ]
    serializer_class = RequestMusicSerializers
    queryset = RequestMusic.objects.all().order_by('-createdAt')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def deleteRequestList(request):
    id = request.data
    for i in id:
        musicRequest = RequestMusic.objects.get(id=int(i))
        musicRequest.delete()
    return Response('ids')


class MusicSoldHistoy(ListAPIView):
    permission_classes=[IsAdminUser, ]
    serializer_class = SoldMusicSerializer
    queryset = SoldMusics.objects.all()

@api_view(['POST'])
@permission_classes([IsAdminUser])
def deleteSoldHistory(request):
    id = request.data
    for i in id:
        history = SoldMusics.objects.get(id=int(i))
        history.delete()
    return Response('deleted')




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addMusicToCart(request, music_id):
    cart = AddMusicToCart.objects.get(user=request.user)
    music = Musics.objects.get(id=music_id)
    ownedMusic = OwnedMusics.objects.get(user=request.user)
    if music in ownedMusic.music.all():
        return Response('purched allready')

    if music in cart.music.all():
        return Response('already added to cart')
    else:
        cart.music.add(music)
        return Response('added to cart')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RemoveMusicToCart(request, music_id):
    cart = AddMusicToCart.objects.get(user=request.user)
    music = Musics.objects.get(id=music_id)

    if music in cart.music.all():
        cart.music.remove(music)
        return Response('success')
    else:
        return Response('false')

    
class AddToCartItems(ListAPIView):
    permission_classes=[IsAuthenticated, ]
    serializer_class = AddToCartSerializer
    def get_queryset(self):
        return AddMusicToCart.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated ])
def addToCartItemsCount(request):
        user= request.user
        if not request.user.is_superuser:
            items = AddMusicToCart.objects.get(user=request.user)
            count = items.music.all().count()
            return Response(count)
        else:
            return Response(0)

@api_view(['GET'])
@permission_classes([IsAuthenticated ])
def purchaseMusic(request):
    user = request.user
    items = AddMusicToCart.objects.get(user=user)
    ownedMusicTable = OwnedMusics.objects.get(user=user)
    for song in items.music.all():
        ownedMusicTable.music.add(song)
        SoldMusics.objects.create(user=user, music=song)

    items.music.clear()
    return Response('successs')


@api_view(['GET'])
def CheckMusicListed(request, spoftifyId):
    music = Musics.objects.filter(spotifyId=spoftifyId).first()
    if music:
        serializer  = MusicRUDSerializers(music)
        return Response({'data':serializer.data, 'is_listed':True})
    else:
        return Response({'is_listed':False})

@api_view(['GET'])
def textView(request, value):
    user = request.user
    music = Musics.objects.filter(spotifyId=value)
    is_requested = RequestMusic.objects.filter(spotifyId=value)
    if user and not user.is_superuser:
        cart = AddMusicToCart.objects.get(user=user)
        owned = OwnedMusics.objects.get(user=user)
        
        if is_requested:
            return Response('requested')
        if music and music[0] in owned.music.all():
            return Response('owned')
        if music and music[0] in cart.music.all():
            return Response('added')    
        if music and music[0]:
            return Response(music[0].id)
        else:
            print('fail')
            return Response('fail')
    else:
        if is_requested:
            return Response('requested')
        else:
            return Response('fail')
    print('hello')


class CreateAddView(CreateAPIView):
    serializer_class = AddSerializer
    queryset = AddField.objects.all()

class AddListView(ListAPIView):
    serializer_class = AddSerializer
    queryset = AddField.objects.filter(id=1)



@api_view(['POST'])
def SearchSongView(request):
    class songs: 
        def __init__(self,id, name, artwork, artist, key, bpm, price, spotifyId, spotifyLink, is_abailable): 
            self.id = id
            self.name = name 
            self.artwork = artwork
            self.artist = artist
            self.key = key
            self.bpm = bpm
            self.price = price
            self.spotifyId = spotifyId
            self.spotifyLink = spotifyLink
            self.is_abailable = is_abailable

    songList = []

    data = request.data
    for song in data:
        # print(song['album']['images'][0]['url'], song['name'], song['album']['artists'][0]['name'],song['id'], '\n')
        songArtWork = song['album']['images'][0]['url']
        songTitle = song['name'] 
        spotifyId= song['id']
        songArtist = song['album']['artists'][0]['name']
        songLink = song['external_urls']['spotify']
        song = Musics.objects.filter(spotifyId=song['id']).first()
        if song:
            songList.append(songs(song.id, song.title, song.artWork, song.artist, song.key, song.bpm, song.price, spotifyId, songLink, True))
        else:
            songList.append(songs('0', songTitle, songArtWork, songArtist,'0', '0', '0', spotifyId,  songLink, False))

    # for song in songList:
    #     print(song.name, song.artist,  song.key, song.bpm, song.is_abailable)

    serializer = SearchSongReviewSerializers(songList, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def sellReportSellAndRevenue(request):
    last_date = datetime.datetime.now() - datetime.timedelta(days=1)
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    last24HSellProductCount = SoldMusics.objects.filter(createdAt__gte=last_date).count()
    last24HSellAvgRevenu = SoldMusics.objects.filter(createdAt__gte=last_date).aggregate(Sum('music__price'))

    last30DSellProductCount = SoldMusics.objects.filter(createdAt__gte=last_month).count()
    last30DSellAvgRevenu = SoldMusics.objects.filter(createdAt__gte=last_month).aggregate(Sum('music__price'))
    return Response({'numberOfSelllast30Days': last30DSellProductCount, 'revenueOnLast30DSell': last30DSellAvgRevenu,
    'numberOfSelllast24Hays':last24HSellProductCount, 'revenueOnLast24HSell':last24HSellAvgRevenu})

@api_view(['POST'])
def sellReportSellAndRevenueWithGivenDate(request):

    day = datetime.datetime.today().strftime("%Y-%m-%d")
  
    today = datetime.datetime.strptime(day,"%Y-%m-%d")

    startDate = request.data['startDate']
    endDate = request.data['endDate']
    if startDate=='no':
        date1 = today
    else:    
        date1 = datetime.datetime.strptime(startDate,"%Y-%m-%d")
    
    if endDate=='no':
        date2 = today
    else:
        date2 = datetime.datetime.strptime(endDate,"%Y-%m-%d")

    print(date1, date2)
    if (date1> date2):
        return Response('bad date formate')

    if date1 and date2 and date1!=date2:
        numberOFSellInBetweenDate = SoldMusics.objects.filter(Q(createdAt__gte=date1) and Q(createdAt__lte=date2)).count()
        sellItemInBetweenDate = SoldMusics.objects.filter(Q(createdAt__gte=date1) and Q(createdAt__lte=date2))
        RevenewInBetweenDate = SoldMusics.objects.filter(Q(createdAt__gte=date1) and Q(createdAt__lte=date2)).aggregate(Sum('music__price'))
    elif date1 and date2 and date1==date2:
        print('else')
        numberOFSellInBetweenDate = SoldMusics.objects.filter(Q(createdAt=date1) ).count()
        sellItemInBetweenDate = SoldMusics.objects.filter(Q(createdAt=date1))
        RevenewInBetweenDate = SoldMusics.objects.filter(Q(createdAt=date1)).aggregate(Sum('music__price'))

    serializer = SoldMusicSerializer(sellItemInBetweenDate, many=True)
    

    return Response({'numberOFSell':numberOFSellInBetweenDate, 'revenue':RevenewInBetweenDate, 'ListOfSoldItem':serializer.data, })
 

@api_view(['GET'])
def getSingleSong(request, id):
    music = Musics.objects.get(id=id)
    serializer = MusicRUDSerializers(music)
    music = serializer.data
    print(music['artist'])
    similarMusic = Musics.objects.filter(Q(artist=music['artist']))
    
    semilarSong = MusicRUDSerializers(similarMusic, many=True)
    print(similarMusic)

    data = {
        'singleSong': serializer.data,
        'similarSong':semilarSong.data
        
        }
    return Response(data)