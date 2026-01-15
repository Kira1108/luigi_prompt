from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class Composable(ABC):
    
    @abstractmethod
    def format(self) -> str:
        ...
          
class Composed(Composable):
    def __init__(self, components: list[Composable], sep = "\n\n"):
        self.components = components
        self.sep = sep
        
        for c in components:
            if not isinstance(c, Composable):
                raise ValueError("All components in Composed must implement the Composable interface")
        
    def format(self) -> str:
        return self.sep.join([component.format() for component in self.components])
    
@dataclass
class Transition:
    condition: str
    target_node: 'BaseNode'
    
    def __post_init__(self):
        if not isinstance(self.target_node, BaseNode):
            print(type(self.target_node))
            print(self.target_node)
            raise ValueError("target_node must be an instance of ConversationNode")
    

class BaseNode(Composable):
    
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
    
    def __init__(self, name, text:str, tag = None):
        self.text = text
        self.tag = tag
        super().__init__(name=name)
        
    def format(self) -> str:
        instruction = TEXT_NODE_INSTRUCTION_TEMPLATE.format(
            instructions=self.text
        )
        
        if self.tag:
            instruction = f"<{self.tag}>\n" + instruction + f"\n</{self.tag}>"
        return instruction
    
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

TOOL_NODE_INSTRUCTION_TEMPLATE = """
{{
    
    "id": {id},
    "description": "In this step, you are expected to call a tool, you MUST call the tool specified below. the tool parameters should inferred from the conversation context.",
    "tool_name": `{tool_name}`,
    "trigger": {trigger_prompt},
    "examples": {examples}
}}
""".strip()

class ToolCallingNode(BaseNode):
    def __init__(self,
        name:str,
        tool_name: str,
        trigger_prompt: list[str],
        examples: list[str] = None
    ):
        self.tool_name = tool_name
        self.trigger_prompt = trigger_prompt
        self.examples = examples if examples is not None else []
        super().__init__(name=name)

        
    def format(self):
        return TOOL_NODE_INSTRUCTION_TEMPLATE.format(
            id=self.id,
            tool_name=self.tool_name,
            trigger_prompt=self.trigger_prompt,
            examples=self.examples
        )
        

        
class ConversationFlow(Composable):
    def __init__(self, 
                 nodes: list[ConversationNode], 
                 global_instructions: str = None):
        self.global_instructions = global_instructions
        self.nodes = nodes
        for idx, node in enumerate(self.nodes):
            
            if not isinstance(node, ConversationNode) and not isinstance(node, ToolCallingNode):
                raise ValueError("All nodes in ConversationFlow must be of type ConversationNode")
            
            node.add_id(id=str(idx + 1))
        
    def format(self) -> str:
        flow_instruction = "\n\n".join([node.format() for node in self.nodes])
        flow_instruction = "<Conversation Flow Definition>\n" + flow_instruction + "\n</Conversation Flow Definition>"
        
        if self.global_instructions:
            flow_instruction = self.global_instructions + "\n" + flow_instruction 
        return flow_instruction
            
        
        
