import pytest
from utils.headingHelpers import extractHeading


def createMockContent(text):
    return {
        "x": 3,
        "y": 4,
        "text": text
    }


def setupMultipleHeadings(headings):
    headings = [createMockContent(heading) for heading in headings]

    headings = [extractHeading(content["text"]) for content in headings]
    return headings


def assertGroup(headings, expectedHeadings):
    i = 0
    while i < len(headings):
        assert headings[i]["region"] == expectedHeadings[i]["region"]
        assert headings[i]["location"] == expectedHeadings[i]["location"]
        i += 1


def test_multiple_locaitons():
    headings = [
        'THE PAST. INT. CONCORD. MARCH HOUSE. JO & MEG’S ROOM. 1861.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "THE PAST. INT.",
            "location": "CONCORD. MARCH HOUSE. JO & MEG’S ROOM",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_one_location():
    headings = [
        'INT. GERMAN BEER HALL. NIGHT. 1868.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INT.",
            "location": "GERMAN BEER HALL",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_both_int_ext():
    headings = [
        'INT/EXT. GERMAN BEER HALL. NIGHT. 1868.',
        'INT./EXT GERMAN BEER HALL. NIGHT. 1868.',
        'INT./EXT. GERMAN BEER HALL. NIGHT. 1868.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INT/EXT.",
            "location": "GERMAN BEER HALL",
        },
        {
            "region": "INT./EXT",
            "location": "GERMAN BEER HALL",
        },
        {
            "region": "INT./EXT.",
            "location": "GERMAN BEER HALL",
        },
    ]

    assertGroup(headings, expectedHeadings)
