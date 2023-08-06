from pathlib import Path

from roheboam.engine.vision.utils.image.io import imread_grayscale, imwrite


def test_read_and_write_grayscale(tmpdir):
    grayscale_image = imread_grayscale(Path(__file__).parent / "test_data" / "berlin1_mask.png")

    imwrite(str(Path(tmpdir / "test.png")), grayscale_image)

    loaded_grayscale_image = imread_grayscale(str(Path(tmpdir / "test.png")))

    assert (grayscale_image == loaded_grayscale_image).all()
