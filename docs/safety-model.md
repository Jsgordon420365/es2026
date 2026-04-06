# Safety Model

## Default posture

Read-first.
No file mutation in v1.
No automatic opening or execution in v1.

## Error handling

Fail clearly.
Do not fabricate paths.
Do not fabricate result counts.
Do not suppress important errors.

## Network posture

If an HTTP server is added, default to loopback-only operation.