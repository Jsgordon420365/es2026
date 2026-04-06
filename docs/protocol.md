# Protocol and JSON Contract

The Search Everything Class-0 service communicates using structured JSON.

## Search Result

A single result entry:

```json
{
  "path": "C:\\Users\\jsgor\\Projects\\es2026\\README.md",
  "name": "README.md",
  "extension": "md",
  "size": 1674,
  "modified_at": "2024-03-06T10:14:44Z",
  "is_directory": false
}
```

## Search Response

```json
{
  "results": [ ... ],
  "count": 1,
  "total": 1,
  "query": "README.md",
  "took_ms": 12
}
```

## Search Request (Parameters)

- `query`: String. The raw Everything query.
- `limit`: Integer. Max results to return.
- `offset`: Integer.
- `folders_only`: Boolean.
- `files_only`: Boolean.
- `regex`: Boolean.

## Health Check Response

```json
{
  "status": "ok",
  "everything_running": true,
  "es_found": true,
  "es_path": "C:\\Program Files\\Everything\\es.exe",
  "version": "0.1.0"
}
```

## Error Response

```json
{
  "error": "EVERYTHING_NOT_RUNNING",
  "message": "The Everything service is not running. Please start it.",
  "code": 503
}
```
