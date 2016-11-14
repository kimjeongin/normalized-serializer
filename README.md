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
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "post": [
        {
            "id": 1,
            "title": "asdf",
            "replies": [
                1,
                3
            ],
            "user": 1
        },
        {
            "id": 2,
            "title": "asdf",
            "replies": [
                2
            ],
            "user": 2
        }
    ],
    "replies": [
        {
            "id": 1,
            "content": "asdf",
            "user": 1
        },
        {
            "id": 2,
            "content": "asdfasfda",
            "user": 1
        },
        {
            "id": 3,
            "content": "asfdasdfafsadf",
            "user": 3
        }
    ],
    "user": [
        {
            "id": 1,
            "name": "aaa",
            "nickname": "abc"
        },
        {
            "id": 2,
            "name": "aaa",
            "nickname": "abc"
        },
        {
            "id": 3,
            "name": "aaa",
            "nickname": "abc"
        }
    ]
}
```
* Post Instance
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS

{
    "post": [
        {
            "id": 1,
            "title": "asdf",
            "replies": [
                1,
                3
            ],
            "user": 1
        }
    ],
    "replies": [
        {
            "id": 1,
            "content": "asdf",
            "user": 1
        },
        {
            "id": 3,
            "content": "asfdasdfafsadf",
            "user": 3
        }
    ],
    "user": [
        {
            "id": 1,
            "name": "aaa",
            "nickname": "abc"
        },
        {
            "id": 3,
            "name": "aaa",
            "nickname": "abc"
        }
    ]
}
```



