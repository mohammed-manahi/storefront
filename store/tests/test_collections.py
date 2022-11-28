""" Test for collections endpoint where directory, file and method names are conventions """
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCreateCollection():
    """ Test cases for creating a collection for collections endpoint """

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
