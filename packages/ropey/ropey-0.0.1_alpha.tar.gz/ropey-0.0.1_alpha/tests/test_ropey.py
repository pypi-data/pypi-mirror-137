import pytest
from ropey import Rope
from itertools import product as _p


TEXTS = [
    "I speak English",
    "Je parle français",
    "This should be a nice test since the sentence might a longer than the others",
    "This is\na\nmultiline\nstring",
]

SLICES = [
    slice(None, None),
    slice(4, None),
    slice(None, 6),
    slice(3, 7),
]


class TestRope:
    def test_new(self):
        r = Rope()

    @pytest.mark.parametrize("text", TEXTS)
    def test_from_str(self, text):
        assert text == Rope.from_str(text).text

    def test_from_reader(self):
        with pytest.raises(NotImplementedError):
            Rope.from_reader(None)

    def test_write_to(self):
        with pytest.raises(NotImplementedError):
            Rope().write_to(None)

    @pytest.mark.parametrize("text", TEXTS)
    def test_len_chars(self, text):
        assert len(text) == Rope.from_str(text).len_chars()

    @pytest.mark.parametrize("text", TEXTS)
    def test_len_lines(self, text):
        assert len(text.splitlines()) == Rope.from_str(text).len_lines()

    @pytest.mark.parametrize("text", TEXTS)
    def test_remove_full(self, text):
        r = Rope.from_str(text)
        r.remove_range_full()
        assert "" == r.text

    @pytest.mark.parametrize("text,slc", _p(TEXTS, SLICES))
    def test_remove_range(self, text, slc):
        start = slc.start or 0
        stop = slc.stop or len(text)
        r = Rope.from_str(text)
        r.remove(slc)
        assert text[:start] + text[stop:] == r.text

    @pytest.mark.parametrize("text,char_idx", _p(TEXTS, [1, 2, 3, 4, 5]))
    def test_split_off(self, text, char_idx):
        r = Rope.from_str(text).split_off(char_idx)
        assert text[char_idx:] == r.text

    @pytest.mark.parametrize("text_a, text_b", _p(TEXTS, TEXTS))
    def test_append(self, text_a, text_b):
        r = Rope.from_str(text_a)
        r.append(Rope.from_str(text_b))
        assert text_a + text_b == r.text
