1. Populate .env
2. Install requirements
3. Run with `date_start`, `date_end`, `email`, for example:
```
$ python visual_time/sele.py 2025-01-23 2025-01-23 my.email@myorg.com
```

It will prompt the pwd, ask for Okta auth, and fill each day that is not weekend starting at 9:00 and ending around 18:00-18:15
