from enum import Enum

from pydantic import BaseModel


class SingleFeedback(str, Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


class Feedback(BaseModel):
    single_feedbacks: list[SingleFeedback] = []
    word_in_list: bool = True
