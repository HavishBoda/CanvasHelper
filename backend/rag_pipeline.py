from langchain_community.llms import Ollama

def ask_question(vectorstore, question):
    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(question, k=3)
    if not docs:
        return "No relevant information found."

    # Combine content
    context = "\n\n".join([doc.page_content for doc in docs])

    # Set up Ollama LLM
    llm = Ollama(model="mistral")  # or "llama2", "gemma", etc.

    # Construct the prompt
    prompt = f"""
    Use the following lecture content to answer the question:

    {context}

    Question: {question}
    Answer:
    """

    # Generate the answer
    response = llm.invoke(prompt)
    return response

def ask_session_question(vectorstore, question):
    return ask_question(vectorstore, question)

