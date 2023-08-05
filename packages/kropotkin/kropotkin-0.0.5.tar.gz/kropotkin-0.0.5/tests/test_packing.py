import json
from string import printable

from hypothesis import assume, given
from hypothesis.strategies import (
    booleans,
    dictionaries,
    lists,
    none,
    recursive,
    text,
)

from kropotkin import pack, unpack

# floats aren't used as msgpack actually inflates short ones
json_fixture = recursive(
    none() | booleans() | text(printable),
    lambda children: lists(children, min_size=1, max_size=4)
    | dictionaries(text(printable), children, min_size=1, max_size=4),
)


@given(json_fixture)
def test_unpack_inverts_pack(j):
    assert unpack(pack(j)) == j


@given(json_fixture)
def test_pack_smaller_than_json_serialise(j):
    packed = pack(j)
    as_json = json.dumps(j)
    # 1. Don't worry if packing is bigger for small input
    # 2. Do worry if JSON dumps would have been smaller
    # 3. ...unless the overhead of packing is marginal
    assert (
        len(packed) <= 16
        or len(packed) <= len(as_json)
        or len(packed) - len(as_json) <= 6
    )


@given(json_fixture)
def test_pack_small_for_reasonable_structures(j):
    # About half what IE allows?
    assert len(pack(j)) <= 1024


@given(json_fixture)
def test_appending_to_arrays(j):
    assume(isinstance(j, list))
    # Imagine we previously sent a user to a URL with j encoded
    packed = pack(j)
    # Then the user fetches that URL so we unserialise j back as fresh state data
    data = unpack(packed)
    # Then our service wants to offer a URL to another state with an item appended
    assume("potato" not in data)
    afforded_state = data + ["potato"]

    assert "potato" in unpack(pack(afforded_state))
