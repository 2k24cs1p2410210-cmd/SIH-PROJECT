from src.models.baseline_current_speed import BaselineCurrentSpeedModel


def test_baseline_speed_model():
    model = BaselineCurrentSpeedModel()
    eta = model.predict(1000.0, 10.0)
    assert eta == 100.0
