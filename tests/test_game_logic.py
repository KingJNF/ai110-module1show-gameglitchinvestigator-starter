from logic_utils import check_guess
import sys
sys.path.insert(0, '..')
from app import get_range_for_difficulty, attempt_limit_map

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# Tests for bug fixes
class TestDifficultyRanges:
    """Test that difficulty ranges are correct after fixing the bug."""
    
    def test_easy_range(self):
        """Easy difficulty should be 1-20"""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20
    
    def test_normal_range(self):
        """Normal difficulty should be 1-50"""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 50
    
    def test_hard_range(self):
        """Hard difficulty should be 1-100"""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 100


class TestAttemptLimits:
    """Test that attempt limits are correct for each difficulty."""
    
    def test_easy_attempts(self):
        """Easy should have 10 attempts"""
        assert attempt_limit_map["Easy"] == 10
    
    def test_normal_attempts(self):
        """Normal should have 8 attempts"""
        assert attempt_limit_map["Normal"] == 8
    
    def test_hard_attempts(self):
        """Hard should have 5 attempts"""
        assert attempt_limit_map["Hard"] == 5


class TestHints:
    """Test that hints are correct after fixing the reversed hints bug."""
    
    def test_guess_too_high_shows_go_lower(self):
        """When guess is too high, hint should say 'Go LOWER!'"""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in message
        assert message == "📉 Go LOWER!"
    
    def test_guess_too_low_shows_go_higher(self):
        """When guess is too low, hint should say 'Go HIGHER!'"""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message
        assert message == "📈 Go HIGHER!"
