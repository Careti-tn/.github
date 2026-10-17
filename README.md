# Careti organization profile

GitHub displays `profile/README.md` on the Careti organization overview when this `.github` repository is public.

Careti is a digital loyalty platform for Tunisian businesses. The profile covers digital stamp cards, rewards, customer updates, and support for Apple Wallet and Google Wallet. Its tagline is "Every visit counts."

The profile follows the structure of the [APP-LOFA organization profile](https://github.com/APP-LOFA). The banner is an editable SVG in `profile/assets/banner.svg`.

Run the local checks with Python 3:

```sh
python scripts/check_profile.py
```

The checks validate the banner, profile links, repository paths, and publishable files for accidental credentials. No access token belongs in this repository.
