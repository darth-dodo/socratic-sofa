from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class SocraticSofa():
    """SocraticSofa crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def socratic_questioner(self) -> Agent:
        return Agent(
            config=self.agents_config['socratic_questioner'], # type: ignore[index]
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def propose_topic(self) -> Task:
        return Task(
            config=self.tasks_config['propose_topic'],
            output_file='outputs/01_topic.md'
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'], # type: ignore[index]
            output_file='outputs/02_proposition.md'
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'], # type: ignore[index]
            output_file='outputs/03_opposition.md'
        )
    
    @task
    def judge_task(self) -> Task:
        return Task(
            config=self.tasks_config['judge_task'], # type: ignore[index]
            output_file='outputs/04_judgment.md'
        )
    @crew
    def crew(self) -> Crew:
        """Creates the SocraticSofa crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
