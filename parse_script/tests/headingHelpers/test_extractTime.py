import pytest
from utils.headingHelpers import extractTime


def createMockContent(text):
    return {
        "x": 3,
        "y": 4,
        "text": text
    }


def setupMultipleHeadings(headings):
    headings = [createMockContent(heading) for heading in headings]
    headings = [extractTime(content["text"]) for content in headings]
    return headings


def assertGroup(headings, expectedHeadings):
    i = 0
    while i < len(headings):
        assert headings[i] == expectedHeadings[i]
        i += 1


def test_no_time():
    headings = [
        'EXT. SPACE - 3-D PRINTED CRAFT'
    ]
    headings = setupMultipleHeadings(headings)
    for heading in headings:
        assert heading == None


def test_multiple_times():
    headings = [
        'INT. GERMAN BEER HALL. NIGHT. 1868.',
        'EXT. PHILADELPHIA STREET - NIGHT (FLASHBACK)',
        'INT. CAMP LEHIGH, SHIELD FACILITY, PEGGY’S OFC. - DAY (1970)',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        ['NIGHT', '1868'],
        ['NIGHT', '(FLASHBACK)'],
        ['DAY', '(1970)'],
    ]

    assertGroup(headings, expectedHeadings)


def test_one_time():
    headings = ['EXT. WATERFORD HOUSE - CONTINUOUS',
                'INT. WATERFORD HOUSE - BEDROOM - DAY',
                'EXT. COURTHOUSE PARKING LOT - SUNSET',
                'THE PAST. INT. CONCORD. MARCH HOUSE. JO & MEG’S ROOM. 1861.',
                ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        ['CONTINUOUS'],
        ['DAY'],
        ['SUNSET'],
        ['1861'],
    ]

    assertGroup(headings, expectedHeadings)
