import whop.whopclient as whopclient
from whop.whopclient.api import (
    products_api,
    notifications_api,
    links_api,
    licenses_api,
    checkout_logs_api,
)


from whop.whopclient.model.create_product_request import CreateProductRequest
from whop.whopclient.model.confirm_product_request import ConfirmProductRequest
from whop.whopclient.model.send_push_notification_request import SendPushNotificationRequest

from whop.whopclient.model.create_link_request import CreateLinkRequest
from whop.whopclient.model.validate_license_by_key_request import ValidateLicenseByKeyRequest
from whop.whopclient.model.update_license_by_key_request import UpdateLicenseByKeyRequest
from whop.whopclient.model.reset_license_by_key_request import ResetLicenseByKeyRequest


from whop.whopclient.model.ban_license_by_key_request import BanLicenseByKeyRequest

from whop.whopclient.model.create_checkout_log_request import CreateCheckoutLogRequest
from whop.whopclient.model.create_link_request import CreateLinkRequest
from whop.whopclient.model.error_response import ErrorResponse
from whop.static.internal_utils import _remove_none_values
from typing import Optional
import json


class Whop:
    def __init__(self, bearer):
        self.api_client = whopclient.ApiClient(
            whopclient.Configuration(access_token=bearer)
        )

    def get_products(self, **kwargs):
        # Fetch All Products
        try:
            client = whopclient.api.products_api.ProductsApi(self.api_client)

            resp = client.get_products(**kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def get_product_by_id(self, id: int, **kwargs):
        # Fetch Product
        try:
            client = whopclient.api.products_api.ProductsApi(self.api_client)

            resp = client.get_product_by_id(id, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def create_product(
        self,
        custom_trial_period: Optional[int] = None,
        expiration_days: Optional[int] = None,
        initial_price: Optional[float] = None,
        license_type: Optional[str] = None,
        title: Optional[str] = None,
        currency: Optional[str] = None,
        cancel_action: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        transferable: Optional[bool] = None,
        billing_period: Optional[int] = None,
        **kwargs
    ):
        # Create Product
        try:
            client = whopclient.api.products_api.ProductsApi(self.api_client)
            body_kwargs = {
                "custom_trial_period": custom_trial_period,
                "expiration_days": expiration_days,
                "initial_price": initial_price,
                "license_type": license_type,
                "title": title,
                "currency": currency,
                "cancel_action": cancel_action,
                "price": price,
                "stock": stock,
                "transferable": transferable,
                "billing_period": billing_period,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = CreateProductRequest(**body_kwargs)

            resp = client.create_product(create_product_request=req, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def confirm_product(
        self,
        billing_period: Optional[int] = None,
        cancel_action: Optional[str] = None,
        custom_trial_period: Optional[int] = None,
        initial_price: Optional[float] = None,
        title: Optional[str] = None,
        currency: Optional[str] = None,
        expiration_days: Optional[int] = None,
        license_type: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        transferable: Optional[bool] = None,
        **kwargs
    ):
        # Product Creation Confirmation
        try:
            client = whopclient.api.products_api.ProductsApi(self.api_client)
            body_kwargs = {
                "billing_period": billing_period,
                "cancel_action": cancel_action,
                "custom_trial_period": custom_trial_period,
                "initial_price": initial_price,
                "title": title,
                "currency": currency,
                "expiration_days": expiration_days,
                "license_type": license_type,
                "price": price,
                "stock": stock,
                "transferable": transferable,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = ConfirmProductRequest(**body_kwargs)

            resp = client.confirm_product(confirm_product_request=req, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def send_push_notification(
        self,
        body: Optional[str] = None,
        link: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ):
        # Send a push notification
        try:
            client = whopclient.api.notifications_api.NotificationsApi(self.api_client)
            body_kwargs = {
                "body": body,
                "link": link,
                "title": title,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = SendPushNotificationRequest(**body_kwargs)

            resp = client.send_push_notification(
                send_push_notification_request=req, **kwargs
            )
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def get_links(self, **kwargs):
        # Fetch Links
        try:
            client = whopclient.api.links_api.LinksApi(self.api_client)

            resp = client.get_links(**kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def create_link(
        self,
        discord_ids: Optional[list] = None,
        password: Optional[str] = None,
        product_id: Optional[int] = None,
        stock: Optional[int] = None,
        **kwargs
    ):
        # Create Password Protected Link
        try:
            client = whopclient.api.links_api.LinksApi(self.api_client)
            body_kwargs = {
                "discord_ids": discord_ids,
                "password": password,
                "product_id": product_id,
                "stock": stock,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = CreateLinkRequest(**body_kwargs)

            resp = client.create_link(create_link_request=req, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def validate_license_by_key(
        self, key: str, metadata: Optional[dict] = None, **kwargs
    ):
        # Validate Key
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)
            body_kwargs = {
                "metadata": metadata,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = ValidateLicenseByKeyRequest(**body_kwargs)

            resp = client.validate_license_by_key(
                key, validate_license_by_key_request=req, **kwargs
            )
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def update_license_by_key(
        self, key: str, metadata: Optional[dict] = None, **kwargs
    ):
        # Update License
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)
            body_kwargs = {
                "metadata": metadata,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = UpdateLicenseByKeyRequest(**body_kwargs)

            resp = client.update_license_by_key(
                key, update_license_by_key_request=req, **kwargs
            )
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def reset_license_by_key(self, key: str, metadata: Optional[dict] = None, **kwargs):
        # Reset License
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)
            body_kwargs = {
                "metadata": metadata,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = ResetLicenseByKeyRequest(**body_kwargs)

            resp = client.reset_license_by_key(
                key, reset_license_by_key_request=req, **kwargs
            )
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def get_licenses(
        self,
        discord_account_id: Optional[str] = None,
        page: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kwargs
    ):
        # Fetch All Licenses
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)
            kwargs.update(
                {
                    "discord_account_id": discord_account_id,
                    "page": page,
                    "start": start,
                    "end": end,
                }
            )

            kwargs = _remove_none_values(kwargs)

            resp = client.get_licenses(**kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def get_license_by_key(self, key: str, **kwargs):
        # Fetch License
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)

            resp = client.get_license_by_key(key, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def ban_license_by_key(self, key: str, metadata: Optional[dict] = None, **kwargs):
        # Ban License
        try:
            client = whopclient.api.licenses_api.LicensesApi(self.api_client)
            body_kwargs = {
                "metadata": metadata,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = BanLicenseByKeyRequest(**body_kwargs)

            resp = client.ban_license_by_key(
                key, ban_license_by_key_request=req, **kwargs
            )
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def get_checkout_logs(
        self, key: Optional[str] = None, status: Optional[str] = None, **kwargs
    ):
        # Fetch Checkout Logs
        try:
            client = whopclient.api.checkout_logs_api.CheckoutLogsApi(self.api_client)
            kwargs.update(
                {
                    "key": key,
                    "status": status,
                }
            )

            kwargs = _remove_none_values(kwargs)

            resp = client.get_checkout_logs(**kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )

    def create_checkout_log(
        self,
        image_url: Optional[str] = None,
        key: Optional[str] = None,
        price: Optional[float] = None,
        product_name: Optional[str] = None,
        size: Optional[int] = None,
        status: Optional[str] = None,
        website: Optional[str] = None,
        **kwargs
    ):
        # Add Checkout Log
        try:
            client = whopclient.api.checkout_logs_api.CheckoutLogsApi(self.api_client)
            body_kwargs = {
                "image_url": image_url,
                "key": key,
                "price": price,
                "product_name": product_name,
                "size": size,
                "status": status,
                "website": website,
            }

            body_kwargs = _remove_none_values(body_kwargs)
            req = CreateCheckoutLogRequest(**body_kwargs)

            resp = client.create_checkout_log(create_checkout_log_request=req, **kwargs)
            return resp
        except Exception as e:
            err_resp = json.loads(e.body)
            return ErrorResponse(
                success=err_resp["success"],
                message=err_resp["message"],
                errors=err_resp["errors"],
            )
