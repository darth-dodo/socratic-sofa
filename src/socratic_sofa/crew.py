from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Callable, Optional

@CrewBase
class SocraticSofa():
    """SocraticSofa crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Optional callback for streaming task completions
    task_callback: Optional[Callable] = None

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

    @task
    def propose_topic(self) -> Task:
        return Task(
            config=self.tasks_config['propose_topic'],
            callback=self.task_callback
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'], # type: ignore[index]
            callback=self.task_callback
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'], # type: ignore[index]
            callback=self.task_callback
        )

    @task
    def judge_task(self) -> Task:
        return Task(
            config=self.tasks_config['judge_task'], # type: ignore[index]
            callback=self.task_callback
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
