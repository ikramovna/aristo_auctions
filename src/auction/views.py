from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.auction.filters import AuctionFilter
from src.auction.serializers import *


class ContactAPIView(CreateAPIView):
    """
    API for submitting contact messages.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        """
        Overriding the create method to customize the response message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Contact message submitted successfully!"},
            status=status.HTTP_201_CREATED
        )


class AuctionFavoriteListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows users to create and list their favorite auctions.

    Example request for adding a favorite:
    POST /api/v1/auction/favorites/
    {
        "auction": 1,
        "liked": true
    }

    Example request for listing favorites:
    GET /api/v1/auction/favorites/
    """
    queryset = AuctionFavorite.objects.all()
    serializer_class = AuctionFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return AuctionFavorite.objects.filter(user=user)

    def get_likes_count(self, auction_id):
        return AuctionFavorite.objects.filter(auction_id=auction_id, liked=True).count()

    def post(self, request, *args, **kwargs):
        auction_id = request.data.get('auction')
        user = request.user
        like_value = request.data.get('liked', True)

        if like_value is False:
            AuctionFavorite.objects.filter(auction_id=auction_id, user=user).delete()
            return Response({
                'id': user.id,
                'auction': auction_id,
                'liked': False,
                'message': 'Favorite deleted successfully'
            })

        favorite_instance, created = AuctionFavorite.objects.get_or_create(
            auction_id=auction_id,
            user=user,
            defaults={'liked': like_value}
        )

        if not created and favorite_instance.liked != like_value:
            favorite_instance.liked = like_value
            favorite_instance.save()

        likes_count = self.get_likes_count(auction_id)
        serializer = self.get_serializer(favorite_instance)
        response_data = serializer.data
        response_data['likes_count'] = likes_count
        response_data['message'] = 'Favorite created successfully'
        return Response(response_data)


class RegionListAPIView(ListAPIView):
    """
    API view for get a regions

    Example Request Body:
    """
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer
    permission_classes = (AllowAny,)


class DistrictListAPIView(ListAPIView):
    """
    API view for get a districts

    ## Enter region_id in the url to get the districts in the desired region
    """
    queryset = District.objects.all()
    serializer_class = DistrictModelSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('region_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        region_id = self.request.query_params.get('region_id')
        if region_id:
            self.queryset = self.queryset.filter(region_id=region_id)
        return super().get(request, *args, **kwargs)


class MahallaListAPIView(ListAPIView):
    """
    API view for get a mahallas

    ## Enter district_id in the url to get the mahallas in the desired district
    """
    queryset = Mahalla.objects.all()
    serializer_class = MahallaModelSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('district_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        district_id = self.request.query_params.get('district_id')
        if district_id:
            self.queryset = self.queryset.filter(district_id=district_id)
        return super().get(request, *args, **kwargs)


class FaqAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqModelSerializer
    queryset = Faq.objects.all()

    @swagger_auto_schema(operation_description="Frequently Asked Questions")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AboutAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AboutModelSerializer
    queryset = About.objects.all()

    @swagger_auto_schema(operation_description="About Us")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryListCreateAPIView(ListAPIView):
    """
    API for list category

    Example Request Body:
    """
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)


class CategoryAuctionListView(ListAPIView):
    serializer_class = AuctionListSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return Auction.objects.filter(category_id=category)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuctionDetailView(RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

    def get_object(self):
        # Retrieve the auction and update its status
        auction = get_object_or_404(Auction, id=self.kwargs['auction_id'])
        auction.update_status()
        return auction

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the auction instance
        instance = self.get_object()

        # Increment view count
        instance.view += 1
        instance.save()

        # Prepare bidding history


        # Calculate time difference (Auction end time - current time)
        time_diff = instance.auction_end_date - now()
        end_time = now() + timedelta(days=time_diff.days, seconds=time_diff.seconds)
        time_remaining = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Serialize the auction instance
        serializer = self.get_serializer(instance)
        auction_data = serializer.data

        # Add bidding history and time remaining
        auction_data['time_remaining'] = time_remaining

        # Add additional fields
        additional_data = [{
            "lot_ref_num": instance.lot_ref_num,
            "lot_num_two": instance.lot_num_two,
            "piece_title": instance.piece_title,
            "price": instance.price,
            "dimensions": instance.dimensions,
            "framed_text": instance.framed_text,
            "body_style": instance.body_style,
            "medium": instance.medium,
            "color_scheme": instance.color_scheme,
            "condition": instance.condition,
            "warranty": instance.warranty,
            "date_prod": instance.date_prod,
            "artist_name": instance.artist_name,
            "artist_birth_date": instance.artist_birth_date,
            "artist_death_date": instance.artist_death_date,
        }]
        auction_data['additional_details'] = additional_data

        # Fetch best related auctions
        related_auctions = Auction.objects.filter(
            category_id=instance.category_id,
            auction_end_date__gt=now()
        ).exclude(id=instance.id)[:5]

        # Serialize related auctions
        related_serializer = RelatedAuctionSerializer(related_auctions, many=True)
        auction_data['best_related_auctions'] = related_serializer.data

        return Response(auction_data, status=status.HTTP_200_OK)


class AuctionListView(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer


class FilteredAuctionListView(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('category', openapi.IN_QUERY, description="Category name (case-insensitive)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY,
                              description="Auction status (upcoming, live, completed, cancelled)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('auction_period', openapi.IN_QUERY,
                              description="Auction period (morning, afternoon, evening)", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SearchAuctionByNameView(ListAPIView):
    serializer_class = AuctionListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Auction name to search for",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        name_query = self.request.query_params.get('name', None)
        if not name_query:
            return Response({"error": "The 'name' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Auction.objects.filter(name__icontains=name_query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopAuctionsAPIView(ListAPIView):
    """
    API endpoint to list top auctions where the view count is higher than 30.
    """
    serializer_class = AuctionTopSerilizer

    def get_queryset(self):
        queryset = Auction.objects.filter(view__gt=30, auction_end_date__gt=now())
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class BestArtistAPIView(APIView):
    """
    API to fetch the artist with the highest number of auctions.
    """

    def get(self, request, *args, **kwargs):
        # Aggregate auctions by artist and group them
        best_artist = (
            Auction.objects.values(
                'artist_name', 'artist_birth_date', 'artist_death_date', 'artist_image'
            )
            .annotate(auction_count=Count('id'))  # Group by artist and count auctions
            .order_by('-auction_count')  # Order by the highest number of auctions
            .first()  # Fetch the top artist
        )

        if not best_artist:
            return Response({"message": "No artists found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare response data
        data = {
            "artist_name": best_artist['artist_name'],
            "artist_birth_date": best_artist['artist_birth_date'],
            "artist_death_date": best_artist['artist_death_date'],
            "artist_image": request.build_absolute_uri(best_artist['artist_image']) if best_artist[
                'artist_image'] else None,
            "auction_count": best_artist['auction_count'],
        }

        return Response(data, status=status.HTTP_200_OK)


#  Bid

class PlaceBidAPIView(CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        auction_id = request.data.get('auction')
        auction = Auction.objects.filter(id=auction_id, auction_end_date__gt=now()).first()

        if not auction:
            return Response({"error": "Auction does not exist or has ended."}, status=status.HTTP_400_BAD_REQUEST)

        bid_amount = request.data.get('bid_amount')
        try:
            bid_amount = float(bid_amount)
        except (TypeError, ValueError):
            return Response({"error": "Invalid bid amount."}, status=status.HTTP_400_BAD_REQUEST)

        current_bid = auction.current_bid if auction.current_bid is not None else auction.price
        if bid_amount <= current_bid:
            return Response({"error": "Bid amount must be higher than the current bid or starting price."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create bid
        data = request.data.copy()
        data['auction'] = auction_id  # Add auction ID to the data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update the auction's current bid
        auction.current_bid = bid_amount
        auction.save()

        return Response({"message": "Bid placed successfully!", "bid": serializer.data}, status=status.HTTP_201_CREATED)
