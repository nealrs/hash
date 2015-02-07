## hash.py

**What**

Input a URL & get back a list of relevant hashtags

**Why**

1. Better hashtags mean better engagement
2. Experimenting with the RiteTag & Textalytics APIs for potential inclusion in [25 Headlines](http://nealrs.github.io/25Headlines/).

**How**

1. Sign up for [Textalytics](https://textalytics.com/personal_area) & [RiteTag](http://ritetag.com/developer/signup). 
2. Add your API keys to `keys_ex.py` & rename it `keys.py`.
3. Install the dependencies:
  `pip install requests requests_oauthlib click`
4. Go nuts

Usage: `hash.py [OPTIONS]`

Options:

```
--url TEXT     The URL you want to analyze  [required]
--rel INTEGER  Keyword relevancy threshold [default 70%]
--ent INTEGER  (1) Extract named entities [default], (0) ignore
--con INTEGER  (1) Extract concepts [default], (0) ignore
--help         Show this message and exit.
```

FYI, you _will_ get rate limited by RiteTag pretty quickly.


**Contribute**

If you think this is a cool idea, but kind of inefficient, please submit a PR and let's make this better.

&copy; 2015, Neal Shyam &middot; not sure on licensing yet, so suggest something?
