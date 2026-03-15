from abc import ABC, abstractmethod
from typing import Optional
import requests
import time
from logging import getLogger



logger = getLogger("AntonIA.publisher")

class PublisherClient(ABC):
    """
    Abstract base class for publishing images to various social media platforms.
    """

    @abstractmethod
    def publish(self, image_path: str, caption: Optional[str] = None, **kwargs) -> bool:
        """
        Publish an image to the platform.

        Args:
            image_path (str): Path to the image file to publish.
            caption (Optional[str]): Caption or message to accompany the image.
            **kwargs: Additional platform-specific parameters.

        Returns:
            bool: True if publication was successful, False otherwise.
        """
        pass


class InstagramPublisher(PublisherClient):
    """
    Publisher client for Instagram using Facebook Graph API.
    """

    def __init__(
            self,
            access_token: str,
            instagram_account_id: str,
            base_image_url: str,
            ):
        """
        Initialize the Instagram publisher.

        Args:
            access_token (str): Facebook Graph API access token.
            instagram_account_id (str): Instagram business account ID.
            base_image_url (str): Base URL for accessing the images (e.g., local server or cloud storage).
        """
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_image_url = base_image_url
        self.base_url = "https://graph.facebook.com/v18.0"

    def _full_image_url(self, image_path: str) -> str:
        """
        Construct the full URL for the image based on the base_image_url and the provided image_path.

        Args:
            image_path (str): The relative path to the image.

        Returns:
            str: The full URL for the image.
        """
        return f"{self.base_image_url}/{image_path}" if self.base_image_url else image_path

    def publish(self, image_path: str, caption: Optional[str] = None, **kwargs) -> bool:
        """
        Publish an image to Instagram.

        Args:
            image_path (str): Path to the image file.
            caption (Optional[str]): Caption for the post.
            **kwargs: Additional parameters.

        Returns:
            bool: True if published successfully.
        """
        # Step 1: Upload the image
        create_url  = f"{self.base_url}/{self.instagram_account_id}/media"

        logger.info(f"Uploading image to Instagram (id: {self.instagram_account_id}): {self.base_image_url}/{image_path} with caption: {caption}")
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        payload = {
            "image_url": self._full_image_url(image_path),
            "caption": caption
        }

        response = requests.post(create_url , headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to upload media: {response.text}")
        
        creation_id = response.json()['id']

        time.sleep(2)  # Wait for container to be ready

        # Step 2: Publish the media
        publish_url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
        payload = {
            "creation_id": creation_id
        }
        response = requests.post(publish_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Failed to publish media: {response.text}")
        
        return response.status_code == 200


class WhatsAppPublisher(PublisherClient):
    """
    Publisher client for WhatsApp using WhatsApp Business API.
    """

    def __init__(self, access_token: str, phone_number_id: str):
        """
        Initialize the WhatsApp publisher.

        Args:
            access_token (str): WhatsApp Business API access token.
            phone_number_id (str): WhatsApp phone number ID.
        """
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"

    def publish(self, image_path: str, caption: Optional[str] = None, recipient: str = None, **kwargs) -> bool:
        """
        Send an image via WhatsApp.

        Args:
            image_path (str): Path to the image file.
            caption (Optional[str]): Caption for the image.
            recipient (str): Recipient's phone number (required).
            **kwargs: Additional parameters.

        Returns:
            bool: True if sent successfully.
        """
        if not recipient:
            raise ValueError("Recipient phone number is required for WhatsApp publishing.")

        # Upload media first
        media_url = f"{self.base_url}/{self.phone_number_id}/media"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'type': 'image/jpeg'}  # Adjust based on image type
            response = requests.post(media_url, headers=headers, files=files, data=data)
            if response.status_code != 200:
                return False
            media_id = response.json()['id']

        # Send message with media
        message_url = f"{self.base_url}/{self.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "image",
            "image": {
                "id": media_id,
                "caption": caption
            }
        }
        response = requests.post(message_url, headers=headers, json=payload)
        return response.status_code == 200