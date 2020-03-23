import pytest
from screenplay_pdf_to_json.utils import isHeading, extractTime, extractHeading


def createMockContent(text):
    return {
        "x": 3,
        "y": 4,
        "text": text
    }


def test_word_region_first():
    text = createMockContent(
        'INT. GERMAN BEER HALL. NIGHT. 1868.')
    assert isHeading(text) == True


def test_word_before_region():
    text = createMockContent(
        'THE PAST. INT. CONCORD. MARCH HOUSE. JO & MEG’S ROOM. 1861.')
    assert isHeading(text) == True


def test_region_location_time():
    text = createMockContent(
        'EXT. WATERFORD HOUSE - CONTINUOUS')
    assert isHeading(text) == True


def test_ext_int_combo():
    text1 = createMockContent(
        'EXT/INT. WATERFORD HOUSE - CONTINUOUS')
    text2 = createMockContent(
        'INT/EXT. WATERFORD HOUSE - CONTINUOUS')
    assert isHeading(text1) == True
    assert isHeading(text2) == True


def test_region_location():
    text = createMockContent(
        'INT. ELEVATOR')
    assert isHeading(text) == True


def test_time_2_dashes():
    text = createMockContent(
        'INT. DON DRAPER’S OFFICE -- LATER')
    assert isHeading(text) == True


def test_word_before_region():
    text = createMockContent(
        'RIGHT IN THE STINT.')
    assert isHeading(text) == False
