To test:
`PYTHONPATH=/home/kevin/Documents/Projects/roheboam/roheboam:/home/kevin/Documents/Projects/roheboam/roheboam/engine pytest {path/to/file} --disable-pytest-warnings`

To test with runner:
```
PYTHONPATH=/home/kevin/Documents/Projects/roheboam/roheboam:/home/kevin/Documents/Projects/roheboam/roheboam/server ptw {path/to/file} --runner 'pytest -s --disable-pytest-warnings'
```

PYTHONPATH=/home/kevin/Documents/Projects/roheboam/roheboam:/home/kevin/Documents/Projects/roheboam/roheboam/engine ptw --runner "pytest _tests/vision/tasks/image_bounding_box_detection/data/loaders/roheboam/test_load_roheboam_sample.py --disable-pytest-warnings"
