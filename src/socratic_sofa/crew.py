from collections.abc import Callable

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class SocraticSofa:
    """SocraticSofa crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Optional callback for streaming task completions
    task_callback: Callable | None = None

    @agent
    def socratic_questioner(self) -> Agent:
        return Agent(
            config=self.agents_config["socratic_questioner"],
            verbose=True,  # type: ignore[index]
        )

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config["judge"], verbose=True)  # type: ignore[index]

    @task
    def propose_topic(self) -> Task:
        return Task(config=self.tasks_config["propose_topic"], callback=self.task_callback)

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config["propose"],
            callback=self.task_callback,  # type: ignore[index]
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config["oppose"],
            callback=self.task_callback,  # type: ignore[index]
        )

    @task
    def judge_task(self) -> Task:
        return Task(
            config=self.tasks_config["judge_task"],  # type: ignore[index]
            callback=self.task_callback,
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
