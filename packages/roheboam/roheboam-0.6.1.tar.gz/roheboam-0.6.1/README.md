## Usage

### Workflow

1. Create a notebook for training
2. Use `roheboam train --config_path {config_path} --root_save_directory {root_save_directory} --gpus {gpus}`
3. Use `roheboam containerise_model --model_path {model_path} --model_image_tag {model_image_tag}`
4. Push to registry
5. Run tests
6. Push to CI

## Development

### Setup development environment

```
conda create -n roheboam python=3.8 && conda activate roheboam
conda install -c conda-forge jupyterlab jupyterlab_vim ipywidgets jupyterlab_code_formatter black isort -y
pip install -e .
pip install pre-commit pytest pytest-only pytest-mock python-semantic-release nbdev nb-black pytest-custom-exit-code
pre-commit install
pre-commit install --hook-type commit-msg # this is for commitizen to work
pre-commit install --hook-type pre-push # this is for a pytest on push to work
```
