from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

from dotenv import load_dotenv

load_dotenv()

topic = "Generative AI in Medical industry"


# tool 1
llm = LLM(model='gpt-4')

# tool 2
search_tool = SerperDevTool(n=10)

research_analyst = Agent(
    role="Blog researcher from Youtube videos",
    goal=f'Research, analyze, and synthesize comprehensive information on {topic} from reliable web sources',
    verbose=True,
    memory=True,
    backstory="You're an expert research analyst with advanced web research skills."
              "You excel at finding, analyzing, and synthesizing information from"
              "across the internet using search tools. You're skilled at"
              "distinguishing reliable sources from unreliable ones,"
              "fact-checking, cross-referencing information, and"
              "identifying key patterns and insights. You provide"
              "well-organized research briefs with proper citations"
              "and source verification. Your analysis includes both"
              "raw data and interpreted insights, making complex"
              "information accessible and actionable.",
    tools=[search_tool],
    allow_deligations=False,
    llm=llm
)


"""
In CrewAI we've 3 components 
1. Agents - Consider them as characters [Like Researcher agent or Analyst agen]
2. Tasks [imp] - What will the agent do ?
3. Tools - How will i approach a particular task ?
"""
