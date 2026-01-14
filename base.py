from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class Transition:
    condition: str
    target_node: 'ConversationNode'
    

class BaseNode(ABC):
    
    def __init__(self, name:str):
        self.transitions: list[Transition] = []
        self.name = name
        self.id = self.name
        
    def add_id(self, id:str):
        self.id = f"{id}_{self.name}"
        
    @abstractmethod
    def format(self) -> str:
        ...
        
    def transit_to(self, node:"BaseNode", condition:str):
        if not hasattr(self, 'transitions'):
            self.transitions = []
        
        transition = Transition(condition=condition, target_node=node)
        self.transitions.append(transition)
        return self
    
TEXT_NODE_INSTRUCTION_TEMPLATE = """
{instructions}
""".strip()
    
class TextNode(BaseNode):
    
    def __init__(self, name, text:str):
        self.text = text
        super().__init__(name=name)
        
    def format(self) -> str:
        return TEXT_NODE_INSTRUCTION_TEMPLATE.format(
            instructions=self.text
        )
    
CONVERSATION_NODE_INSTRUCTION_TEMPLATE = """
{{
  "id": {id},
  "description": {description},
  "instructions": {instructions},
  "examples": {examples},
  "transitions": {transitions}
}}
""".strip()

class ConversationNode(BaseNode):
    
    def __init__(self,
        name:str,
        description: str,
        instructions: list[str],
        examples: list[str] = None
    ):
        self.description = description
        self.instructions = instructions
        self.examples = examples if examples is not None else []
        super().__init__(name=name)
        
    def format(self) -> str:
        transitions_formatted = [
            {
                "condition": t.condition,
                "target_node": t.target_node.id
            } for t in self.transitions
        ]
        return CONVERSATION_NODE_INSTRUCTION_TEMPLATE.format(
            id=self.id,
            description=self.description,
            instructions=self.instructions,
            examples=self.examples,
            transitions=transitions_formatted
        )
        
class ConversationFlow:
    def __init__(self, 
                 nodes: list[ConversationNode], 
                 global_instructions: str = None):
        self.global_instructions = global_instructions
        self.nodes = nodes
        for idx, node in enumerate(self.nodes):
            node.add_id(id=str(idx + 1))
        
    def format(self) -> str:
        flow_instruction = "\n\n".join([node.format() for node in self.nodes])
        flow_instruction = "\n<Conversation Flow Definition>\n" + flow_instruction + "\n</Conversation Flow Definition>\n"
        
        if self.global_instructions:
            flow_instruction = self.global_instructions + "\n" + flow_instruction 
        return flow_instruction
            
        
        
