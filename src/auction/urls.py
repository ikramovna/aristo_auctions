from django.urls import path

from src.auction.views import *

urlpatterns = [
    # path("regions", RegionListAPIView.as_view(), name="region-list"),
    # path("districts", DistrictListAPIView.as_view(), name="district-list"),
    # path("mahallas", MahallaListAPIView.as_view(), name="mahalla-list"),
    path("faq", FaqAPIView.as_view(), name='faq'),
    path("about", AboutAPIView.as_view(), name='about'),
    path("category", CategoryListCreateAPIView.as_view(), name='category'),
    path('category/<int:category_id>', CategoryAuctionListView.as_view(), name='category'),
    path('list', AuctionListView.as_view(), name='list'),
    path('<int:auction_id>', AuctionDetailView.as_view(), name='detail'),
    path('filter', FilteredAuctionListView.as_view(), name='filter'),
    path('search', SearchAuctionByNameView.as_view(), name='search'),
    path('favorites', AuctionFavoriteListCreateAPIView.as_view(), name='favorites'),
    path('top', TopAuctionsAPIView.as_view(), name='top'),
    path('contact', ContactAPIView.as_view(), name='contact'),
    path('bid', PlaceBidAPIView.as_view(), name='bid'),
    path('best-artist', BestArtistAPIView.as_view(), name='best-artist'),

]
