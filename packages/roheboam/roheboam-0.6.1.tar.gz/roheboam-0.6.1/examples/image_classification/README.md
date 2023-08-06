### Hotdog not hotdog example

#### To train:
`PYTHONPATH=. python roheboam_hotdog_not_hotdog.py train --config_file_folder ./configs`

#### To serve:
`PYTHONPATH=. python roheboam_hotdog_not_hotdog.py serve --model_path <path_to_model>`

#### To create a application for training of Hotdog Not Hotdog
`pyinstaller --noconfirm --add-data 'examples/image_classification/hotdog_not_hotdog/configs:configs/' --add-data './Dockerfile:.' examples/image_classification/hotdog_not_hotdog/roheboam_hotdog_not_hotdog.py`

#### To build, run and train
1. `cd` to pyinstaller directory
2. `docker build . --tag roheboam-hotdog-not-hotdog && mkdir experiments`
3.
```
docker run --runtime=nvidia \
--mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/examples/image_classification/hotdog_not_hotdog/data,dst=/app/data' --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam_hotdog_not_hotdog/experiments,dst=/app/experiments' --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam_hotdog_not_hotdog/configs,dst=/app/configs' --shm-size 8G roheboam-hotdog-not-hotdog train --config_file_folder configs
```

```
docker run \
--mount 'type=bind,src=/Users/kevinlu/Downloads/roheboam_hotdog_not_hotdog/data,dst=/app/data' --mount 'type=bind,src=/Users/kevinlu/Downloads/roheboam_hotdog_not_hotdog/experiments,dst=/app/experiments' --mount 'type=bind,src=/Users/kevinlu/Downloads/roheboam_hotdog_not_hotdog/configs,dst=/app/configs' --shm-size 8G roheboam-hotdog-not-hotdog train --config_file_folder configs
```

#### E2E
```pyinstaller --noconfirm --add-data 'examples/image_classification/hotdog_not_hotdog/configs:configs/' --add-data './Dockerfile:.' examples/image_classification/hotdog_not_hotdog/roheboam.py && cd dist/roheboam && docker build . --tag roheboam-hotdog-not-hotdog && mkdir experiments && docker run --runtime=nvidia \
--mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/examples/image_classification/hotdog_not_hotdog/data,dst=/app/data' --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam/experiments,dst=/app/experiments' --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam/configs,dst=/app/configs' --shm-size 8G roheboam-hotdog-not-hotdog train --config_file_folder configs
```

#### Debug Docker:
```
docker run --runtime=nvidia --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam_hotdog_not_hotdog/experiments,dst=/app/experiments' -it --entrypoint /bin/bash roheboam-hotdog-not-hotdog
```

#### To serve MLflow on Mac:
```
docker run --mount 'type=bind,src=/Users/kevinlu/Downloads/roheboam_hotdog_not_hotdog/experiments,dst=/app/experiments' -p 5000:5000 roheboam-hotdog-not-hotdog serve --model_path <model_path>
```

#### To serve MLflow on Linux:
```
docker run --runtime=nvidia --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam/dist/roheboam_hotdog_not_hotdog/experiments,dst=/app/experiments' -p 5000:5000 roheboam-hotdog-not-hotdog serve --model_path <model_path>
```


We are going to recreate the Seefood AI classifier from the show Silicon Valley

This data can be downloaded by:
1. `cd` to this directory
2. `git clone https://github.com/kevinlu1211/seefood-dataset data`

Install the environment via:
`conda env create -f src/classification_demo.yml`

We can do the training via:
`python src/train.py`

We can do set Flask endpoint (after training) via:
`python src/app.py --model_config_path src/experiments/config.yml`
