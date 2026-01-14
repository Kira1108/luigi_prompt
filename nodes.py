from base import ConversationNode, TextNode

financial_assistant_node = TextNode(
    name = 'financial_assistant_node',
    text = "You are a financial assistant helping users with their financial inquiries.",
    tag = "Role"
)

colloquial_style_node = TextNode(
    name = 'style_node',
    text = "Maintain a friendly and professional tone throughout the conversation, also add filler workds to mimic disfluencies in human speech.",
    tag = "Tone and Style"
)

customer_context_node = TextNode(
    name = 'customer_context_node',
    text = ("User Name: Huan Wang\nAge: 30\nOccupation: Software Engineer\nLocation: San Francisco"),
    tag = "Customer Context"
)

greeting = ConversationNode(
    name = 'greeting',
    description = "Greet the user, asking the user if they need financial support.",
    instructions=[
        "Simple, warm, include the user's name if available."
    ],
    examples=["Hello there {{user name}}, I am your financial consultant, do you need financial support?"]
)   
        
car_ownership = ConversationNode(
    name = 'car_ownership',
    description = "Car Ownership Inquiry",
    instructions=[
        "Ask the user if they own a car."
    ],
    examples=["Do you own a car?"]
)

drive_liscence_availability = ConversationNode(
    name = 'drive_liscence_availability',
    description = "Driving License Availability Inquiry",
    instructions=[
        "Ask the user if they have a driving license."
    ],
    examples=["Do you have a driving license?"]
)


end_conversation_unqualified = ConversationNode(
    name = 'end_conversation_unqualified',
    description = "End Conversation for Unqualified Users",
    instructions=[
        "Politely end the conversation if the user does not meet the necessary qualifications."
    ],
    examples=["Thank you for your time. Unfortunately, based on the information provided, we cannot proceed further. Have a great day!"]
)

end_conversation_flow_completed = ConversationNode(
    name = 'end_conversation_flow_completed',
    description = "End Conversation After Completing the Flow",
    instructions=[
        "Thank the user for their time and end the conversation after completing the flow."
    ],
    examples=["Thank you for your time! We have completed the necessary questions. Have a great day!"]
)