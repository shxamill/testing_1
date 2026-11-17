# Bootstrap Login UI Practice

[![CI](https://github.com/shxamill/testing_1/actions/workflows/ci.yml/badge.svg)](https://github.com/shxamill/testing_1/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small front-end exercise for practising HTML, CSS, and Bootstrap components.

## What is included

- A static Bootstrap 5 page with heading and button examples.
- A login-form layout.
- A second HTML exercise under the web directory.

## Validate local assets

Run `python scripts/check_assets.py` to check local HTML/CSS references. The same check runs automatically in GitHub Actions on pushes and pull requests.

## Run locally

No build step or package installation is required. Open index.html in a browser, or run a local server from the repository root:

~~~bash
python -m http.server 8000
~~~

Then visit http://localhost:8000.

Bootstrap is loaded from jsDelivr, so an internet connection is needed for its CDN stylesheet and JavaScript.

## Important limitation

The login form is a visual front-end demonstration only. It has no authentication service, database, registration flow, or working account session. Do not enter real credentials.

## Contributing

See CONTRIBUTING.md. Keep examples focused and explain what each exercise demonstrates.

## License

This project is licensed under the [MIT License](LICENSE).

## Community and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md).
