from app.pipeline import progress_line

def test_progress_line():
    assert progress_line(300, 2100) == "  extracted 300 of 2100"
    assert progress_line(0, 2100) is None
    assert progress_line(50, 2100, 50) == "  extracted 50 of 2100"