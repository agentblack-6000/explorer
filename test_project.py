from project import explore_asteroids, explore_apod, explore_mars_rover_photos


def test_explore_asteroids():
    """Tests explore_asteroids()"""
    assert not explore_asteroids("December 20, 2022", "2022-12-21")
    assert not explore_asteroids("2022-12-21", "December 20, 2022")
    assert not explore_asteroids("2022-12-27", "2022-12-21")

    status_code = explore_asteroids("2022-12-22", "2022-12-25")
    assert status_code == 200

    status_code = explore_asteroids("2022-12-20", "2022-12-26")
    assert status_code == 200


def test_explore_apod():
    """Tests explore_apod()"""
    assert not explore_apod("2023-12-22", "image")
    assert not explore_apod("December 20, 2022", "image")
    assert not explore_apod("2022-12-23", "")

    status_code = explore_apod("2022-12-29", "apod")
    assert status_code == 200

    status_code = explore_apod("2022-12-25", "apod")
    assert status_code == 200


def test_explore_mars_rover_photos():
    """Tests explore_mars_rover_photos()"""
    assert not explore_mars_rover_photos("images", "2022-12-12")
    assert not explore_mars_rover_photos("images.txt", "December 20, 2022")
    assert not explore_mars_rover_photos("images.txt", "2023-13-12")

    status_code = explore_mars_rover_photos("images.txt", "2022-12-23")
    assert status_code == 200

    status_code = explore_mars_rover_photos("images.txt", "2022-12-22")
    assert status_code == 200
