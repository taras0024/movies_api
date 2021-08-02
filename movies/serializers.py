from rest_framework import serializers

from movies.models import Actor, Movie, Review, Rating


class ActorListSerializer(serializers.ModelSerializer):
    """Get actors list"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Get actor details"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """List of movies"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """Filter review, only parent"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """ Show child comment"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Show review"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'parent', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Movie detail"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)  # named like related_name
    # directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    directors = ActorListSerializer(read_only=True, many=True)
    # actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    # genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Add rating"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
