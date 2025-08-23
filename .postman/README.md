# Postman | API Tests

This document describes how Postman is used in this project to perform black-box API testing, how to run the tests locally, and how tests are integrated into CI/CD pipelines.

Postman is a GUI-based tool for sending, documenting, and especially testing API requests. In this project, Postman is used to perform black-box API tests to ensure the quality and reliability of the backend API.

## Black-box Testing

Black-box testing means that Postman tests never have direct access to the source code. Instead, requests are sent to the API, and the responses are evaluated. The goal is to cover as many edge cases as possible, especially those involving invalid input, to ensure a robust and high-quality API.

- Tests validate both successful and erroneous responses.
- No assumptions are made about the internal implementation—only the API contract is tested.
- This approach helps to catch regressions and unexpected behavior from a user's perspective.

![blackbox_testing](./blackbox_testing.svg)

## Running Tests Locally

You can run the Postman collection locally using either the Postman GUI, the [Postman CLI](https://learning.postman.com/docs/postman-cli/postman-cli-overview/), or [Newman](https://www.npmjs.com/package/newman):

- **Postman GUI:** Import the collection and environment, then run the collection using the built-in runner.
- **Postman CLI:** Authenticate with your Postman account, then run the collection directly from the cloud or from an exported file.
- **Newman:** Export the collection and environment as JSON, then run:
  ```
  newman run collection.json -e environment.json --reporters cli,junit --reporter-junit-export results.xml
  ```

## CI/CD Integration

Postman is used as a cloud-based tool in this project:

- The main collection is stored in the Postman Cloud.
- The [Postman CLI](https://learning.postman.com/docs/postman-cli/postman-cli-overview/) is used in CI to authenticate, fetch, and execute the collection locally.
- Test results are stored as artifacts in the CI pipeline and can also be uploaded to the Postman Cloud for further analysis.
- The CI integration is implemented via GitHub Actions in [../.github/workflows/test.yaml](../.github/workflows/test.yaml).

### How it works in CI

1. The pipeline logs into Postman using secure credentials.
2. The collection is executed against the deployed API (usually a staging or test environment).
3. Test results are exported in machine-readable formats (JUnit, JSON) and stored as build artifacts.
4. Optionally, results are uploaded to the Postman Cloud for historical tracking and reporting.
5. The build fails if any test fails, ensuring only passing APIs are deployed.