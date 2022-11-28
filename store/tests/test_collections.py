""" Test for collections endpoint where directory, file and method names are conventions """
from django.contrib.auth.models import User
from store.models import Collection
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestCreateCollection():
    """ Test cases for creating a collection for collections endpoint """

    @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self):
        # Test workflow consists of three parts arrange, act and assert actions
        # Arrange:
        # Nothing to arrange since this test is for creation
        # Act:
        api_client = APIClient()
        # Ensure that the url starts with / in the http method
        response = api_client.post("/store/collections/", {"title": "new collection"})
        # Assert:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):
        # Arrange:
        # Nothing to arrange since this test is for creation
        # Act:
        api_client = APIClient()
        # Test using authenticated user
        api_client.force_authenticate(user={})
        # Ensure that the url starts with / in the http method
        response = api_client.post("/store/collections/", {"title": "new collection"})
        # Assert:
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        # Arrange:
        # Nothing to arrange since this test is for creation
        # Act:
        api_client = APIClient()
        # Test using authenticated admin user
        api_client.force_authenticate(user=User(is_staff=True))
        # Set invalid title to test invalid data test case
        response = api_client.post("/store/collections/", {"title": ""})
        # Assert:
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self):
        # Arrange:
        # Nothing to arrange since this test is for creation
        # Act:
        api_client = APIClient()
        # Test using authenticated admin user
        api_client.force_authenticate(user=User(is_staff=True))
        # Set invalid title to test invalid data test case
        response = api_client.post("/store/collections/", {"title": "new collection"})
        # Assert:
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollection():
    """ Test cases for retrieving a collection for collections endpoint """

    def test_if_collection_exists_returns_200(self):
        # Arrange:
        # Collection.objects.create(title="new collection")
        # Instead of creating model instance manually, model bakery provides a better approach
        collection = baker.make(Collection)
        # Act:
        api_client = APIClient()
        api_client.force_authenticate(user=User(is_staff=True))
        # Get the id of the collection created by model bakery
        response = api_client.get(f"/store/collections/{collection.id}/")
        # Assert:
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"id": collection.id, "title": collection.title, "product_count": 0}
