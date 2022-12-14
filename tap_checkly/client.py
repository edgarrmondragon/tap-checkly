"""REST client handling, including ChecklyStream base class."""

from __future__ import annotations

import json
import sys
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from singer_sdk import RESTStream
from singer_sdk._singerlib import resolve_schema_references
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BasePageNumberPaginator, first

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

if TYPE_CHECKING:
    from requests import Response

PAGE_SIZE = 100


class ChecklyPaginator(BasePageNumberPaginator):
    """Checkly API paginator."""

    def __init__(self, page: int, records_jsonpath: str) -> None:
        """Initialize paginator.

        Args:
            page: The page number.
            records_jsonpath: The JSON path to the records.
        """
        super().__init__(page)
        self.records_jsonpath = records_jsonpath

    def has_more(self, response: Response) -> bool:
        """Check if response has any items.

        Args:
            response: API response object.

        Returns:
            True if response contains at least one item.
        """
        try:
            first(
                extract_jsonpath(
                    self.records_jsonpath,
                    response.json(),
                )
            )
        except StopIteration:
            return False

        return True


@lru_cache(maxsize=None)
def load_openapi() -> dict[str, Any]:
    """Load the OpenAPI specification from the package.

    Returns:
        The OpenAPI specification as a dict.
    """
    with importlib_resources.files("tap_checkly").joinpath("openapi.json").open() as f:
        return json.load(f)


class ChecklyStream(RESTStream, metaclass=ABCMeta):
    """Checkly stream class."""

    url_base = "https://api.checklyhq.com/v1"
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
            "X-Checkly-Account": self.config["account_id"],
        }

    def get_url_params(
        self,
        context: dict | None,
        _: Any | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {}

        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date:
                params["from"] = start_date.timestamp()

        return params

    def _resolve_openapi_ref(self) -> dict[str, Any]:
        schema = {"$ref": f"#/components/schemas/{self.openapi_ref}"}
        openapi = load_openapi()
        schema["components"] = openapi["components"]
        return resolve_schema_references(schema)

    @property
    @lru_cache(maxsize=None)  # noqa: B019
    def schema(self) -> dict[str, Any]:  # type: ignore[override]
        """Return the schema for this stream.

        Returns:
            The schema for this stream.
        """
        return self._resolve_openapi_ref()

    @property
    @abstractmethod
    def openapi_ref(self) -> str:
        """Return the OpenAPI component name for this stream.

        Returns:
            The OpenAPI reference for this stream.
        """
        ...


class ChecklyPaginatedStream(ChecklyStream):
    """Checkly paginated stream class."""

    def get_new_paginator(self) -> ChecklyPaginator:
        """Get a new paginator instance.

        Returns:
            A paginator instance.
        """
        return ChecklyPaginator(1, self.records_jsonpath)

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: int | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        params["page"] = next_page_token
        params["limit"] = PAGE_SIZE
        return params
