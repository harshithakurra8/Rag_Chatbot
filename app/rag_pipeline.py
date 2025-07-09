from app.document_handler import retrieve_relevant_chunks
from app.llm_wrapper import LLMWrapper

llm = LLMWrapper()

def answer_question(question: str) -> str:
    chunks = retrieve_relevant_chunks(question)
    if not chunks:
        return "Sorry, I couldn't find any relevant information in the documents."
    context = "\n".join(chunks)
    prompt = (
        f"Answer the question using ONLY the context below. "
        f"If the answer is not in the context, say 'I don't know.'\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return llm.generate(prompt)
