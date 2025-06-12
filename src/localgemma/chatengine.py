from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_ollama import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import sys

# Initialize models
llm = Ollama(model="gemma3:4b")
embedding_model = OllamaEmbeddings(model="bge-m3:567m")

# Load PDF and build vector store
def load_documents(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embedding_model)
    return vectorstore.as_retriever()

# Prompt template
QA_TEMPLATE = """
Answer the question based only on the context provided.

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(QA_TEMPLATE)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_chain(retriever):
    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_qa.py <path_to_pdf>")
        sys.exit(1)

    retriever = load_documents(sys.argv[1])
    chain = build_chain(retriever)

    while True:
        question = input("What do you want to learn from the document?\n")
        print("\nAnswer:\n")
        print(chain.invoke(question))
        print()

if __name__ == "__main__":
    main()

