import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from src.auction.models import Contact, AuctionFavorite, Region, District, Mahalla, Category, Auction, Bid
from src.users.models import User
from datetime import timedelta
from django.utils.timezone import now


@pytest.fixture
def api_client():
    return APIClient()


import uuid

@pytest.fixture
def create_user():
    def _create_user(email=None, password="password123", username=None, full_name="Test User"):
        if not email:
            email = f"testuser-{uuid.uuid4()}@example.com"  # Generate a unique email
        if not username:
            username = f"testuser-{uuid.uuid4()}"  # Generate a unique username
        return User.objects.create_user(email=email, password=password, username=username, full_name=full_name)
    return _create_user



@pytest.fixture
def create_auction(create_user):
    def _create_auction():
        category = Category.objects.create(name="Art")
        user = create_user()
        return Auction.objects.create(
            name="Test Auction",
            location="Test Location",
            lot_ref_num="LOT123",
            lot_num_two="01",
            piece_title="Test Piece",
            price=100,
            auction_start_date=now(),
            auction_end_date=now() + timedelta(days=1),
            category_id=category,
            owner=user
        )
    return _create_auction


### Tests for ContactAPIView
@pytest.mark.django_db
def test_contact_api_view(api_client):
    url = reverse('contact')
    data = {"name": "John Doe", "email": "johndoe@example.com", "message": "Hello!"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Contact.objects.count() == 1


### Tests for AuctionFavoriteListCreateAPIView
@pytest.mark.django_db
def test_auction_favorite_list_create(api_client, create_user, create_auction):
    user = create_user()
    auction = create_auction()
    api_client.force_authenticate(user=user)

    # Add a favorite
    url = reverse('favorites')
    data = {"auction": auction.id, "liked": True}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert AuctionFavorite.objects.count() == 1

    # List favorites
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_region_list_api_view(api_client):
    Region.objects.create(name="Tashkent")
    url = reverse('region-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_district_list_api_view(api_client):
    region = Region.objects.create(name="Tashkent")
    District.objects.create(name="Yunusabad", region=region)
    url = reverse('district-list')
    response = api_client.get(url, {"region_id": region.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_mahalla_list_api_view(api_client):
    region = Region.objects.create(name="Tashkent")
    district = District.objects.create(name="Yunusabad", region=region)
    Mahalla.objects.create(name="Mahalla 1", district=district)
    url = reverse('mahalla-list')
    response = api_client.get(url, {"district_id": district.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1



### Tests for CategoryListCreateAPIView
@pytest.mark.django_db
def test_category_list_api_view(api_client):
    url = reverse('category')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


### Tests for AuctionDetailView
@pytest.mark.django_db
def test_auction_detail_view(api_client, create_auction):
    auction = create_auction()
    url = reverse('detail', kwargs={'auction_id': auction.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == auction.name


### Tests for PlaceBidAPIView
@pytest.mark.django_db
def test_place_bid_api_view(api_client, create_user, create_auction):
    user = create_user()
    auction = create_auction()
    api_client.force_authenticate(user=user)

    url = reverse('bid')
    data = {"auction": auction.id, "bid_amount": 150.00}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Bid.objects.count() == 1


### Tests for TopAuctionsAPIView
@pytest.mark.django_db
def test_top_auctions_api_view(api_client, create_auction):
    auction = create_auction()
    auction.view = 50
    auction.save()

    url = reverse('top')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


### Tests for BestArtistAPIView
@pytest.mark.django_db
def test_best_artist_api_view(api_client, create_auction):
    auction = create_auction()
    auction.artist_name = "Famous Artist"
    auction.save()

    url = reverse('best-artist')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["artist_name"] == "Famous Artist"
