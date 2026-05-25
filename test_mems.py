import pytest
from mems import MemeCollection


@pytest.fixture
def cleanup_collection():
    collections = []
    yield collections
    for collection in collections:
        collection.memes.clear()


@pytest.fixture
def empty_collection(cleanup_collection):
    collection = MemeCollection()
    cleanup_collection.append(collection)
    return collection


@pytest.fixture
def filled_collection(cleanup_collection):
    collection = MemeCollection()
    cleanup_collection.append(collection)
    collection.add_meme("Кот за компьютером", "коты", "100")
    collection.add_meme("Забавное видео", "видео", "50")
    collection.add_meme("Победа в игре", "игра", "200")
    collection.add_meme("Смешная ситуация", "ситуация", "75")
    collection.add_meme("Ещё один кот", "коты", "150")
    return collection


def test_empty(empty_collection):
    assert empty_collection.memes == []


def test_filled(filled_collection):
    assert len(filled_collection.memes) == 5


def test_add(empty_collection):
    result = empty_collection.add_meme("Новый мем", "коты", "10")
    assert result == "Success"


def test_add_count(empty_collection):
    empty_collection.add_meme("Мем", "видео", "25")
    assert len(empty_collection.memes) == 1


def test_add_data(empty_collection):
    empty_collection.add_meme("Тестовый мем", "игра", "42")
    meme = empty_collection.memes[0]
    assert meme["title"] == "Тестовый мем"
    assert meme["category"] == "игра"
    assert meme["likes"] == "42"


def test_category_ok(filled_collection):
    result = filled_collection.get_by_category("коты")
    assert len(result) == 2
    for meme in result:
        assert meme["category"] == "коты"


def test_category_empty(filled_collection):
    result = filled_collection.get_by_category("нет такой")
    assert result == []


def test_popular_none(empty_collection):
    assert empty_collection.get_most_popular() is None


def test_popular_max(filled_collection):
    meme = filled_collection.get_most_popular()
    assert meme["title"] == "Победа в игре"
    assert int(meme["likes"]) == 200


def test_popular_same(empty_collection):
    empty_collection.add_meme("Мем 1", "коты", "100")
    empty_collection.add_meme("Мем 2", "видео", "100")
    meme = empty_collection.get_most_popular()
    assert int(meme["likes"]) == 100


def test_clear(filled_collection):
    filled_collection.clear()
    assert filled_collection.memes == []


@pytest.mark.parametrize(
    "title, category, likes, expected",
    [
        (123, "коты", 10, "title должен быть строкой"),
        ("Мем", 456, 10, "category должен быть строкой"),
        ("Мем", "коты", {"x": 1}, "likes должен быть числом"),
        ("", "коты", 10, "title не должен быть пустым"),
        ("Мем", "", 10, "category не должен быть пустым"),
        ("Мем", "коты", -5, "likes не должен быть отрицательным"),
    ],
)
def test_bad_data(empty_collection, title, category, likes, expected):
    result = empty_collection.add_meme(title, category, likes)
    assert result == expected


def test_likes_number(empty_collection):
    result = empty_collection.add_meme("Мем", "коты", 100)
    assert result == "Success"
    assert empty_collection.memes[0]["likes"] == 100
