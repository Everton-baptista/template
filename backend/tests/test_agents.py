import pytest
from app.agents import get_researcher_agent, get_analyst_agent, get_writer_agent, get_coder_agent
from app.teams import get_research_and_writing_team, get_software_dev_team

def test_instantiate_single_agents():
    researcher = get_researcher_agent()
    analyst = get_analyst_agent()
    writer = get_writer_agent()
    coder = get_coder_agent()

    assert researcher.name == "ResearcherAgent"
    assert analyst.name == "AnalystAgent"
    assert writer.name == "WriterAgent"
    assert coder.name == "CoderAgent"

def test_instantiate_multiagent_teams():
    research_team = get_research_and_writing_team()
    dev_team = get_software_dev_team()

    assert research_team.name == "ResearchAndWritingTeamLeader"
    assert len(research_team.members) == 3
    assert dev_team.name == "SoftwareDevTeamLeader"
    assert len(dev_team.members) == 2
