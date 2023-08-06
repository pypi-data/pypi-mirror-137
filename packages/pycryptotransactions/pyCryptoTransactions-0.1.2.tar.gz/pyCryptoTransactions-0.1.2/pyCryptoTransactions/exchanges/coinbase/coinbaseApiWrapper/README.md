# Unofficial Coinbase Python3 Client Library

A minimalistic wrapper to interact with the Coinbase API. 
This version is based on the repository [coinbase_python3](https://github.com/resy/coinbase_python3) from Michael Montero and was extended to work with v2 of the Coinbase API.
Some functions were taken out for a minmalistic wrapper.

This library supports both the [API key authentication method](https://coinbase.com/docs/api/overview) and OAuth. The below examples use an API key - for instructions on how to use OAuth, see [OAuth Authentication](#oauth-authentication).

## Usage

Start by [enabling an API Key on your account](https://coinbase.com/settings/api).

Next, create an instance of the client using the `Coinbase.with_api_key()` method:

```python
import coinbase

coinbase = coinbase.Coinbase.with_api_key(coinbase_api_key, coinbase_api_secret)
```

Keeping your credentials safe is essential to maintaining good security.  Read more about the recommended [security practices](https://coinbase.com/docs/api/overview#security) provided by Coinbase.

Now you can call methods on `coinbase` similar to the ones described in the [API reference](https://coinbase.com/api/doc).  For example:

```python
accounts = coinbase.get('/accounts')
```
## OAuth Authentication

To authenticate with OAuth, first create an OAuth application at https://coinbase.com/oauth/applications.  When a user wishes to connect their Coinbase account, redirect them to a URL created with `CoinbaseOAuth.create_authorize_url()`:

```python
import coinbase
coinbase_oauth = coinbase.CoinbaseOAuth(client_id, client_secret, redirect_url)
```

Define the scopes you need (check the Coinbase API documentation) and generate a Authorize URL:

```python
scopes = ["wallet:accounts:read","wallet:addresses:read",
            "wallet:transactions:read","wallet:buys:read",
            "wallet:sells:read", "wallet:deposits:read",
            "wallet:withdrawals:read"]
coinbase_oauth.create_authorize_url(scopes)
```

After the user has authorized your application, they will be redirected back to the redirect URL specified above. A `code` parameter will be included - pass this into `get_tokens()` to receive a set of tokens:

```python
tokens = coinbase_oauth.get_tokens(code)
```

Store these tokens safely, and use them to make Coinbase API requests in the future. For example:

```python
coinbase = coinbase.Coinbase.with_oauth(access_token, refresh_token)
accounts = coinbase.get('/accounts')
```

## Security notes

If someone gains access to your API Key they will have complete control of your Coinbase account.  This includes the abillity to send all of your bitcoins elsewhere.

For this reason, API access is disabled on all Coinbase accounts by default.  If you decide to enable API key access you should take precautions to store your API key securely in your application.  How to do this is application specific, but it's something you should [research](http://programmers.stackexchange.com/questions/65601/is-it-smart-to-store-application-keys-ids-etc-directly-inside-an-application) if you have never done this before.
