"""Face Authentication module"""
import json
import requests
from bs4 import BeautifulSoup


class FaceAuthentication:
    """This class is a wrapper for the YooniK Web Product, an API for face authentication.
    """
    def __init__(self, api_url: str, api_key: str):
        """
        :param api_url:
        :param api_key:
        """
        self.api_url = api_url
        self.api_key = api_key

        self.status = None
        self.message_class = None
        self.message = None

    @staticmethod
    def allowed_base64_image(image: str) -> bool:
        """Check if base64 image has an allowed format.
        :param image:
        :return:
        """
        if not image.startswith('data:image/'):
            return False
        return image[11:14] in {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def parse_response_error(html_text: str, extra_response_codes: dict = None) -> str:
        """Parse HTML error response
        :param html_text:
            HTML error message.
        :param extra_response_codes:
            Dictionary with additional response codes and description pairs, to search on html_text.
        :return:
            Parsed error message.
        """
        message = ''
        html = BeautifulSoup(markup=html_text, features="html.parser")
        if html.p:
            inner_html = BeautifulSoup(markup=html.p.text, features="html.parser")
            message = inner_html.text if inner_html.p is None else inner_html.p.text

        if "face_not_found" in message:
            message = "Could not find a face in the image."
        elif "multiple_faces" in message:
            message = "The image has more than one person."
        elif "quality_failed" in message:
            message = "The provided image does not have enough quality."
        elif extra_response_codes:
            for code in extra_response_codes:
                if code in message:
                    message = extra_response_codes[code]
                    break
        else:
            message = "An error occurred. Please contact your systems administrator."
            print(f"ERROR: {html.text}")
        return message

    @staticmethod
    def parse_response_status(status: str) -> str:
        """Create a message from the response status data
        :param status:
            Status of the operation.
        :return:
            Resulting message to be sent to the UI.
        """
        message = status
        if status == 'SUCCESS':
            message = "Face authentication successful"
        elif status == 'NEW_USER':
            message = "Face signup successful"
        elif status == 'USER_NOT_FOUND':
            message = "User not registered"
        elif status == 'FAILED':
            message = "Face authentication failed"
        return message

    def request_face_authentication(self, user_id: str, user_photo: str,
                                    user_attributes: dict = None, create_if_new: bool = True):
        """
        :param user_id:
        :param user_photo:
        :param user_attributes
        :param create_if_new:
        :return:
        """
        self.status = 'FAILED'
        self.message_class = 'text-danger'
        self.message = 'Face authentication failed'

        if self.allowed_base64_image(user_photo):
            yoonik_request_data = {
                'user_id': user_id,
                'user_photo': user_photo.split('base64,')[1],
                'user_attributes': user_attributes,
                'create_if_new': create_if_new
            }
            response = requests.post(
                self.api_url,
                headers={'x-api-key': self.api_key},
                json=yoonik_request_data
            )
            if response.ok:
                result = json.loads(response.text)
                self.status = result['status']
                self.message_class = 'text-success' if self.status == 'SUCCESS' or self.status == 'NEW_USER' else 'text-danger'
                self.message = self.parse_response_status(self.status)
            else:
                self.message = f'Ups! {self.parse_response_error(response.text)}'

    def request_account_deletion(self, user_id: str) -> bool:
        """
        :param user_id:
        :return:
        """
        response = requests.delete(
            self.api_url,
            headers={'x-api-key': self.api_key},
            json={'user_id': user_id}
        )
        return response.ok
