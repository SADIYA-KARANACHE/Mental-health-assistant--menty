import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Directly set your Groq API key here
api_key = "YOUR_API_KEY"  

def main():
    st.title("Mental Health Support Chatbot")
    st.write("I'm here to provide mental health awareness and support. How can I help you today?")

    # Session state to store chat history and feedback history
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'feedback' not in st.session_state:
        st.session_state['feedback'] = []

    # User input box
    user_input = st.text_input("You: ", "")

    # Initialize memory for the conversation
    memory = ConversationBufferWindowMemory(k=5)  # Keep the last 5 messages

    # Initialize Groq Langchain chat object
    groq_chat = ChatGroq(groq_api_key=api_key, model_name='mixtral-8x7b-32768')  

    # Initialize conversation
    conversation = ConversationChain(llm=groq_chat, memory=memory)

    # Process user input
    if user_input:
        # Append user input to chat history
        st.session_state['history'].append(f"You: {user_input}")

        # Call the Groq API
        response = conversation(user_input)

        # Append chatbot response to chat history
        st.session_state['history'].append(f"Bot: {response['response']}")

        # Display feedback prompt after chatbot response
        feedback = st.text_input("How did you feel about this response? Provide your feedback: ", key=len(st.session_state['feedback']))

        # Store feedback
        if feedback:
            st.session_state['feedback'].append(f"Feedback: {feedback}")
            st.write(f"Thank you for your feedback: {feedback}")

    # Display chat history
    st.write("Chat History:")
    for message in st.session_state['history']:
        st.write(message)
        
    # Optionally display feedback history
    st.write("Feedback History:")
    for fb in st.session_state['feedback']:
        st.write(fb)

if __name__ == "__main__":
    main()
