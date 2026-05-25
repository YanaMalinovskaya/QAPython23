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
    sample_memes = [
        ("Кот за компьютером", "коты", "100"),
        ("Забавное видео", "видео", "50"),
        ("Победа в игре", "игра", "200"),
        ("Смешная ситуация", "ситуация", "75"),
        ("Ещё один кот", "коты", "150"),
    ]
    for title, category, likes in sample_memes:
        collection.add_meme(title, category, likes)
    return collection


class TestMemeCollectionBasics:
    def test_new_collection_is_empty(self, empty_collection):
        assert empty_collection.memes == []

    def test_filled_collection_contains_memes(self, filled_collection):
        assert len(filled_collection.memes) == 5

    def test_add_meme_returns_success(self, empty_collection):
        result = empty_collection.add_meme("Новый мем", "коты", "10")
        assert result == "Success"

    def test_add_meme_increases_count(self, empty_collection):
        empty_collection.add_meme("Новый мем", "видео", "25")
        assert len(empty_collection.memes) == 1

    def test_add_meme_stores_correct_data(self, empty_collection):
        empty_collection.add_meme("Тестовый мем", "игра", "42")
        meme = empty_collection.memes[0]
        assert meme["title"] == "Тестовый мем"
        assert meme["category"] == "игра"
        assert meme["likes"] == "42"


class TestGetByCategory:
    def test_get_by_category_existing(self, filled_collection):
        result = filled_collection.get_by_category("коты")
        assert len(result) == 2
        assert all(meme["category"] == "коты" for meme in result)

    def test_get_by_category_not_existing(self, filled_collection):
        result = filled_collection.get_by_category("несуществующая")
        assert result == []


class TestGetMostPopular:
    def test_get_most_popular_empty_collection(self, empty_collection):
        assert empty_collection.get_most_popular() is None

    def test_get_most_popular_different_likes(self, filled_collection):
        most_popular = filled_collection.get_most_popular()
        assert most_popular["title"] == "Победа в игре"
        assert int(most_popular["likes"]) == 200

    def test_get_most_popular_equal_likes(self, empty_collection):
        empty_collection.add_meme("Мем A", "коты", "100")
        empty_collection.add_meme("Мем B", "видео", "100")
        most_popular = empty_collection.get_most_popular()
        assert int(most_popular["likes"]) == 100
        assert most_popular["title"] in ("Мем A", "Мем B")


class TestClearCollection:
    def test_clear_empties_collection(self, filled_collection):
        filled_collection.clear()
        assert filled_collection.memes == []


class TestAddMemeValidation:
    @pytest.mark.parametrize(
        "title,category,likes,expected_message",
        [
            (123, "коты", 10, "title должен быть строкой"),
            ("Мем", 456, 10, "category должен быть строкой"),
            ("Мем", "коты", {"likes": 10}, "likes должен быть числом"),
            ("", "коты", 10, "title не должен быть пустым"),
            ("Мем", "", 10, "category не должен быть пустым"),
            ("Мем", "коты", -5, "likes не должен быть отрицательным"),
        ],
    )
    def test_add_meme_invalid_data(
        self, empty_collection, title, category, likes, expected_message
    ):
        result = empty_collection.add_meme(title, category, likes)
        assert result == expected_message

    @pytest.mark.parametrize(
        "title,category,likes",
        [
            ("Мем про кота", "коты", "100"),
            ("Видео мем", "видео", "0"),
            ("Игровой мем", "игра", "1"),
        ],
    )
    def test_add_meme_valid_string_likes(
        self, empty_collection, title, category, likes
    ):
        result = empty_collection.add_meme(title, category, likes)
        assert result == "Success"
        meme = empty_collection.memes[-1]
        assert meme["title"] == title
        assert meme["category"] == category
        assert meme["likes"] == likes

    @pytest.mark.parametrize(
        "title,category,likes",
        [
            ("Мем про кота", "коты", 100),
            ("Видео мем", "видео", 0),
            ("Игровой мем", "игра", 1),
        ],
    )
    def test_add_meme_valid_numeric_likes(
        self, empty_collection, title, category, likes
    ):
        result = empty_collection.add_meme(title, category, likes)
        assert result == "Success"
        meme = empty_collection.memes[-1]
        assert meme["title"] == title
        assert meme["category"] == category
        assert meme["likes"] == likes
