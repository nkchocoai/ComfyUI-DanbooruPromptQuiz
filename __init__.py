from .py.node import DanbooruPromptQuiz, DanbooruPromptComparison

NODE_CLASS_MAPPINGS = {
    "DanbooruPromptQuiz": DanbooruPromptQuiz,
    "DanbooruPromptComparison": DanbooruPromptComparison,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DanbooruPromptQuiz": "Danbooru Prompt Quiz",
    "DanbooruPromptComparison": "Danbooru Prompt Comparison",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
