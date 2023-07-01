import pytest
import json
import os
import sys
from scripts.program.metadata.image_metadata import ImageSet, ImageMetadata, ImageSetEncoder

@pytest.fixture
def sample_metadata() -> ImageMetadata:
    metadata = ImageMetadata()

    image_set1 = ImageSet(
        header={
            "num_images": 3,
            "description": "Set of images for task 1"
        },
        images=["image1.jpg", "image2.jpg", "image3.jpg"]
    )

    image_set2 = ImageSet(
        header={
            "num_images": 2,
            "description": "Set of images for task 2"
        },
        images=["image4.jpg", "image5.jpg"]
    )

    metadata.add_image_set(image_set1)
    metadata.add_image_set(image_set2)

    return metadata

def test_save_and_load_json(sample_metadata, tmp_path):
    # Save metadata to JSON
    filename = tmp_path / "image_metadata.json"
    sample_metadata.save_to_json(str(filename))

    # Load metadata from JSON
    loaded_metadata = ImageMetadata.load_from_json(str(filename))

    # Check number of image sets
    assert len(loaded_metadata.image_sets) == len(sample_metadata.image_sets)

    # Check header information of the first image set
    assert loaded_metadata.image_sets[0]["header"]["num_images"] == 3
    assert loaded_metadata.image_sets[0]["header"]["description"] == "Set of images for task 1"

    # Check images in the first image set
    assert loaded_metadata.image_sets[0]["images"] == ["image1.jpg", "image2.jpg", "image3.jpg"]

    # ... additional assertions for the second image set

def test_save_and_load_json_file_content(sample_metadata, tmp_path):
    # Save metadata to JSON
    filename = tmp_path / "image_metadata.json"
    sample_metadata.save_to_json(str(filename))

    # Load JSON file and compare its content
    with open(filename, "r") as file:
        loaded_data = json.load(file)

    assert len(loaded_data["image_sets"]) == len(sample_metadata.image_sets)

    for loaded_image_set, sample_image_set in zip(loaded_data["image_sets"], sample_metadata.image_sets):
        # Compare dictionaries by converting ImageSet instances to dictionaries
        assert loaded_image_set == ImageSetEncoder().default(sample_image_set)

