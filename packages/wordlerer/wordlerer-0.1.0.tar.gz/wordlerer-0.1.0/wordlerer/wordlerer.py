import random
from typing import Callable, Optional

from . import utils
from .models import Feedback, SingleFeedback


class Wordlerer:
    def __init__(
        self,
        words: list[str],
        word_size: int,
        feedback_handler: Callable[[str], Feedback],
        choice_handler: Optional[Callable[[list[str]], str]] = None,
    ):
        self.words = utils.filter_by_length(words, word_size)
        self.word_size = word_size
        self.feedback_handler = feedback_handler
        self.choice_handler = choice_handler or random.choice

    def solve(self) -> bool:
        options = self.words
        for _ in range(6):
            word_attempt = self.choice_handler(options)
            feedback = self.feedback_handler(word_attempt)
            if not feedback.word_in_list:
                continue

            correct_feedback_size = len(feedback.single_feedbacks) == self.word_size
            all_correct_spots = all(
                f == SingleFeedback.CORRECT for f in feedback.single_feedbacks
            )
            if correct_feedback_size and all_correct_spots:
                # win
                return True

            options = self._get_options(options, word_attempt, feedback)
        return False

    def _get_options(
        self, words: list[str], word_attempt: str, feedback: Feedback
    ) -> list[str]:
        assert len(word_attempt) == self.word_size
        assert len(feedback.single_feedbacks) == self.word_size

        options = [
            word for word in words if self._is_option(feedback, word, word_attempt)
        ]
        return sorted(options)

    def _is_option(self, feedback, word, word_attempt) -> bool:
        present_letters = []
        absent_letters = []
        correct_indexes = []
        for i, c in enumerate(word_attempt):
            if feedback.single_feedbacks[i] == SingleFeedback.CORRECT:
                if c != word[i]:
                    break
                correct_indexes.append(i)
            elif feedback.single_feedbacks[i] == SingleFeedback.PRESENT:
                if c == word[i]:
                    break
                present_letters.append(c)
            else:
                absent_letters.append(c)
        else:
            if self._check_against_present_letters(word, present_letters):
                return self._check_against_absent_letters(
                    word, correct_indexes, absent_letters, present_letters
                )
        return False

    @staticmethod
    def _check_against_absent_letters(
        word: str,
        correct_indexes: list[int],
        absent_letters: list[str],
        present_letters: list[str],
    ) -> bool:
        letters_without_correct = "".join(
            [letter for i, letter in enumerate(word) if i not in correct_indexes]
        )
        return not any(
            (
                absent_letter not in present_letters
                and absent_letter in letters_without_correct
            )
            for absent_letter in absent_letters
        )

    @staticmethod
    def _check_against_present_letters(word: str, present_letters: list[str]) -> bool:
        return all(present_letter in word for present_letter in present_letters)
