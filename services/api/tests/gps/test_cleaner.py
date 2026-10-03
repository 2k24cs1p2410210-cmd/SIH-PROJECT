from app.gps.cleaner import GPSCleaner


def test_gps_cleaner_valid_point():
    cleaner = GPSCleaner()
    assert cleaner.clean_point(lat=15.3647, lon=75.1239, accuracy_m=5.0, speed_mps=10.0) is True


def test_gps_cleaner_noisy_accuracy():
    cleaner = GPSCleaner()
    assert cleaner.clean_point(lat=15.3647, lon=75.1239, accuracy_m=100.0, speed_mps=10.0) is False
