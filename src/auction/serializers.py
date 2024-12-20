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
    class Meta:
        model = Auction
        fields = (
            'id', 'name', 'location', 'current_bid', 'description', 'status', 'image1', 'image2', 'image3', 'image4',
            'video', 'view')


class AuctionListSerializer(ModelSerializer):
    remaining_time = SerializerMethodField()
    owner_full_name = SerializerMethodField()
    owner_image = SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'image1', 'name', 'price', 'remaining_time', 'owner_full_name', 'owner_image']

    def get_remaining_time(self, obj):
        remaining_time = obj.get_remaining_time()
        return f"{remaining_time['days']}D : {remaining_time['hours']}H : {remaining_time['minutes']}M : {remaining_time['seconds']}S"

    def get_owner_full_name(self, obj):
        return obj.owner.full_name if obj.owner else None

    def get_owner_image(self, obj):
        return obj.owner.image.url if obj.owner and obj.owner.image else None


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
        return localtime(obj.auction_end_date).strftime('%Y-%m-%d, %H:%M')


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
