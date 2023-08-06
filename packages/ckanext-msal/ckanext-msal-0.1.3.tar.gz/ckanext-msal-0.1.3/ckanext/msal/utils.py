import secrets
from typing import Dict, Optional, Any, List
from datetime import datetime as dt
from datetime import timedelta as td

import msal

import ckan.lib.helpers as h
import ckan.plugins.toolkit as tk
from ckan.common import session

import ckanext.msal.config as msal_conf


def build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        msal_conf.CLIENT_ID,
        authority=authority or msal_conf.AUTHORITY,
        client_credential=msal_conf.CLIENT_SECRET,
        token_cache=cache,
    )


def build_auth_code_flow(authority=None, scopes=None) -> Dict[str, Any]:
    return build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [], redirect_uri=h.url_for("msal.authorized", _external=True)
    )


def _load_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if session.get("msal_token_cache"):
        cache.deserialize(session["msal_token_cache"])
    return cache


def _save_cache(cache) -> None:
    if cache.has_state_changed:
        session["msal_token_cache"] = cache.serialize()


def _get_token_from_cache(scope=None) -> Optional[Dict[Any, Any]]:
    cache = _load_cache()
    app = build_msal_app(cache=cache)
    accounts: List[Dict[Any, Any]] = app.get_accounts()

    if accounts:
        _save_cache(cache)
        return app.acquire_token_silent(scope, account=accounts[0])


def _get_exp_date():
    """
    Returns a float number that represents an expiration date of user session
    The session lifetime is configurable with `ckanext.msal.session_lifetime` option

    return
    type: float
    """
    return (dt.now() + td(seconds=msal_conf.USER_SESSION_LIFETIME)).timestamp()


def _make_password() -> str:
    """
    Return a random URL-safe text string, in Base64 encoding

    return
    type: str
    """
    return secrets.token_urlsafe(60)


def get_restricted_domains() -> List[str]:
    """Returns a lits of restricted domains from config
    User won't be able to login with this email domain

    Returns:
        List[str]: a list of domain strings
    """

    return tk.aslist(msal_conf.RESTRICTED_DOMAINS, ",")


def get_allowed_domains() -> List[str]:
    """Returns a lits of allowed domains from config
    User will be able to login only with those email domains

    Returns:
        List[str]: a list of domain strings
    """

    return tk.aslist(msal_conf.ALLOWED_DOMAINS, ",")


def is_email_restricted(email: str) -> bool:
    """Checks if the user email is restricted by domain
    Returns True if resticted

    Args:
        email (str): user email

    Returns:
        bool
    """

    for domain in get_restricted_domains():
        if email.endswith(domain):
            return True
    return False


def is_email_allowed(email: str) -> bool:
    """Checks if the user email is allowed by domain
    Returns True if allowed

    Args:
        email (str): user email

    Returns:
        bool
    """
    
    allowed_domains: list[str] = get_allowed_domains()
    
    if not allowed_domains:
        return True

    for domain in get_allowed_domains():
        if email.endswith(domain):
            return True
    return False
