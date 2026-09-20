from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Any, TypedDict
from urllib.parse import urlencode

import httpx
from authlib.oidc.core import CodeIDToken
from joserfc import jwt
from joserfc.jwk import KeySet
from joserfc.jwt import JWTClaimsRegistry

from app.auth.oidc_transaction import (
    OIDCLoginTransaction,
    OIDCLoginTransactionStore,
)
from app.core.config.settings import settings


class OIDCConfigurationError(RuntimeError):
    """Raised when AIIP OIDC configuration is incomplete."""


class OIDCAuthenticationError(RuntimeError):
    """Raised when an OIDC authentication response cannot be trusted."""


class JWKSResponse(TypedDict):
    """JSON Web Key Set response from the OIDC provider."""

    keys: list[dict[str, Any]]


class Auth0OIDCService:
    """Auth0 OpenID Connect integration for internal AIIP operators."""

    _HTTP_TIMEOUT = 10.0

    def _validate_configuration(self) -> None:
        required = {
            "AUTH0_DOMAIN": settings.auth0_domain,
            "AUTH0_CLIENT_ID": settings.auth0_client_id,
            "AUTH0_CLIENT_SECRET": settings.auth0_client_secret,
            "AUTH0_REDIRECT_URI": settings.auth0_redirect_uri,
        }

        missing = [name for name, value in required.items() if not value]

        if missing:
            raise OIDCConfigurationError(f"OIDC configuration is incomplete: {', '.join(missing)}")

    @property
    def issuer(self) -> str:
        domain = settings.auth0_domain.strip().rstrip("/")

        if domain.startswith("https://"):
            return domain

        if domain.startswith("http://"):
            raise OIDCConfigurationError("AUTH0_DOMAIN must use HTTPS.")

        return f"https://{domain}"

    @property
    def discovery_url(self) -> str:
        return f"{self.issuer}/.well-known/openid-configuration"

    async def discover(self) -> dict[str, Any]:
        self._validate_configuration()

        async with httpx.AsyncClient(timeout=self._HTTP_TIMEOUT) as client:
            response = await client.get(self.discovery_url)
            response.raise_for_status()

        metadata = response.json()

        if not isinstance(metadata, dict):
            raise OIDCAuthenticationError("Invalid OpenID Connect discovery response.")

        issuer = metadata.get("issuer")

        if not isinstance(issuer, str) or not issuer:
            raise OIDCAuthenticationError("Issuer is missing from OIDC discovery.")

        return metadata

    @staticmethod
    def _generate_code_verifier() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def _generate_code_challenge(code_verifier: str) -> str:
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    async def build_authorization_url(
        self,
        *,
        transaction_store: OIDCLoginTransactionStore,
    ) -> str:
        self._validate_configuration()

        metadata = await self.discover()

        authorization_endpoint = metadata.get("authorization_endpoint")

        if not isinstance(authorization_endpoint, str):
            raise OIDCAuthenticationError("Authorization endpoint is missing from OIDC discovery.")

        nonce = secrets.token_urlsafe(32)
        code_verifier = self._generate_code_verifier()

        transaction = await transaction_store.create(
            nonce=nonce,
            code_verifier=code_verifier,
        )

        params = {
            "response_type": "code",
            "client_id": settings.auth0_client_id,
            "redirect_uri": settings.auth0_redirect_uri,
            "scope": settings.auth0_scope,
            "state": transaction.state,
            "nonce": transaction.nonce,
            "code_challenge": self._generate_code_challenge(code_verifier),
            "code_challenge_method": "S256",
        }

        return f"{authorization_endpoint}?{urlencode(params)}"

    async def exchange_code(
        self,
        *,
        code: str,
        transaction: OIDCLoginTransaction,
    ) -> dict[str, Any]:
        self._validate_configuration()

        metadata = await self.discover()
        token_endpoint = metadata.get("token_endpoint")

        if not isinstance(token_endpoint, str):
            raise OIDCAuthenticationError("Token endpoint is missing from OIDC discovery.")

        payload = {
            "grant_type": "authorization_code",
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "code": code,
            "redirect_uri": settings.auth0_redirect_uri,
            "code_verifier": transaction.code_verifier,
        }

        async with httpx.AsyncClient(timeout=self._HTTP_TIMEOUT) as client:
            response = await client.post(
                token_endpoint,
                data=payload,
                headers={"Accept": "application/json"},
            )

        if response.status_code >= 400:
            raise OIDCAuthenticationError("Authorization code exchange failed.")

        token_response = response.json()

        if not isinstance(token_response, dict):
            raise OIDCAuthenticationError("Invalid token response.")

        if not isinstance(token_response.get("id_token"), str):
            raise OIDCAuthenticationError("ID token is missing from the token response.")

        return token_response

    async def validate_id_token(
        self,
        *,
        id_token: str,
        transaction: OIDCLoginTransaction,
    ) -> dict[str, Any]:
        self._validate_configuration()

        metadata = await self.discover()

        discovered_issuer = metadata.get("issuer")

        if not isinstance(discovered_issuer, str) or not discovered_issuer:
            raise OIDCAuthenticationError("Issuer is missing from OIDC discovery.")

        jwks_uri = metadata.get("jwks_uri")

        if not isinstance(jwks_uri, str):
            raise OIDCAuthenticationError("JWKS URI is missing from OIDC discovery.")

        async with httpx.AsyncClient(timeout=self._HTTP_TIMEOUT) as client:
            response = await client.get(jwks_uri)
            response.raise_for_status()

        raw_jwks = response.json()

        if not isinstance(raw_jwks, dict) or not isinstance(raw_jwks.get("keys"), list):
            raise OIDCAuthenticationError("Invalid JWKS response.")

        raw_keys = raw_jwks.get("keys")

        if not isinstance(raw_keys, list):
            raise OIDCAuthenticationError("Invalid JWKS response.")

        if not all(isinstance(key, dict) for key in raw_keys):
            raise OIDCAuthenticationError("Invalid JWKS response.")

        jwks: JWKSResponse = {
            "keys": raw_keys,
        }

        try:
            key_set = KeySet.import_key_set(jwks)

            token = jwt.decode(
                id_token,
                key_set,
                algorithms=["RS256"],
            )

            claims = CodeIDToken(
                token.claims,
                token.header,
                params={"nonce": transaction.nonce},
            )

            claims.validate(leeway=60)

            registry = JWTClaimsRegistry(
                iss={"essential": True, "value": discovered_issuer},
                aud={
                    "essential": True,
                    "values": [settings.auth0_client_id],
                },
                sub={"essential": True},
            )
            registry.validate(claims)

        except Exception as exc:
            import logging

            logging.getLogger(__name__).exception(
                "OIDC ID token validation failed: %s: %s",
                type(exc).__name__,
                str(exc),
            )
            raise OIDCAuthenticationError("ID token validation failed.") from exc

        return dict(claims)
