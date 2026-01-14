from dataclasses import dataclass, field

@dataclass
class Transition:
    condition: str
    target_node: 'ConversationNode'
    

NODE_INSTRUCTION_TEMPLATE = """
{{
  "id": {id},
  "description": {description},
  "instructions": {instructions},
  "examples": {examples},
  "transitions": {transitions}
}}
""".strip()

@dataclass
class ConversationNode:
    name:str
    description: str
    instructions: list[str]
    examples: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.id = self.name
        self.transitions: list[Transition] = []
        
    def add_id(self, id:str):
        self.id = f"{id}_{self.name}"
        
    def transit_to(self, node:"ConversationNode", condition:str):
        transition = Transition(condition=condition, target_node=node)
        self.transitions.append(transition)
        return self
        
    def format(self) -> str:
        transitions_formatted = [
            {
                "condition": t.condition,
                "target_node": t.target_node.id
            } for t in self.transitions
        ]
        return NODE_INSTRUCTION_TEMPLATE.format(
            id=self.id,
            description=self.description,
            instructions=self.instructions,
            examples=self.examples,
            transitions=transitions_formatted
        )
        
class ConversationFlow:
    def __init__(self, 
                 nodes: list[ConversationNode], 
                 global_instructions: str = "You are a helpful assistant that responds based on the conversation flow defined below."):
        self.global_instructions = global_instructions
        self.nodes = nodes
        for idx, node in enumerate(self.nodes):
            node.add_id(id=str(idx + 1))
        
    def format(self, **kwargs) -> str:
        flow_instruction = "\n\n".join([node.format() for node in self.nodes])
        flow_instruction = "\n<Conversation Flow Definition>\n" + flow_instruction + "\n</Conversation Flow Definition>\n"
        flow_instruction = self.global_instructions + "\n" + flow_instruction
        
        variables = [f"{k} = {v}" for k, v in kwargs.items()]
        if len(variables) == 0:
            return flow_instruction
        
        variables_instruction = "\n".join(variables)
        variables_instruction = f"<Conversation context>\n" + variables_instruction + "\n</Conversation context>\n"
        if variables_instruction:
            flow_instruction += "\n\n" + variables_instruction
        return flow_instruction
            
        
        
