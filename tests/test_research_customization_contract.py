#!/usr/bin/env python3
"""ARIS Codex 科研工作流二次定制的最小契约测试。"""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
CODEX = ROOT / "skills" / "skills-codex"

def read(name):
    return (CODEX / name / "SKILL.md").read_text()

class ResearchCustomizationContractTest(unittest.TestCase):
    def test_methodology_protocol(self):
        s = (CODEX / "shared-references" / "research-methodology-cn.md").read_text()
        for token in ("第一轮", "第二轮", "五集合", "P0–P4", "Insight Card", "H/Q/M/B/E", "strong_positive", "inconclusive", "Research Wiki", "Notion", "Impact Check", "语义依赖传播"):
            self.assertIn(token, s)

    def test_literature_is_two_round_and_materialized(self):
        s = read("research-lit")
        for token in ("Round 1", "Round 2", "收集 → 精读 → 五集合 → 跨论文归纳", "LITERATURE_ROUND1.md", "LITERATURE_ROUND2.md", "PROBLEM_EVIDENCE_PACK.md", "P0–P4"):
            self.assertIn(token, s)

    def test_idea_and_pilot_contract(self):
        creator = read("idea-creator")
        discovery = read("idea-discovery")
        for token in ("Insight Card", "target_hq", "failure_attribution", "strong_positive", "clear_negative", "CUDA_VISIBLE_DEVICES=0,1"):
            self.assertIn(token, creator)
        self.assertIn("AUTO_PROCEED = true", discovery)
        for token in ("PROBLEM_EVIDENCE_PACK", "pilot_status", "inconclusive", "不以“Pilot 必须 positive”"):
            self.assertIn(token, discovery)

    def test_refine_experiment_and_bridge_contract(self):
        refine = read("research-refine")
        plan = read("experiment-plan")
        bridge = read("experiment-bridge")
        impl = read("research-implementation-plan")
        for token in ("SCORE_THRESHOLD = 9", "Impact Check", "Revision Propagation & Consistency Check", "证据 → 问题/Insight → H/Q → M → B/E → claim"):
            self.assertIn(token, refine)
        for token in ("Research Map", "Pilot Evidence", "Diagnostic/Mechanism", "Formal Evaluation", "Formal Infra Plan"):
            self.assertIn(token, plan)
        self.assertIn("/research-implementation-plan", bridge)
        for token in ("文件、类/函数", "Consistency Check", "IMPLEMENTATION_PLAN.md"):
            self.assertIn(token, impl)

    def test_wiki_persists_pilot_diagnostics(self):
        helper = (ROOT / "tools" / "research_wiki.py").read_text()
        for token in ("pilot_status", "pilot_diagnostics", "failure_attribution", "target_hq", "isolated_mbe"):
            self.assertIn(token, helper)

    def test_profiles_are_executable(self):
        for profile, expected in (("research", "idea-discovery"), ("experiment", "experiment-bridge")):
            path = ROOT / "profiles" / f"{profile}.tsv"
            self.assertIn("skills\t", path.read_text())
            with tempfile.TemporaryDirectory() as project:
                proc = subprocess.run(
                    ["bash", "tools/install_aris_codex.sh", project, "--aris-repo", str(ROOT), "--profile", profile, "--dry-run", "--no-doc"],
                    cwd=ROOT, text=True, capture_output=True, check=False,
                )
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                self.assertIn("Selection:", proc.stdout)
                self.assertIn(expected, path.read_text())

if __name__ == "__main__":
    unittest.main()
