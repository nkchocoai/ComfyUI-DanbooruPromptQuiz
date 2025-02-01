from .server import MessageHolder

from comfy.sd1_clip import token_weights


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False


any = AlwaysEqualProxy("*")


class DanbooruPromptQuiz:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "input": ("STRING", {"default": "", "multiline": True}),
                "answer": (
                    "STRING",
                    {"forceInput": True},
                ),
            },
            "optional": {
                "any": (any, {}),
            },
            "hidden": {
                "id": "UNIQUE_ID",
            },
        }

        return inputs

    RETURN_TYPES = (
        "FLOAT",
        "FLOAT",
        "FLOAT",
        "FLOAT",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "accuracy",
        "precision",
        "recall",
        "f1-measure",
        "correct tags (TP)",
        "wrong tags (FP)",
        "missing tags (FN)",
        "input",
        "answer",
    )
    FUNCTION = "check"

    def check(self, id, input, answer, any):
        message = MessageHolder.waitForMessage(id)
        (
            accuracy,
            precision,
            recall,
            f1,
            correct_tags,
            wrong_tags,
            missing_tags,
        ) = self._check(message, answer)
        return (
            accuracy,
            precision,
            recall,
            f1,
            correct_tags,
            wrong_tags,
            missing_tags,
            message,
            answer,
        )

    def _check(self, input, answer):
        input_tags = []
        for t, _ in token_weights(input, 1.0):
            for tag in t.split(","):
                tag = tag.strip()
                if tag:
                    input_tags.append(tag)

        answer_tags = []
        for t, _ in token_weights(answer, 1.0):
            for tag in t.split(","):
                tag = tag.strip()
                if tag:
                    answer_tags.append(tag)

        correct_tags = []
        wrong_tags = []
        missing_tags = []
        for t in input_tags:
            if t in answer_tags and t not in correct_tags:
                correct_tags.append(t)
            elif t not in answer_tags and t not in wrong_tags:
                wrong_tags.append(t)
        for t in answer_tags:
            if t not in input_tags and t not in missing_tags:
                missing_tags.append(t)

        tp = len(correct_tags)
        fp = len(wrong_tags)
        fn = len(missing_tags)
        accuracy = tp / (tp + fp + fn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * precision * recall / (precision + recall)

        return (
            accuracy,
            precision,
            recall,
            f1,
            ", ".join(correct_tags),
            ", ".join(wrong_tags),
            ", ".join(missing_tags),
        )


class DanbooruPromptComparison(DanbooruPromptQuiz):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "input": ("STRING", {"default": "", "multiline": True}),
                "answer": ("STRING", {"default": "", "multiline": True}),
            },
        }

        return inputs

    def check(self, input, answer):
        (
            accuracy,
            precision,
            recall,
            f1,
            correct_tags,
            wrong_tags,
            missing_tags,
        ) = self._check(input, answer)
        return (
            accuracy,
            precision,
            recall,
            f1,
            correct_tags,
            wrong_tags,
            missing_tags,
            input,
            answer,
        )
