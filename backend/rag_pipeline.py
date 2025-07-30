from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Literal
import os

# Supported model providers
ModelProvider = Literal["openai", "anthropic", "google", "ollama"]

def get_llm(provider: ModelProvider, model_name: Optional[str] = None, api_key: Optional[str] = None):
    """
    Get an LLM instance based on the provider and configuration.
    
    Args:
        provider: The LLM provider to use
        model_name: Optional model name to use (if not provided, uses default)
        api_key: Optional API key (if not provided, uses environment variable)
    """
    if provider == "openai":
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        return ChatOpenAI(
            model_name=model_name or "gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
    elif provider == "anthropic":
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key is required")
        return ChatAnthropic(
            model_name=model_name or "claude-3-sonnet-20240229",
            temperature=0.7,
            api_key=api_key
        )
    elif provider == "google":
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google API key is required")
        return ChatGoogleGenerativeAI(
            model_name=model_name or "gemini-pro",
            temperature=0.7,
            google_api_key=api_key
        )
    elif provider == "ollama":
        return Ollama(model=model_name or "mistral")
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def ask_question(vectorstore, question: str, provider: ModelProvider = "ollama", 
                model_name: Optional[str] = None, api_key: Optional[str] = None):
    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(question, k=3)
    if not docs:
        return "No relevant information found."

    # Combine content
    context = "\n\n".join([doc.page_content for doc in docs])

    # Get the appropriate LLM
    llm = get_llm(provider, model_name, api_key)

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

def ask_session_question(vectorstore, question: str, provider: ModelProvider = "ollama",
                        model_name: Optional[str] = None, api_key: Optional[str] = None):
    return ask_question(vectorstore, question, provider, model_name, api_key)

