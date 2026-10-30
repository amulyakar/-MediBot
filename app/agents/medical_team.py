
from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team
from agno.team.mode import TeamMode

from app.config import GROQ_MODEL
from app.agents.tools import search_medical_library


# Shared AI model configuration
model = Groq(id=GROQ_MODEL)


# AGENT 1: Medical Query Analyzer
medical_query_analyzer = Agent(
    name="Medical Query Analyzer",

    role="Understand and classify the user's medical information question.",

    model=model,

    instructions=[
        "Understand the user's question carefully.",
        "Identify the main medical topic and important details.",
        "Clarify ambiguous questions when necessary.",
        "Do not diagnose diseases or prescribe medicines.",
        "Pass a clear understanding of the question to the research stage."
    ]
)


# AGENT 2: Medical Research Agent
medical_research_agent = Agent(
    name="Medical Research Agent",

    role="Find relevant information from the local medical reference library.",

    model=model,

    tools=[search_medical_library],

instructions=[
    "Search the medical reference library using the user's question.",
    "Call search_medical_library only once per question.",
    "Do not repeat searches if relevant documents are found.",
    "Use only information returned by the search tool.",
    "Include the document title, source and reference URL.",
    "Clearly state when information is unavailable.",
    "Never diagnose or prescribe treatment."
]
)


# AGENT 3: Medical Answer Reviewer
medical_answer_reviewer = Agent(
    name="Medical Answer Reviewer",

    role="Review medical answers for accuracy, clarity and safety.",

    model=model,

instructions=[
    "Review the research findings before producing the final answer.",
    "Use only facts explicitly supported by the research documents.",
    "Do not add medical facts from your general knowledge.",
    "Remove every claim that cannot be supported by a retrieved document.",
    "Check that the answer is clear, accurate and easy to understand.",
    "Never diagnose diseases or prescribe medicines.",
    "Mention when professional medical advice is necessary.",
    "Include the educational medical disclaimer.",
    "If the research is insufficient, clearly state that limitation."
]
)


# COORDINATING TEAM
medical_team = Team(
    name="MediBot Medical Assistant",

    mode=TeamMode.coordinate,

    model=model,

    members=[
        medical_query_analyzer,
        medical_research_agent,
        medical_answer_reviewer
    ],

    instructions=[
        "You coordinate three specialist medical information agents.",
        "First, ask the Medical Query Analyzer to understand the question.",
        "Next, ask the Medical Research Agent to retrieve relevant evidence.",
        "Finally, ask the Medical Answer Reviewer to review the findings.",
        "Combine their contributions into one clear and understandable answer.",
        "Use only information supported by the retrieved reference material.",
        "If the reference library has insufficient information, say so clearly.",
        "Never diagnose a user or prescribe medication.",
        "For emergencies, advise the user to contact local emergency services.",
        "Always include this disclaimer:",
        "MediBot provides educational information only and is not a "
        "substitute for professional medical advice."
    ],

    markdown=True,

    show_members_responses=True
)

