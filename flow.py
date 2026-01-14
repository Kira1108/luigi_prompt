from nodes import (
    greeting, 
    car_ownership, 
    drive_liscence_availability, 
    end_conversation_unqualified,
    end_conversation_flow_completed,
    colloquial_style_node,
    financial_assistant_node,
    customer_context_node,
    forbiddent_topics_node
)

from base import ConversationFlow, Composed

def create_flow_financial_assistant() -> ConversationFlow:
    
    greeting.transit_to(
        node=car_ownership,
        condition="User responds to greeting"
    )
        
    car_ownership.transit_to(
        node=drive_liscence_availability,
        condition="User indicates they own a car"
    )

    car_ownership.transit_to(
        node=end_conversation_unqualified,
        condition="User indicates they do not own a car"
    )
    
    drive_liscence_availability.transit_to(
        node=end_conversation_flow_completed,
        condition="User indicates they have a driving license"
    )
    
    drive_liscence_availability.transit_to(
        node=end_conversation_unqualified,
        condition="User indicates they do not have a driving license"
    )
    
    flow = ConversationFlow(
        nodes=[
            greeting, 
            car_ownership, 
            drive_liscence_availability, 
            end_conversation_unqualified, 
            end_conversation_flow_completed
        ],
    )
    
    flow = Composed(
        components=[
            financial_assistant_node,
            colloquial_style_node, 
            flow,
            forbiddent_topics_node,
            customer_context_node
            ],
        sep = '\n\n'
    )
    return flow
    
if __name__ == "__main__":
    flow = create_flow_financial_assistant()
    instruction = flow.format()
    print(instruction)