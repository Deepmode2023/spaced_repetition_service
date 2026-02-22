from app.domain.vo.specific_tags import SPECIFIC_TAGS, TAGS_RE


import pytest


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        ("[important]: Something", "important", "Something"),
        ("[[important]: Something sdfsd", "important", "Something sdfsd"),
        ("[[  important]]: Something", "important", "Something"),
        ("[[IMPORTANT]] Something", "important", "Something"),
        ("[[important]] Something", "important", "Something"),
    ],
)
def test_important_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        ("[hint]: Something", "hint", "Something"),
        ("[[hint]: Something sdfsd", "hint", "Something sdfsd"),
        ("[[  hint]]: Something", "hint", "Something"),
        ("[[hint]] Something", "hint", "Something"),
        ("[[hint]] Something", "hint", "Something"),
    ],
)
def test_hint_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        ("[asked_question]: Something", "question", "Something"),
        ("[[asked_question]: Something sdfsd", "question", "Something sdfsd"),
        ("[[  question]]: Something", "question", "Something"),
        ("[[question]] Something", "question", "Something"),
        ("[[question]] Something", "question", "Something"),
    ],
)
def test_question_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        ("### Something", "highlight", "Something"),
        ("## Something sdfsd", "highlight", "Something sdfsd"),
        ("# Something", "highlight", "Something"),
    ],
)
def test_question_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        (
            "[[b219f15a-de8c-4745-906e-d5e07a28d32c]]",
            "load_link",
            "b219f15a-de8c-4745-906e-d5e07a28d32c",
        ),
    ],
)
def test_question_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content


@pytest.mark.parametrize(
    "capture, tag_name, content",
    [
        ("[[dkkd]][[dkkdd]]", "tag", "dkkd"),
        ("[[dkkd]]", "tag", "dkkd"),
        ("[[dkkd sdfsd]]", "tag", "dkkd sdfsd"),
    ],
)
def test_question_tag(capture, tag_name, content):
    tag = SPECIFIC_TAGS.find_tag(capture)

    assert tag is not None
    assert tag.tag.name == tag_name
    assert tag.content == content
