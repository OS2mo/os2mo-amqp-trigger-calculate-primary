<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->

# OS2mo AMQP Trigger Calculate Primary

OS2mo AMQP Trigger for recalculating primary.

## Usage

Adjust the `FASTRAMQPI__MO_URL` variable and the other settings to point at your
running OS2mo instance, either;
* directly in `docker-compose.yaml` or
* by creating a `docker-compose.override.yaml` file.

Now start the container using `docker compose`:
```sh
docker compose up -d
```

The integration uses OS2mo's GraphQL event system. On startup it declares a
listener on the `engagement` routing key in the `mo` namespace, and OS2mo events
are then delivered as HTTP POSTs to its own `/events/mo/engagement` endpoint:
```
{
    "subject": "23d2dfc7-6ceb-47cf-97ed-db6beadcb09b",
    "priority": 10000
}
```

Each event causes the employee(s) related to the engagement to have their
primary engagement recalculated.

## Development

### Prerequisites

- [Poetry](https://github.com/python-poetry/poetry)

### Getting Started

1. Clone the repository:
```sh
git clone https://github.com/OS2mo/os2mo-amqp-trigger-calculate-primary.git
```

2. Install all dependencies:
```sh
poetry install
```

3. Set up pre-commit:
```sh
poetry run pre-commit install
```

### Running the tests

You need to have a running [os2mo](https://github.com/OS2mo/os2mo) stack to run tests.

Then run:
```sh
docker compose up -d
docker compose run --rm calculate-primary pytest .
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing data models
- MINOR: Backwards compatible updates to existing data models OR new models added
- PATCH: Backwards compatible bug fixes

## Authors

Magenta ApS <https://magenta.dk>

## License

This project uses: [MPL-2.0](MPL-2.0.txt)

This project uses [REUSE](https://reuse.software) for licensing.
All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
