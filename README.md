# VisionAR Cloud

Cloud repository for VisionAR models.

## Catalog format (`models.json`)

`models.json` is generated automatically by `scripts/generate_models_catalog.py`
(via `.github/workflows/generate-models-catalog.yml`) from the current
contents of `assets/models/` — **do not edit it manually**, changes will be
overwritten on the next push that touches a `.glb` file.

```json
{
  "version": 1,
  "catalogName": "VisionAR Cloud",
  "models": [
    {
      "id": "house",
      "name": "House",
      "model": "assets/models/house.glb",
      "sizeBytes": 53915000
    }
  ]
}
```

Fields per model entry:

- `id` — filename without extension, used as the model's stable id.
- `name` — display name derived from `id` (`garden_table` -> `Garden Table`).
- `model` — path to the `.glb` file, relative to the repository root.
- `sizeBytes` — optional. Exact file size in bytes, read directly from the
  `.glb` file on disk at generation time. Consumers that don't recognize
  this field should ignore it safely (it was added after the initial
  schema and is not required for a valid catalog entry).
