#!/usr/bin/env python3
"""ARIS Codex 最终科研工作流修复的行为契约测试。"""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
CODEX = ROOT / "skills" / "skills-codex"

def read_skill(name):
    return (CODEX / name / "SKILL.md").read_text()

class ResearchCustomizationContractTest(unittest.TestCase):
    def test_p0_p4_are_the_single_formal_definition(self):
        methodology = (CODEX / "shared-references" / "research-methodology-cn.md").read_text()
        expected = {
            "P0：作者在 Limitation": "作者明确线索",
            "P1：实验直接暴露": "实验直接问题",
            "P2：多个相关工作共同": "跨论文归纳",
            "P3：根据方法的假设": "机制性推导",
            "P4：探索性构想": "探索性构想",
        }
        for phrase in expected:
            self.assertIn(phrase, methodology)
        lit = read_skill("research-lit")
        self.assertIn("唯一正式定义", lit)
        self.assertNotIn("P0 是核心 limitation/失败", lit)

    def test_native_banlist_semantics_are_restored(self):
        files = [
            CODEX / "shared-references" / "research-methodology-cn.md",
            CODEX / "idea-creator" / "SKILL.md",
            CODEX / "research-wiki" / "SKILL.md",
        ]
        combined = "\n".join(p.read_text() for p in files)
        self.assertNotIn("conditional " + "banlist", combined)
        self.assertIn("failed-ideas banlist", combined)
        self.assertIn("失败背景", combined)

    def test_experiment_layers_keep_pilot_light_and_formal_heavy(self):
        plan = read_skill("experiment-plan")
        for phrase in (
            "已有结果",
            "直接复用已有结果",
            "Diagnostic/Mechanism",
            "一次只回答一个最关键的不确定性",
            "Formal Evaluation",
            "multi-seed",
            "Formal Infra Plan",
            "不要求 multi-seed",
            "不自动升级为 Formal claim",
        ):
            self.assertIn(phrase, plan)
        self.assertIn("H/Q/M/B/E 用来定位问题，不要求 Pilot 覆盖所有 H、M 或 B", plan)

    def test_idea_creator_has_real_pilot_update_contract(self):
        creator = read_skill("idea-creator")
        for phrase in (
            "pilot_verdict",
            "target_hypothesis",
            "primary_signal",
            "failure_attribution",
            "next_action",
            "update_on_exist",
            "Pilot 的 `strong_positive` 只表示继续研究",
        ):
            self.assertIn(phrase, creator)

    def test_wiki_writes_diagnostics_and_query_pack_reads_lessons(self):
        helper = (ROOT / "tools" / "research_wiki.py").read_text()
        for phrase in ("target_hypothesis", "primary_signal", "diagnostics", "failure_attribution", "Recent Pilot Lessons"):
            self.assertIn(phrase, helper)
        with tempfile.TemporaryDirectory() as directory:
            wiki = Path(directory) / "research-wiki"
            subprocess.run(["python3", "tools/research_wiki.py", "init", str(wiki)], cwd=ROOT, check=True, capture_output=True, text=True)
            result = subprocess.run([
                "python3", "tools/research_wiki.py", "upsert_idea", str(wiki),
                "--title", "Pilot lesson", "--pilot-verdict", "inconclusive",
                "--target-hypothesis", "signal reaches action",
                "--primary-signal", "ranking changed but action did not",
                "--diagnostics", "signal was created upstream",
                "--failure-attribution", "signal_not_transmitted",
                "--next-action", "diagnose", "--provenance", "runs/pilot-1",
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            idea = next((wiki / "ideas").glob("*.md"))
            content = idea.read_text()
            self.assertIn("pilot_verdict:", content)
            self.assertIn("inconclusive", content)
            self.assertIn("ranking changed but action did not", content)
            subprocess.run(["python3", "tools/research_wiki.py", "rebuild_query_pack", str(wiki)], cwd=ROOT, check=True, capture_output=True, text=True)
            self.assertIn("Recent Pilot Lessons", (wiki / "query_pack.md").read_text())
            subprocess.run(["python3", "tools/research_wiki.py", "upsert_idea", str(wiki), "--slug", idea.stem, "--title", "Pilot lesson", "--pilot-verdict", "clear_negative", "--target-hypothesis", "H", "--primary-signal", "none", "--diagnostics", "updated lesson", "--failure-attribution", "signal_not_created", "--next-action", "archive", "--update-on-exist"], cwd=ROOT, check=True, capture_output=True, text=True)
            updated = idea.read_text()
            self.assertIn("_TODO: the core hypothesis / direction._", updated)
            self.assertIn("updated lesson", updated)
            self.assertIn("outcome: pending", updated)

    def test_profiles_remain_unchanged_scope(self):
        self.assertTrue((ROOT / "profiles" / "research.tsv").exists())
        self.assertTrue((ROOT / "profiles" / "experiment.tsv").exists())

if __name__ == "__main__":
    unittest.main()
