# models.py
class Tag(models.Model):
    image = models.ImageField(upload_to='tag_images', null=True, blank=True)

class Record(models.Model):
    file = models.FileField(upload_to='record_files', null=True, blank=True)

class Weight(models.Model):
    record = models.ForeignKey(
        Record,
        related_name='weights',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        related_name='weights',
        on_delete=models.CASCADE
    )
    value = models.IntegerField()

    class Meta:
        unique_together = ('record', 'tag',)

# serializers.py
class RecordSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ('id', 'file', 'tags')

    def get_tags(self, obj):
        return TagSerializer(Tag.objects.filter(weights__in=obj.weights.all()), many=True).data

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'image')

# record results
{
    "id": 1,
    "file": "http://127.0.0.1:8080/media/record_files/record00.mp3",
    "tags": [
        {
            "id": 4,
            "image": "/media/tag_images/image04.jpg"
        },
        {
            "id": 10,
            "image": "/media/tag_images/image10.jpg"
        }
    ]
}

# tags results
[
    {
        "id": 4,
        "image": "http://127.0.0.1:8080/media/tag_images/image04.jpg"
    },
    {
        "id": 10,
        "image": "http://127.0.0.1:8080/media/tag_images/image10.jpg"
    }
]