from . import english_words
from .models import Feedback, SingleFeedback
from .wordlerer import Wordlerer


class App:
    DEFAULT_WORD_SIZE = 5

    FEEDBACK_MAPPING = {
        "c": SingleFeedback.CORRECT,
        "p": SingleFeedback.PRESENT,
        "a": SingleFeedback.ABSENT,
    }

    def get_feedback(self, word: str) -> Feedback:
        print(word)
        while True:
            feedback_input = input("feedback: ")
            if len(feedback_input) != len(word):
                self.print_wrong_size_feedback(len(word))
                continue

            single_feedbacks = []
            for f in feedback_input:
                single_feedback = self.FEEDBACK_MAPPING.get(f)
                if not single_feedback:
                    self.print_invalid_feedback()
                    break
                single_feedbacks.append(single_feedback)
            else:
                return Feedback(single_feedbacks=single_feedbacks)

    @staticmethod
    def print_wrong_size_feedback(size: int):
        print(f"Feedback must have same size as word ({size})")

    def print_invalid_feedback(self):
        feedback_characters = self.FEEDBACK_MAPPING.keys()
        print(f"Feedback must have only these characters: {feedback_characters}")

    def get_word_size(self) -> int:
        while True:
            word_size = input(
                f"word size (leave blank for default: {self.DEFAULT_WORD_SIZE}): "
            )
            if not word_size:
                return self.DEFAULT_WORD_SIZE
            try:
                return int(word_size)
            except Exception:
                print("invalid size, try again")
                continue

    @staticmethod
    def choose(options: list[str]) -> str:
        print(options)
        while True:
            word = input("choose one word: ")
            if word not in options:
                print("this was not an option")
            else:
                return word

    def run(self):
        wordlerer = Wordlerer(
            words=english_words.lower_alpha_set,
            word_size=self.get_word_size(),
            feedback_handler=self.get_feedback,
            choice_handler=self.choose,
        )
        wordlerer.solve()
        print("congrats!")
