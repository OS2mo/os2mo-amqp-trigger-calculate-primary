<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->

# OS2mo AMQP Trigger Calculate Primary

OS2mo AMQP Trigger for recalculating primary.

## Usage

Adjust the `AMQP_HOST` variable to OS2mo's running message-broker, either;
* directly in `docker-compose.yml` or
* by creating a `docker-compose.override.yaml` file.

Add variables from MoraHelper and more.

Now start the container using `docker-compose`:
```sh
docker-compose up -d
```

You should see the following:
```
Configuring calculate-primary logging
Acquiring updater: SD
Got class: <class 'integrations.calculate_primary.sd.SDPrimaryEngagementUpdater'>
Got object: <integrations.calculate_primary.sd.SDPrimaryEngagementUpdater object at 0x7fe055067a30>
Establishing AMQP connection to amqp://guest:xxxxx@msg_broker:5672/
Creating AMQP channel
Attaching AMQP exchange to channel
Declaring unique message queue: os2mo-consumer-db169240-4054-4818-a333-15ca41ba9835
Binding routing-key: employee.employee.create
Binding routing-key: employee.employee.edit
Binding routing-key: employee.employee.terminate
Binding routing-key: employee.engagement.create
Binding routing-key: employee.engagement.edit
Binding routing-key: employee.engagement.terminate
Listening for messages
```

At which point an update to an employee or engagement in OS2mo should trigger an event similar to:
```
{
    "routing-key": "employee.employee.edit",
    "body": {
        "uuid": "23d2dfc7-6ceb-47cf-97ed-db6beadcb09b",
        "object_uuid": "23d2dfc7-6ceb-47cf-97ed-db6beadcb09b",
        "time": "2022-01-04T00:00:00+01:00"
    }
}
Recalculating user: 23d2dfc7-6ceb-47cf-97ed-db6beadcb09b
```

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
