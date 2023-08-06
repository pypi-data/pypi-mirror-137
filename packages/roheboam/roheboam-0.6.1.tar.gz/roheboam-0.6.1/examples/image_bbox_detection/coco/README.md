This is an example for a classification pipeline using the Pytorch Toolbox

We are going to recreate the find the number of cells that are in a microscopy slide

This data can be downloaded by:
1. `kaggle competitions download -c data-science-bowl-2018`
2. Then unzip downloaded files into `data/raw`, this is needed because we need to generate contour masks and bounding boxes

Install the environment via:
`conda env create -f src/bounding_box_detection_demo.yml`

We can do the training via:
`python src/train.py`

We can do set Flask endpoint (after training) via:
`python src/app.py --model_config_path src/experiments/config.yml`
