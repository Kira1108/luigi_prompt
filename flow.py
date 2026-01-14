from nodes import (
    greeting, 
    car_ownership, 
    drive_liscence_availability, 
    end_conversation_unqualified,
    end_conversation_flow_completed,
    colloquial_style_node
)

from base import ConversationFlow

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
        nodes=[greeting, car_ownership, drive_liscence_availability, end_conversation_unqualified, end_conversation_flow_completed],
        global_instructions="You are a financial assistant guiding customers through a series of questions."
    )
    
    return flow
    
if __name__ == "__main__":
    flow = create_flow_financial_assistant()
    instruction = flow.format()
    print(instruction)