from django.urls import path

from src.auction.views import *

urlpatterns = [
    path("region", RegionListAPIView.as_view()),
    path("district", DistrictListAPIView.as_view()),
    path("mahalla", MahallaListAPIView.as_view()),
    path("faq", FaqAPIView.as_view()),
    path("about", AboutAPIView.as_view()),
    path("category", CategoryListCreateAPIView.as_view()),
    path('category/<int:category_id>', CategoryAuctionListView.as_view()),
    path('list', AuctionListView.as_view()),
    path('<int:auction_id>', AuctionDetailView.as_view()),
    path('filter', FilteredAuctionListView.as_view()),
    path('search', SearchAuctionByNameView.as_view()),
    path('favorites', AuctionFavoriteListCreateAPIView.as_view()),
    path('top', TopAuctionsAPIView.as_view()),
    path('contact', ContactAPIView.as_view()),
    path('bid', PlaceBidAPIView.as_view()),
    path('best-artist', BestArtistAPIView.as_view()),

]
