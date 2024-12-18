import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Chatbot logic remains the same
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.2")  # Ensure the correct model name
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# GUI for Chatbot
class ChatbotGUI:
    def __init__(self, root):
        self.context = ""

        # Set up main window
        self.root = root
        self.root.title("Max the Chatbot")

        # Create a chat display area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entry box for user input
        self.input_box = tk.Entry(self.root, width=40)
        self.input_box.grid(row=1, column=0, padx=10, pady=10)

        # Button to send the message
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Bind Enter key to send message
        self.root.bind('<Return>', lambda event: self.send_message())

    def send_message(self):
        user_input = self.input_box.get()
        if not user_input:
            return
        # Display user input
        self.display_message(f"You: {user_input}")

        try:
            # Get chatbot response
            result = chain.invoke({"context": self.context, "question": user_input})
            self.display_message(f"Max: {result}")
            # Update conversation context
            self.context += f"\nUser: {user_input}\nMax: {result}"
        except Exception as e:
            self.display_message(f"Max: Sorry, I couldn't process that.\nError: {e}")

        # Clear input box after sending
        self.input_box.delete(0, tk.END)

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)  # Auto-scroll to the bottom


if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()
