from pathlib import Path

from roheboam.engine.vision.tasks.image_bounding_box_detection.loaders import roheboam_sample_data_paths_from_path


def test_roheboam_sample_data_paths_from_path():
    root_data_path = Path(__file__).parent / "data"
    train_image_paths, train_label_paths = roheboam_sample_data_paths_from_path(root_data_path, category="train")
    assert len(train_image_paths) == 1
    assert str(train_image_paths[0]) == str(root_data_path / "000000000009" / "image" / "000000000009.jpg")
    assert len(train_label_paths) == 1
    assert str(train_label_paths[0]) == str(root_data_path / "000000000009" / "label" / "000000000009.txt")

    test_image_paths, test_label_paths = roheboam_sample_data_paths_from_path(root_data_path, category="test")
    assert len(test_image_paths) == 1
    assert str(test_image_paths[0]) == str(root_data_path / "000000000025" / "image" / "000000000025.jpg")
    assert len(test_label_paths) == 1
    assert str(test_label_paths[0]) == str(root_data_path / "000000000025" / "label" / "000000000025.txt")
