import pytest
from datetime import datetime, timedelta
from django.utils.timezone import now
from src.auction.models import (
    Contact, AuctionFavorite, Faq, AboutImage, About, Region, District, Mahalla,
    Address, Category, Auction, Bid
)
from src.users.models import User


@pytest.mark.django_db
def test_contact_model():
    contact = Contact.objects.create(name="John Doe", email="johndoe@example.com", message="Hello!")
    assert str(contact) == "John Doe - johndoe@example.com"
    assert contact.created_at is not None


@pytest.mark.django_db
def test_auction_favorite_model():
    user = User.objects.create(username="testuser", email="testuser@example.com")
    category = Category.objects.create(name="Art")
    auction = Auction.objects.create(
        name="Test Auction",
        location="Test Location",
        lot_ref_num="LOT12345",
        lot_num_two="01",
        piece_title="Test Piece",
        price=100,
        auction_start_date=now(),
        auction_end_date=now() + timedelta(days=1),
        category_id=category,
        owner=user
    )
    favorite = AuctionFavorite.objects.create(auction=auction, user=user, liked=True)
    assert str(favorite) == "testuser - Test Auction"
    assert favorite.liked is True


@pytest.mark.django_db
def test_bid_model():
    # Create a user
    user = User.objects.create(username="testuser", email="testuser@example.com")

    # Create a category
    category = Category.objects.create(name="Art")

    # Create an auction with a valid category
    auction = Auction.objects.create(
        name="Test Auction",
        location="Test Location",
        lot_ref_num="LOT12345",
        lot_num_two="01",
        piece_title="Test Piece",
        price=100,
        auction_start_date=now(),
        auction_end_date=now() + timedelta(days=1),
        category_id=category,  # Assign the created category
        owner=user
    )

    # Create a bid
    bid = Bid.objects.create(auction=auction, user=user, bid_amount=150.00)

    # Assert that the bid is created correctly
    assert str(bid) == "testuser - 150.00"


@pytest.mark.django_db
def test_region_model():
    region = Region.objects.create(name="Tashkent")
    assert str(region) == "Tashkent"


@pytest.mark.django_db
def test_district_model():
    region = Region.objects.create(name="Tashkent")
    district = District.objects.create(name="Yunusabad", region=region)
    assert str(district) == "Yunusabad"
    assert district.region == region


@pytest.mark.django_db
def test_mahalla_model():
    region = Region.objects.create(name="Tashkent")
    district = District.objects.create(name="Yunusabad", region=region)
    mahalla = Mahalla.objects.create(name="Mahalla 1", district=district)
    assert str(mahalla) == "Mahalla 1"
    assert mahalla.district == district


@pytest.mark.django_db
def test_address_model():
    region = Region.objects.create(name="Tashkent")
    district = District.objects.create(name="Yunusabad", region=region)
    mahalla = Mahalla.objects.create(name="Mahalla 1", district=district)
    address = Address.objects.create(region=region, district=district, mahalla=mahalla, house="123")
    assert str(address) == "Tashkent Yunusabad Mahalla 1 123"


@pytest.mark.django_db
def test_category_model():
    category = Category.objects.create(name="Art")
    assert str(category) == "Art"


@pytest.mark.django_db
def test_auction_model_update_status():
    user = User.objects.create(username="testuser", email="testuser@example.com")
    category = Category.objects.create(name="Art")
    auction = Auction.objects.create(
        name="Test Auction",
        location="Test Location",
        lot_ref_num="LOT12345",
        lot_num_two="01",
        piece_title="Test Piece",
        price=100,
        auction_start_date=now() - timedelta(days=1),
        auction_end_date=now() + timedelta(days=1),
        category_id=category,
        owner=user,
    )
    auction.update_status()
    assert auction.status == Auction.StatusChoices.LIVE


@pytest.mark.django_db
def test_bid_model():
    user = User.objects.create(username="testuser", email="testuser@example.com")
    category = Category.objects.create(name="Art")
    auction = Auction.objects.create(
        name="Test Auction",
        location="Test Location",
        lot_ref_num="LOT12345",
        lot_num_two="01",
        piece_title="Test Piece",
        price=100,
        auction_start_date=now(),
        auction_end_date=now() + timedelta(days=1),
        category_id=category,  # Assign the created category
        owner=user
    )
    bid = Bid.objects.create(auction=auction, user=user, bid_amount=150.00)
    assert str(bid) == "testuser - 150.00"