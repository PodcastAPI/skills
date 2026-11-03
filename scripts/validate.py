"""Validate skill metadata, references, packaging boundaries, and review cases."""
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("podcast-api", "podcast-mcp")
PUBLISHER = "Listen Notes, Inc."
CONTACT = "hello@listennotes.com"


def load_json(path):
    return json.loads((ROOT / path).read_text())


def validate_skills():
    for name in SKILLS:
        skill_path = ROOT / "skills" / name / "SKILL.md"
        skill = skill_path.read_text()
        header = yaml.safe_load(skill.split("---", 2)[1])
        assert header["name"] == name
        assert header["description"].strip()
        assert header["metadata"]["author"] == PUBLISHER
        assert header["metadata"]["contact"] == CONTACT

        references = re.findall(r"\(references/([^)]+\.md)\)", skill)
        assert references, f"{name} must link to its supporting references"
        for reference in references:
            path = skill_path.parent / "references" / reference
            assert path.is_file(), f"Missing reference: {path}"

    api_skill = (ROOT / "skills/podcast-api/SKILL.md").read_text()
    for value in (
        "LISTEN_API_KEY",
        "X-ListenAPI-Key",
        "https://listen-api.listennotes.com/api/v2",
        "https://listen-api-test.listennotes.com/api/v2",
    ):
        assert value in api_skill, f"podcast-api is missing {value}"

    assert not (ROOT / "skills/podcast-api/agents/openai.yaml").exists()
    agent = yaml.safe_load((ROOT / "skills/podcast-mcp/agents/openai.yaml").read_text())
    assert agent["interface"]["display_name"] == "Podcast Search by Listen Notes"
    assert 25 <= len(agent["interface"]["short_description"]) <= 64
    assert "$podcast-mcp" in agent["interface"]["default_prompt"]
    assert agent["policy"]["allow_implicit_invocation"] is True
    dependencies = agent["dependencies"]["tools"]
    assert len(dependencies) == 1
    dependency = dependencies[0]
    assert dependency["type"] == "mcp"
    assert dependency["value"] == "listen_notes"
    assert dependency["description"].strip()
    assert dependency["transport"] == "streamable_http"
    assert dependency["url"] == "https://mcp.listennotes.com/mcp/"


def validate_packaging():
    marketplace = load_json(".claude-plugin/marketplace.json")
    plugin = load_json(".claude-plugin/plugin.json")
    assert marketplace["name"] == "podcastapi"
    for identity in (marketplace["owner"], plugin["author"]):
        assert identity["name"] == PUBLISHER
        assert identity["email"] == CONTACT

    assert plugin["name"] == "podcast-api"
    assert re.fullmatch(r"\d+\.\d+\.\d+", plugin["version"])
    assert len(marketplace["plugins"]) == 1
    entry = marketplace["plugins"][0]
    assert entry["name"] == "podcast-api"
    assert entry["source"] == "./"
    # Root marketplace entries can restrict the default skills scan. A skills
    # key in plugin.json would only add paths and would not isolate the plugin.
    assert entry["skills"] == ["./skills/podcast-api"]
    assert entry.get("strict", True) is True
    for path in entry["skills"]:
        assert (ROOT / path / "SKILL.md").is_file()
    assert "mcpServers" not in plugin and "mcpServers" not in entry
    assert not (ROOT / ".mcp.json").exists()


def validate_cases():
    for path in ("evals/cases.json", "evals/podcast-mcp.json"):
        cases = load_json(path)
        assert len(cases) >= 6
        assert len({case["id"] for case in cases}) == len(cases)
        for case in cases:
            assert case["prompt"].strip()
            assert case["context"].strip()
            expected = case["expected"]
            assert expected["invariants"] and all(
                isinstance(value, str) and value.strip() for value in expected["invariants"])
            if path == "evals/cases.json":
                assert expected["endpoint"].strip()
            else:
                assert isinstance(expected["activate"], bool)
                assert isinstance(expected["tools"], list)
                assert all(isinstance(tool, str) and tool for tool in expected["tools"])
                if not expected["activate"]:
                    assert not expected["tools"]
        if path == "evals/podcast-mcp.json":
            assert {case["expected"]["activate"] for case in cases} == {False, True}


if __name__ == "__main__":
    validate_skills()
    validate_packaging()
    validate_cases()
    print("Validated both skills, MCP dependency, developer-plugin isolation, and review case structure.")
