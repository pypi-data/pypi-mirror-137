import json
import sys
import warnings
from collections import defaultdict
from time import gmtime, strftime
from typing import List, Dict

import requests
from tqdm import trange

from eaas.config import Config

BATCH_SIZE = 100


class Client:
    def __init__(self):
        """ A client wrapper """
        # self.end_point = "http://18.224.144.134/"
        self._record_end_point = "http://piaget.lti.cs.cmu.edu:6666/record"
        self._score_end_point = "http://piaget.lti.cs.cmu.edu:6666/score"
        # self._record_end_point = "http://clio.lti.cs.cmu.edu:6666/record"
        # self._score_end_point = "http://clio.lti.cs.cmu.edu:6666/score"
        self._valid_metrics = [
            "bart_score_cnn_hypo_ref",
            "bart_score_summ",
            "bart_score_mt",
            "bert_score_p",
            "bert_score_r",
            "bert_score_f",
            "bleu",
            "chrf",
            "comet",
            "comet_qe",
            "mover_score",
            "prism",
            "prism_qe",
            "rouge1",
            "rouge2",
            "rougeL"
        ]
        self._config = None

    def load_config(self, config: Config):
        assert isinstance(config, Config), "You should pass a Config class defined in eaas.config"
        self._config = config.to_dict()

    @property
    def metrics(self):
        return self._valid_metrics

    def log_request(self, inputs, metrics):
        """ Log the metadata of this request. """

        def word_count(l):
            """ count words in a list (or list of list)"""
            c = 0
            for x_ in l:
                if isinstance(x_, List):
                    c += word_count(x_)
                else:
                    c += len(x_.split(" "))
            return c

        srcs = [x["source"] for x in inputs]
        refs = [x["references"] for x in inputs]
        hypos = [x["hypothesis"] for x in inputs]

        srcs_wc = word_count(srcs)
        refs_wc = word_count(refs)
        hypos_wc = word_count(hypos)

        return {
            "date:": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "user": "placeholder",
            "metrics": metrics,
            "src_tokens": srcs_wc,
            "refs_tokens": refs_wc,
            "hypos_tokens": hypos_wc
        }

    # TODO: Beautify bleu, rouge1, rouge2, rougeL
    def bleu(self, refs: List[List[str]], hypos: List[str], lang="en"):
        assert self._config is not None, "You should use load_config first to load metric configurations."
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})
        data = {
            "inputs": inputs,
            "metrics": ["bleu"],
            "config": self._config,
            "task": "mt",
            "cal_attributes": False
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

        scores = rjson["scores"]
        assert len(scores["bleu"]) == len(inputs)
        return scores

    def rouge1(self, refs: List[List[str]], hypos: List[str], lang="en"):
        assert self._config is not None, "You should use load_config first to load metric configurations."
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})
        data = {
            "inputs": inputs,
            "metrics": ["rouge1"],
            "config": self._config,
            "task": "sum",
            "cal_attributes": False
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

        scores = rjson["scores"]
        assert len(scores["rouge_1"]) == len(inputs)
        return scores

    def rouge2(self, refs: List[List[str]], hypos: List[str], lang="en"):
        assert self._config is not None, "You should use load_config first to load metric configurations."
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})
        data = {
            "inputs": inputs,
            "metrics": ["rouge2"],
            "config": self._config,
            "task": "sum",
            "cal_attributes": False
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

        scores = rjson["scores"]
        assert len(scores["rouge_2"]) == len(inputs)
        return scores

    def rougeL(self, refs: List[List[str]], hypos: List[str], lang="en"):
        assert self._config is not None, "You should use load_config first to load metric configurations."
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})
        data = {
            "inputs": inputs,
            "metrics": ["rougeL"],
            "config": self._config,
            "task": "sum",
            "cal_attributes": False
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

        scores = rjson["scores"]
        assert len(scores["rouge_l"]) == len(inputs)
        return scores

    def score(self, inputs: List[Dict], task="sum", metrics=None, lang="en"):
        assert self._config is not None, "You should use load_config first to load metric configurations."

        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang

        if metrics is None:
            metrics = self._valid_metrics
            warnings.warn("You didn't specify the metrics, will use all valid metrics by default.")
        else:
            for metric in metrics:
                assert metric in self._valid_metrics, "Your have entered invalid metric, please check."

        # First record the request
        metadata = self.log_request(inputs, metrics)
        response = requests.post(url=self._record_end_point, json=json.dumps(metadata))
        if response.status_code != 200:
            raise RuntimeError("Internal server error.")
        print(f"EaaS: Your request has been sent.", file=sys.stderr)

        inputs_len = len(inputs)

        final_score_dic = {}

        def attr_in_dic(_dic):
            _flag = False
            for _k in _dic:
                if "attr" in _k:
                    _flag = True
            return _flag

        # First deal with BLEU and CHRF
        if "bleu" in metrics:

            data = {
                "inputs": inputs,
                "metrics": ["bleu"],
                "config": self._config,
                "task": task,
                "cal_attributes": not attr_in_dic(final_score_dic)
            }
            response = requests.post(
                url=self._score_end_point,
                json=json.dumps(data),
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

            scores = rjson["scores"]
            assert len(scores["bleu"]) == inputs_len
            final_score_dic["bleu"] = scores["bleu"]
            final_score_dic["corpus_bleu"] = scores["corpus_bleu"]
            for k, v in scores.items():
                if "attr" in k:
                    final_score_dic[k] = v
                    final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

            metrics.remove("bleu")

        if "chrf" in metrics:
            data = {
                "inputs": inputs,
                "metrics": ["chrf"],
                "config": self._config,
                "task": task,
                "cal_attributes": not attr_in_dic(final_score_dic)
            }
            response = requests.post(
                url=self._score_end_point,
                json=json.dumps(data)
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

            scores = rjson["scores"]
            assert len(scores["chrf"]) == inputs_len
            final_score_dic["chrf"] = scores["chrf"]
            final_score_dic["corpus_chrf"] = scores["corpus_chrf"]
            for k, v in scores.items():
                if "attr" in k:
                    final_score_dic[k] = v
                    final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

            metrics.remove("chrf")

        # Deal with the inputs 100 samples at a time
        score_dic = defaultdict(list)
        for i in trange(0, len(inputs), BATCH_SIZE, desc="Calculating scores."):
            data = {
                "inputs": inputs[i: i + BATCH_SIZE],
                "metrics": metrics,
                "config": self._config,
                "task": task,
                "cal_attributes": not attr_in_dic(final_score_dic)
            }

            response = requests.post(
                url=self._score_end_point,
                json=json.dumps(data)
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(f"[Error on metric: {rjson['metric']}]\n[Error Message]: {rjson['message']}")

            scores = rjson["scores"]

            for k, v in scores.items():
                if "corpus" in k:
                    continue
                score_dic[k] += v

        # Aggregate scores and get corpus-level scores for some metrics
        for k, v in score_dic.items():
            assert len(v) == inputs_len
            final_score_dic[k] = v
            final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

        # Reformat the returned dict
        sample_level = []
        for i in range(len(inputs)):
            sample_level.append({})
        corpus_level = {}
        reformatted_final_score_dic = {}
        for k, v in final_score_dic.items():
            if "corpus" in k:
                corpus_level[k] = v
            else:
                for i in range(len(inputs)):
                    sample_level[i][k] = v[i]

        reformatted_final_score_dic["sample_level"] = sample_level
        reformatted_final_score_dic["corpus_level"] = corpus_level

        return reformatted_final_score_dic

    def signature(self):
        pass
