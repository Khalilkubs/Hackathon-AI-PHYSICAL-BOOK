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

    # Add author information
    st.markdown("**Author: Khalil ur rehman**")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "run_script" not in st.session_state:
        st.session_state.run_script = 0  # Counter to trigger script execution

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

        st.header("Author Information")
        st.markdown("""
        **Khalil ur rehman**
        """)

    # Create a container for the chat messages
    with st.container():
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the book..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Increment counter to trigger script execution
        st.session_state.run_script += 1
        st.rerun()

    # Process the last message if it's from the user and we haven't processed it yet
    if (st.session_state.messages and
        st.session_state.messages[-1]["role"] == "user" and
        (len(st.session_state.messages) == 1 or st.session_state.messages[-2]["role"] != "assistant")):

        user_prompt = st.session_state.messages[-1]["content"]

        # Display assistant response
        with st.chat_message("assistant"):
            rag_system = get_rag_system()

            with st.spinner("Searching for relevant content in the book..."):
                try:
                    response = rag_system.query(user_prompt)
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"

            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Increment counter to trigger script execution
        st.session_state.run_script += 1
        st.rerun()

    # Auto-scroll to bottom using JavaScript
    # This script runs after each interaction to scroll to the bottom
    scroll_script = f"""
    <script>
    // Function to scroll to bottom of chat container
    function scrollToBottom() {{
        // Get all scrollable containers
        var containers = window.parent.document.querySelectorAll('div[data-testid="stVerticalBlock"]');
        for (var i = 0; i < containers.length; i++) {{
            if (containers[i].scrollHeight > containers[i].clientHeight) {{
                containers[i].scrollTop = containers[i].scrollHeight;
                break;
            }}
        }}

        // Also scroll main page to bottom if needed
        window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);
    }}

    // Run immediately
    scrollToBottom();

    // Run again after a short delay to ensure content is fully rendered
    setTimeout(scrollToBottom, 100);
    </script>
    """

    st.markdown(scroll_script, unsafe_allow_html=True)

if __name__ == "__main__":
    main()