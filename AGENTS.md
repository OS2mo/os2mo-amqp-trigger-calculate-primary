## Context
- This is an integration for the OS2mo application (https://github.com/OS2mo) that runs as a separate docker-compose service.
- This integration ensures that employees have a "primary" engagement, for compatibility with external systems that expect a 1:1 relationship between employees and engagements.
- This integration is event-driven, it listens to events from OS2mo and triggers its validation logic
- This integration is important, but also contains a lot of legacy code, as it has been running in production without any accidents for a long time. Therefore, changes should be surgical if possible. No big refactoring.

## Running Tests
- Unit tests are in `tests/`, except for any sub-directories, like `tests/integration/`, which is for integration tests
- Unit tests can be run without starting the whole stack
- Unit tests are old and not very good
- Integration tests are in `tests/integration/`
- Integration tests require the MO stack to be running, you can clone it from: https://github.com/OS2mo
- To run integration tests:
  - Ensure mo stack is running
  - Start project's stack: `docker compose up -d`
  - Run tests: `docker compose run --rm calculate-primary pytest <test-path>`

## Boundaries
- If there are uncommitted changes, do not add them to commits you make. Either commit your changes separately, or if it isn't possible, ask me for permission to commit the existing changes.
