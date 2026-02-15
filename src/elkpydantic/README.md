# elkpydantic package files

Short explanation of each item in this folder:

- `__init__.py`: Public package exports (`build_canvas`, models, enums, settings, and `layout_with_elkjs`).
- `base.py`: Shared primitives (`Properties`) and utility ID generator.
- `builder.py`: Core input parsing + graph enrichment logic; also package CLI entrypoint.
- `canvas.py`: Root ELK canvas model (`id`, `layoutOptions`, top-level `children`/`edges`).
- `edge.py`: Edge and edge-label Pydantic models.
- `elkjs.py`: Local Node/elkjs bridge for optional layout execution from Python.
- `enums.py`: ELK enum definitions used by typed options/models.
- `node.py`: Node and node-label models with validation rules (leaf vs subgraph sizing, unique IDs).
- `options.py`: Typed ELK layout option models and parsing/serialization helpers.
- `port.py`: Port and port-label models.
- `settings.py`: Settings/defaults models and built-in sample settings.
