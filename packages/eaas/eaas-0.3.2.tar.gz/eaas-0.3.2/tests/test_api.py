# %%
from eaas import Client, Config
import jsonlines
from pathlib import Path
import os
import unittest

curr_dir = Path(__file__).parent


def read_jsonlines_to_list(file_name):
    lines = []
    with jsonlines.open(file_name, 'r') as reader:
        for obj in reader:
            lines.append(obj)
    return lines


class TestMetrics(unittest.TestCase):
    def test_api(self):
        client = Client()
        config = Config()
        client.load_config(config)

        input_file = os.path.join(curr_dir, "inputs", "multi_references.jsonl")
        inputs = read_jsonlines_to_list(input_file)
        res = client.score(inputs)
        print(res)

    def test_multilingual(self):
        client = Client()
        config = Config()
        client.load_config(config)

        for lang in ["en", "fr", "zh"]:
            # Single ref
            print(f"****** LANG: {lang} ******")
            print("For single reference")
            input_file = os.path.join(curr_dir, "inputs", f"{lang}_single_ref_tiny.jsonl")
            inputs = read_jsonlines_to_list(input_file)
            res = client.score(inputs, task="sum", metrics=None, lang=lang)
            print(res)

            # Multi ref
            print(f"For multiple references")
            input_file = os.path.join(curr_dir, "inputs", f"{lang}_multi_ref_tiny.jsonl")
            inputs = read_jsonlines_to_list(input_file)
            res = client.score(inputs, task="sum", metrics=None, lang=lang)
            print(res)
