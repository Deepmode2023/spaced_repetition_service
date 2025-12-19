import app.modules.md.domain.mapper as mapper
from unittest.mock import Mock


def test_mapper_called(postfix_prefix_data, monkeypatch):
    (post, pref) = postfix_prefix_data
    mock = Mock()
    monkeypatch.setattr(mapper, "mapper_tag_name", mock)
    mapper.mapper_tag_name(post, pref)
    mock.assert_called_once_with(post, pref)


def test_mapper_actual_returned_value(postfix_prefix_data):
    (post, pref) = postfix_prefix_data
    tag = mapper.mapper_tag_name(post, pref)
    assert tag.name == "italic"
    assert tag.postfix == post
    assert tag.prefix == pref


def test_mapper_for_unexisting_tag():
    (post, pref) = ("kdkfkgd", "dfjjfj")
    tag = mapper.mapper_tag_name(post, pref)
    assert tag.name == "text"
    assert tag.postfix == ""
    assert tag.prefix == ""


def test_mapper_with_wrong_type_args():
    (post, pref) = (19, 20)
    tag = mapper.mapper_tag_name(post, pref)
    assert tag.name == "text"
    assert tag.postfix == ""
    assert tag.prefix == ""
