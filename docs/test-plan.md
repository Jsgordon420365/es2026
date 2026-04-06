# Test Plan

## Minimum smoke tests

- Confirm project imports
- Confirm health check behavior
- Confirm missing `es.exe` produces a clear error
- Confirm a basic search returns structured data
- Confirm empty results are handled cleanly

## Unit test targets

- Query builder
- Result parser
- Service orchestration
- Health logic