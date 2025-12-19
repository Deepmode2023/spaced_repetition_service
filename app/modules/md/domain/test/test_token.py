import pytest
from ..token import Token, FlatToken


@pytest.fixture
def data_token(postfix_prefix_data) -> tuple[int, int, str, str, str]:
    return 0, 10, "content", *postfix_prefix_data


def test_for_correct_retured_token(data_token):
    (start, end, content, postf, pref) = data_token
    token = Token(start, end, content, postf, pref)
    assert token.content == content
    assert len(token.children) == 0
    assert token.position.start == start
    assert token.position.end == end
    assert token.tag.name == "italic"


def test_type_passed_behavior():
    with pytest.raises(ValueError):
        Token(-1, "skfdk", 202003, "kskfk", "dlldld")


def test_for_unknown_prefix():
    token = Token(0, 2, "dlldldld", "kskdkd", "dkkdkd")

    assert token.tag.name == "text"


def test_check_set_child_method(token):
    token.set_child(
        Token(12, 15, "ExampleContent", "*", "*"),
    )
    assert len(token.children) == 1


def test_check_set_child_method_for_incorect_data(token):
    with pytest.raises(ValueError):
        token.set_child(20)
        token.set_child("strs")


def test_check_set_children_method(token):
    print(token.children)
    token.set_children(
        (
            Token(12, 15, "ExampleContent", "*", "*"),
            Token(17, 25, "ExampleContent", "*", "*"),
        )
    )
    assert len(token.children) == 2


def test_check_set_children_method_for_incorect_data(token):
    with pytest.raises(ValueError):
        token.set_children(20)
        token.set_children(("strs",))


def test_flat_token_without_children():
    token = Token(0, 5, "abc", "*")

    flat = token.flat_token()

    assert flat.start == 0
    assert flat.end == 5
    assert flat.tag == token.tag.name
    assert flat.children == []


def test_flat_token_deep_tree():
    root = Token(0, 10, "r", "*")
    child = Token(1, 9, "c", "*")
    sub = Token(2, 8, "s", "*")

    root.set_child(child)
    child.set_child(sub)

    flat = root.flat_token()

    assert flat.children[0].children[0].start == 2
