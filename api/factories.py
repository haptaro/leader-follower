import factory
from django.contrib.auth.models import User
from api.models import UserMetadata


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        password = extracted or "defaultpassword123"
        self.set_password(password)
        self.save()


class UserMetadataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserMetadata
    
    user = factory.SubFactory(UserFactory)
    access_token = factory.LazyFunction(lambda: UserMetadata().generate_token())
