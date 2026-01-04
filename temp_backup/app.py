import streamlit as st
import os
from retrieve import RAGSystem

# Set page config
st.set_page_config(
    page_title="Physical AI & Humanoid Robotics Book - RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    return RAGSystem()

def main():
    st.title("🤖 Physical AI & Humanoid Robotics Book Assistant")
    st.markdown("Ask questions about the Physical AI & Humanoid Robotics book content")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for additional info
    with st.sidebar:
        st.header("About this Assistant")
        st.markdown("""
        This chatbot can answer questions about:
        - ROS 2 fundamentals
        - Computer vision for robotics
        - Vision-Language-Action models
        - Physical AI concepts
        - Humanoid robotics principles
        - And other topics from the book
        """)

        st.header("How it works")
        st.markdown("""
        1. Your question is embedded using Cohere
        2. Similar content is retrieved from the book using Qdrant
        3. A response is generated based on the retrieved content
        """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the book..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            rag_system = get_rag_system()

            with st.spinner("Searching for relevant content in the book..."):
                try:
                    response = rag_system.query(prompt)
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"

            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()