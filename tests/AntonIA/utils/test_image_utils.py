import pytest
from PIL import Image
from AntonIA.utils import image_utils
import tempfile
import os

def create_test_image(color=(255, 0, 0, 255), size=(100, 100)):
    img = Image.new("RGBA", size, color)
    buf = tempfile.SpooledTemporaryFile()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

def create_temp_watermark(color=(0, 255, 0, 128), size=(20, 20)):
    img = Image.new("RGBA", size, color)
    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(temp, format="PNG")
    temp.close()
    return temp.name

def test_add_watermark_basic():
    base_img_bytes = create_test_image()
    watermark_path = create_temp_watermark()
    result_bytes = image_utils.add_watermark(base_img_bytes, watermark_path)
    result_img = Image.open(tempfile.SpooledTemporaryFile())
    result_img = Image.open(tempfile.SpooledTemporaryFile())
    result_img.fp.write(result_bytes)
    result_img.fp.seek(0)
    result_img = Image.open(result_img.fp)
    assert result_img.size == (100, 100)
    os.remove(watermark_path)

def test_add_watermark_opacity_and_scale():
    base_img_bytes = create_test_image()
    watermark_path = create_temp_watermark()
    # Test with different opacity and scale
    result_bytes = image_utils.add_watermark(base_img_bytes, watermark_path, opacity=0.5, scale=0.5)
    result_img = Image.open(tempfile.SpooledTemporaryFile())
    result_img.fp.write(result_bytes)
    result_img.fp.seek(0)
    result_img = Image.open(result_img.fp)
    assert result_img.size == (100, 100)
    os.remove(watermark_path)

def test_add_watermark_fn_factory_valid():
    base_img_bytes = create_test_image()
    watermark_path = create_temp_watermark()
    fn = image_utils.add_watermark_fn_factory(watermark_path, opacity=0.7, scale=0.3)
    assert callable(fn)
    result_bytes = fn(base_img_bytes)
    result_img = Image.open(tempfile.SpooledTemporaryFile())
    result_img.fp.write(result_bytes)
    result_img.fp.seek(0)
    result_img = Image.open(result_img.fp)
    assert result_img.size == (100, 100)
    os.remove(watermark_path)

def test_add_watermark_fn_factory_missing_file():
    fn = image_utils.add_watermark_fn_factory("nonexistent_file.png")
    assert fn is None

def test_add_watermark_fn_factory_invalid_image():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        temp.write(b"not an image")
        temp_path = temp.name
    fn = image_utils.add_watermark_fn_factory(temp_path)
    assert fn is None
    os.remove(temp_path)