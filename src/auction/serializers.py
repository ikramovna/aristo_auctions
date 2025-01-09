from datetime import timedelta

from rest_framework.serializers import ModelSerializer, SerializerMethodField, HiddenField, CurrentUserDefault, \
    ValidationError, Serializer

from src.auction.models import *
from django.utils.timezone import now, localtime


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message']


class AuctionFavoriteSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = AuctionFavorite
        fields = ('id', 'auction', 'user', 'liked')

    def validate(self, attrs):
        auction = attrs.get('auction')
        user = attrs.get('user')

        if AuctionFavorite.objects.filter(auction=auction, user=user).exists():
            raise ValidationError('You have already added this auction to your favorites.')

        return attrs


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class MahallaModelSerializer(ModelSerializer):
    class Meta:
        model = Mahalla
        fields = ('id', 'name', 'district')


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'region', 'district', 'mahalla', 'house')

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "region": instance.region.name,
            "district": instance.district.name,
            "mahalla": instance.mahalla.name,
            "house": instance.house
        }


class FaqModelSerializer(ModelSerializer):
    class Meta:
        model = Faq
        fields = ('id', 'question', 'answer')


class AboutImageModelSerializer(ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ('id', 'image')


class AboutModelSerializer(ModelSerializer):
    image = AboutImageModelSerializer(many=True)

    class Meta:
        model = About
        fields = ('id', 'title', 'description', 'image')


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class AuctionDetailSerializer(ModelSerializer):
    images = SerializerMethodField()

    class Meta:
        model = Auction
        fields = (
            'id', 'name', 'location', 'current_bid', 'description', 'status', 'images', 'video', 'view')

    def get_images(self, obj):
        base_url = "http://aristoback.ikramovna.me"
        images = []
        if obj.image1:
            images.append(f"{base_url}{obj.image1.url}")
        if obj.image2:
            images.append(f"{base_url}{obj.image2.url}")
        if obj.image3:
            images.append(f"{base_url}{obj.image3.url}")
        if obj.image4:
            images.append(f"{base_url}{obj.image4.url}")
        return images

class AuctionListSerializer(ModelSerializer):
    remaining_time = SerializerMethodField()
    owner_full_name = SerializerMethodField()
    owner_image = SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'image1', 'name', 'price', 'remaining_time', 'owner_full_name', 'owner_image', 'current_bid']

    def get_remaining_time(self, obj):
        remaining_time = obj.get_remaining_time()
        now_time = now()
        end_time = now_time + timedelta(days=remaining_time['days'], hours=remaining_time['hours'],
                                        minutes=remaining_time['minutes'], seconds=remaining_time['seconds'])
        return end_time.strftime('%Y-%m-%dT%H:%M:%S')

    def get_owner_full_name(self, obj):
        return obj.artist_name

    def get_owner_image(self, obj):
        return obj.artist_image.url if obj.artist_image else None


class AuctionTopSerilizer(ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'image1', 'image2', 'name', 'price', 'status', 'view']


class RelatedAuctionSerializer(ModelSerializer):
    auction_end_date = SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'image1', 'name', 'lot_ref_num', 'price', 'auction_end_date']

    def get_auction_end_date(self, obj):
        return localtime(obj.auction_end_date).strftime('%Y-%m-%dT%H:%M:%S')


class BestArtistSerializer(Serializer):
    artist_name = CharField()
    artist_birth_date = DateField()
    artist_death_date = DateField()
    artist_image = ImageField()
    auction_count = IntegerField()


# Bid

class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'name', 'description', 'price', 'current_bid', 'image1', 'auction_end_date']


class BidSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'bid_amount', 'bid_time']
