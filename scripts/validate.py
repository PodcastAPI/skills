"""Validate skill metadata, references, packaging boundaries, and review cases."""
import json
import re
import struct
from pathlib import Path

import yaml

from build_plugin import skill_files


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


def validate_openai_marketplace():
    marketplace = load_json('.agents/plugins/marketplace.json')
    assert marketplace['name'] == 'podcastapi'
    assert marketplace['interface']['displayName'] == 'Listen Notes'
    entries = marketplace['plugins']
    assert len(entries) == len({entry['name'] for entry in entries}) == 2
    sources = {entry['name']: entry['source'] for entry in entries}
    assert sources == {
        'podcast-search': {'source': 'local', 'path': './plugins/podcast-search-openai'},
        'podcast-api': {'source': 'local', 'path': './skills/podcast-api'},
    }
    for source in sources.values():
        directory = (ROOT / source['path']).resolve()
        assert directory.is_relative_to(ROOT.resolve()) and directory.is_dir()
    # Import the API skill directly so it cannot also discover the research skill.
    assert (ROOT / sources['podcast-api']['path'] / 'SKILL.md').is_file()
    assert load_json(sources['podcast-search']['path'] + '/plugin.json')['name'] == 'podcast-search'
    canonical = skill_files(ROOT / 'skills/podcast-mcp')
    bundled = skill_files(ROOT / sources['podcast-search']['path'] / 'skills/podcast-mcp')
    assert bundled == canonical, 'Run scripts/build_plugin.py to refresh the bundled research skill.'


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


def validate_openai_plugin():
    source = ROOT / 'plugins/podcast-search-openai'
    plugin = load_json('plugins/podcast-search-openai/plugin.json')
    assert plugin['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert plugin['name'] == 'podcast-search'
    assert re.fullmatch(r'\d+\.\d+\.\d+', plugin['version'])
    assert plugin['author']['name'] == PUBLISHER and plugin['author']['email'] == CONTACT
    assert not plugin.get('apps') and not plugin.get('hooks')
    openai = plugin['extensions']['com.openai']
    interface = openai['interface']
    assert interface['displayName'] == 'Podcast Search by Listen Notes'
    for field in ('displayName', 'shortDescription'):
        assert 1 <= len(interface[field]) <= 30
    assert interface['developerName'] == PUBLISHER
    assert interface['category'] == 'Entertainment'
    for field in ('websiteURL', 'privacyPolicyURL', 'termsOfServiceURL', 'supportURL'):
        assert interface[field].startswith('https://www.listennotes.com/')
    for field in ('logo', 'logoDark', 'composerIcon', 'composerIconDark'):
        path = source / interface[field]
        assert path.resolve().is_relative_to(source.resolve()) and path.is_file()
        data = path.read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) <= 5 * 1024 * 1024
        width, height = struct.unpack('>II', data[16:24])
        assert width == height and 256 <= width <= 4096
    review = openai['review']
    assert review['commerce'] is False
    assert len(review['test_cases']['positive']) >= 5
    assert len(review['test_cases']['negative']) >= 3
    for kind, cases in review['test_cases'].items():
        for case in cases:
            assert case['prompt'].strip() and case['description'].strip()
            if kind == 'positive':
                assert case['tools_triggered'].strip() and case['expected_behavior'].strip()
    assert openai['publication']['countries'] == []  # All directory-supported countries.
    mcp = load_json('plugins/podcast-search-openai/mcp.json')
    assert mcp['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
    assert set(mcp['mcpServers']) == {'listen_notes'}
    server = mcp['mcpServers']['listen_notes']
    assert server['type'] == 'streamable-http'
    assert server['url'] == 'https://mcp.listennotes.com/mcp/'
    assert not ({'headers', 'env', 'command'} & server.keys())
    # Use server-advertised OAuth metadata and scopes to keep the runtime
    # transport declaration compatible across supported clients.
    assert set(server) == {'type', 'url'}, 'Use only type and url; obtain OAuth metadata through server discovery.'
    assert not list(source.rglob('.app.json'))


if __name__ == "__main__":
    validate_skills()
    validate_packaging()
    validate_openai_marketplace()
    validate_cases()
    validate_openai_plugin()
    print("Validated both skills, GitHub marketplaces, MCP dependency, developer-plugin isolation, OpenAI package, and review cases.")
