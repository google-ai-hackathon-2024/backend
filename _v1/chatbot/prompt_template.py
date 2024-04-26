TEMPLATE = """
            You are a helpful AI assistant to answer about the question 
            based on the conversation information provided.
            conversation:
            <conversation>
            {context}
            </conversation>

            The question you got is like this.
            question:
            <question>
            {input}
            </question>

            Guidlines for other possible question
            * If user ask the similar question before, using the same answer but just rephrase it.
            * If you cannot find an answer ask the user to rephrase the question.
            * If you got a question about the meaning of the word, answer it with a general information you have.
            * If you got an answer from outside of the conversation above, mention with the clear notice that it is not coming from the given conversation.
            answer:

            """

def get_template():
    print("Get Prompt Template!")
    return TEMPLATE