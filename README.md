# Normalized serializer #

### What is this repository for? ###

* Change nested serializer to normalized serializer
* Version 0.1.0

### Installation ###

Install using `pip`...

    pip install https://github.com/kimjeongin/normalized-serializer.git

### Example ###

```python
from normalized.serializers import NormalizedSerializer, NormalizedListSerializer

class PostUserSerializer(NormalizedSerializer):

    class Meta:
        model = PostUser
        list_serializer_class = NormalizedListSerializer
        fields = ('id', 'name', 'nickname')
        normalized_fields = ["user"]


class PostReplySerializer(NormalizedSerializer):
    user = PostUserSerializer()

    class Meta:
        model = PostReply
        list_serializer_class = NormalizedListSerializer
        fields = ('id', 'content', 'user')
        normalized_fields = ["replies"]

class PostSerializer(NormalizedSerializer):
    replies = PostReplySerializer(many=True)
    user = PostUserSerializer()

    class Meta:
        model = Post
        list_serializer_class = NormalizedListSerializer
        fields = ('id','title', 'replies', 'user')
        model_name = "post"
        normalized_fields = ["replies", "user"]
```

### Result ###

* Post List

* Post Instance

