import os
import pytest
from unittest.mock import patch, MagicMock
from AntonIA.services.publisher_client import InstagramPublisher


@pytest.fixture
def instagram_api_id():
    return os.getenv("ANTONIA_BUENOS_DIAS_INSTAGRAM_API_ID")


@pytest.fixture
def instagram_api_token():
    return os.getenv("ANTONIA_BUENOS_DIAS_INSTAGRAM_API_TOKEN")


@pytest.fixture
def sample_image_path():
    return r"C:\Users\cmolins\Desktop\AntonIA\outputs\images\20251006_234241_0aad063a.png"


@pytest.fixture
def instagram_publisher(instagram_api_token, instagram_api_id):
    if not instagram_api_token or not instagram_api_id:
        pytest.skip("Instagram API credentials not configured")
    return InstagramPublisher(access_token=instagram_api_token, instagram_account_id=str(instagram_api_id))


def test_instagram_publisher_initialization(instagram_publisher):
    assert instagram_publisher.access_token is not None
    assert instagram_publisher.instagram_account_id is not None
    assert instagram_publisher.base_url == "https://graph.facebook.com/v18.0"


@patch('requests.post')
def test_instagram_publisher_publish_success(mock_post, instagram_publisher, sample_image_path):
    # Mock the upload response
    upload_response = MagicMock()
    upload_response.status_code = 200
    upload_response.json.return_value = {'id': 'test_creation_id'}

    # Mock the publish response
    publish_response = MagicMock()
    publish_response.status_code = 200

    # Configure mock to return different responses for different calls
    mock_post.side_effect = [upload_response, publish_response]

    result = instagram_publisher.publish(image_path=sample_image_path, caption="Test caption")

    assert result is True
    assert mock_post.call_count == 2

    # Check upload call
    upload_call = mock_post.call_args_list[0]
    assert 'media' in upload_call[0][0]
    assert 'caption' in upload_call[1]['data']

    # Check publish call
    publish_call = mock_post.call_args_list[1]
    assert 'media_publish' in publish_call[0][0]
    assert publish_call[1]['json']['creation_id'] == 'test_creation_id'


@patch('requests.post')
def test_instagram_publisher_publish_upload_failure(mock_post, instagram_publisher, sample_image_path):
    # Mock upload failure
    upload_response = MagicMock()
    upload_response.status_code = 400
    mock_post.return_value = upload_response

    result = instagram_publisher.publish(image_path=sample_image_path, caption="Test caption")

    assert result is False
    mock_post.assert_called_once()


@patch('requests.post')
def test_instagram_publisher_publish_publish_failure(mock_post, instagram_publisher, sample_image_path):
    # Mock successful upload
    upload_response = MagicMock()
    upload_response.status_code = 200
    upload_response.json.return_value = {'id': 'test_creation_id'}

    # Mock publish failure
    publish_response = MagicMock()
    publish_response.status_code = 400

    mock_post.side_effect = [upload_response, publish_response]

    result = instagram_publisher.publish(image_path=sample_image_path, caption="Test caption")

    assert result is False
    assert mock_post.call_count == 2