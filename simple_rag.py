from agno.embedder.ollama import OllamaEmbedder
from agno.models.ollama import Ollama
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.pdf import PDFKnowledgeBase

embedder = OllamaEmbedder(id="mxbai-embed-large", dimensions=1024)
vector_db = LanceDb(
    table_name="iplt20",
    uri="/tmp/lancedb",
    search_type=SearchType.hybrid,
    embedder=embedder,
)
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://documents.iplt20.com/bcci/documents/1775736835406_TATA_IPL_2026_Match_Playing_Conditions.pdf"],
    vector_db=vector_db
)
#knowledge_base = PDFKnowledgeBase(
#    path="C://Users//Ashch//PycharmProjects//Langchain//fih-Rules-of-hockey-2026-final.pdf",
#    vector_db=vector_db
#)
#####################################
#knowledge_base.load(upsert=True)
######################################################

from agno.agent import Agent

agent = Agent(
    model=Ollama(id="gemma3:1b", options={"num_ctx": 16192}),
    # Enable RAG
    knowledge=knowledge_base,
    add_context=True,
    # Add references to the original documents
    add_references=True,
    description="You are an expert in the rules of the IPL T20 Cricket.",
    instructions=[
        "Use additional data provided for the corresponding rules.",
        "Cite the rules book with the corresponding information at the end of the answer to a question"
    ],
    search_knowledge=False,
    add_history_to_messages=True,
    num_history_responses=10,
    markdown=True,
    # debug_mode=True,

)


prompt = "Summarize Super over rule"
response = agent.run(prompt)
print(response.content)

