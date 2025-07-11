from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool

from dotenv import load_dotenv

load_dotenv()


class AgentFactory:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search_tool = search_tool

    def research_analyst(self, topic: str):
        research_analyst = Agent(
            role="Seasoned and the best Research analyst of the world",
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
            tools=[self.search_tool],
            allow_deligations=False,
            llm=self.llm
        )

        return research_analyst

    def content_writer(self, topic: str):
        content_writer = Agent(
            role="Senior content writer",
            goal="Transform, research findings into engaging blog post while maintaining accuracy",
            backstory="You're are skilled content writer specialized in creating"
                      "engaging, accessible content from technical research. "
                      "You work closely with the Senior Research Analyst and excel at maintaining the perfect "
                      "balance between informative and entertaining writing, "
                      "while ensuring all facts and citations from the research "
                      "are properly incorporated. You have a talent for making "
                      "complex topics approachable without oversimplifying them.",
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
        return content_writer

    def create_research_task(self, agent, topic):
        return Task(
            description=(
                f"""
                1. Conduct comprehensive research on {topic} including:
                   - Recent developments and news
                   - Key industry trends and innovations
                   - Expert opinions and analyses
                   - Statistical data and market insights
                2. Evaluate source credibility and fact-check all information
                3. Organize findings into a structured research brief
                4. Include all relevant citations and sources   
                """
            ),
            expected_output="""
            A detailed research report containing:
            - Executive summary of key findings
            - Comprehensive analysis of current trends and developments
            - List of verified facts and statistics
            - All citations and links to original sources
            - Clear categorization of main themes and patterns
            Please format with clear sections and bullet points for easy reference.
            """,
            agent=agent
        )

    def create_writing_task(self, agent):
        return Task(
            description="""
                Using the research brief provided, create an engaging blog post that:
                1. Transforms technical information into accessible content
                2. Maintains all factual accuracy and citations from the research
                3. Includes:
                   - Attention-grabbing introduction
                   - Well-structured body sections with clear headings
                   - Compelling conclusion
                4. Preserves all source citations in [Source: URL] format
                5. Includes a References section at the end
            """,
            expected_output="""
            A polished blog post in markdown format that:
            - Engages readers while maintaining accuracy
            - Contains properly structured sections
            - Includes inline citations hyperlinked to the original source URL
            - Presents information in an accessible yet informative way
            - Follows proper markdown formatting, using H1 for the title and H3 for the sub-sections
            """,
            agent=agent
        )


def main(topic: str):
    # topic = "Generative AI in Medical industry"

    # tool 1
    llm = LLM(model='gpt-4')

    # tool 2
    search_tool = SerperDevTool(n=10)

    factory = AgentFactory(llm, search_tool)

    # create agents
    research_analyst = factory.research_analyst(topic)
    content_writer = factory.content_writer(topic)

    # create tasks
    research_tasks = factory.create_research_task(research_analyst, topic)
    writing_task = factory.create_writing_task(content_writer)

    # crew = Crew(
    #     agents=[research_analyst, content_writer],
    #     tasks=[research_tasks, writing_task],
    #     process=Process.sequential,     # serialized way
    #     memory=True,
    #     cache=True,
    #     verbose=True
    # )

    # Ensure to provide a manager_llm or manager_agent
    crew = Crew(
        agents=[research_analyst, content_writer],
        tasks=[research_tasks, writing_task],
        process=Process.hierarchical,  # hierarchical process
        manager_llm='gpt-4o',
        memory=True,
        cache=True,
        verbose=True
    )

    try:
        result = crew.kickoff(inputs={"topic": topic})
    except Exception as e:
        print(f"Error during crew execution: {e}")

    return result


"""
In CrewAI we've 3 components 
1. Agents - Consider them as characters [Like Researcher agent or Analyst agent]
2. Tasks [imp] - What will the agent do ?
3. Tools - How will i approach a particular task ?
"""
