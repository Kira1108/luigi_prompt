from base import ConversationNode, TextNode, ToolCallingNode

from nodes import (
    greeting, 
    colloquial_style_node,
    financial_assistant_node,
    customer_context_node,
    forbiddent_topics_node,
    dry_node, 
    flex_node, 
    language_node, 
)

from base import ConversationFlow, Composed


def create_yx_flow():
    greeting = ConversationNode(
        name = "greeting",
        description = "greet the user",
        instructions = [
            "include the customer's name in the greeting message, but do not include titles like ‘先生’ or '小姐', call his/her full name directly, in this node.",
            "You only call the full name in the opening greeting node, do not repeat full name in the following nodes.(use pronouns instead e.g. '您')"
        ],
        examples = ['您好，请问是... 吗？']
    )

    financial_support_inquiry = ConversationNode(
        name = "financial_support_inquiry",
        description = "ask if the user need financial support",
        instructions = [
            "Ask a yes/no question about financial support needs.",
            "You should include you self as `[clueSource]合作方易鑫集团....`, plug in the variable[clueSource] from context.",
            "Pass condition: user do not reject or refuse financial support.(呃， 啊， 嗯， 可以，好的， 你说)",
            "Fail condition: user explicitly reject or refuse financial support.（不需要，没兴趣，不不不，不想要）"
        ],
        examples = ['这边是[clueSource]合作方易鑫集团的金融专属顾问，我们收到了您申请的汽车金融方案，请问您是有资金需求吗？']
    )

    payment_strategy_inquiry = ConversationNode(
        name = "payment_strategy_inquiry",
        description = "inquire about the user's car payment strategy",
        instructions = [
            "Ask if the user bought the car with cash or financed it. If financed, ask whether it is currently paid off or if payments are still ongoing.",
            "Stay In the Node: If the user indicates the car is financed, follow up with a question about their current payment status.",
            "Go to next node: If the car is bought with cash or the financing is already paid off.",
            "Fail condition: User indicates that there is not a car under his/her name."
            ],
        examples = [
            "请问您名下的车是全款的还是按揭购买的？",
            "哦，是按揭的话， 现在已经还清了么，还是正在还款中？"
        ]
    )

    vehicle_registration_inquiry = ConversationNode(
        name = "vehicle_registration_inquiry",
        description = "inquire about the vehicle registration(green book) availability",
        instructions = [
            "Ask if the the vehicle registration (green book) is currently available.(在手里, not mortagaged and can be provided)",
            "Pass condition: user confirms the vehicle registration is available.",
            "Fail condition: user indicates the vehicle registration is not available or is mortgaged.",
            "Vehicle registration if also referred to as '绿本', ‘大本’ in Chinese."
        ],
        examples = [
            "那这辆车的绿本是在您手里吧？"
        ]
    )

    qualification_fail_node  = ConversationNode(
        name = 'qualification_fail_node',
        description = "The user does not meet the qualification criteria for a financial support.",
        instructions = [
            "Reclaim the question(where the user fails the qualification), make sure the user's unqualification is clear.",
            "If the previous unqualification reason is an asr error or the user seems confused, go back to the previous node and continue the conversation flow."
            "If the user fails the qualification again, politely end the conversation."
        ],
        examples = [
            "Agent:请问您按揭现在换完了吗？User：没有; Agent(reclaim and rephrase): 哦，您是说正在还款中，对吧？",
            "那不好意思打扰您了，祝您生活愉快， 再见。"
        ]
    )

    handoff_wechat_collector = ToolCallingNode(
        name = 'AgentHandoff Node',
        tool_name= 'transfer_to_wechat_account_collector',
        trigger_prompt = "Call the tool to transfer the qualified lead to a WeChat Account Collection Agent for further processing.",
    )


    greeting.transit_to(
        node=financial_support_inquiry,
        condition="User responds to greeting"
    )
    greeting.transit_to(
        node=qualification_fail_node,
        condition="Use explicitly indicates a wrong number or false name.")


    financial_support_inquiry.transit_to(
        node = payment_strategy_inquiry,
        condition = "User indicates they need financial support."
    )


    financial_support_inquiry.transit_to(
        node = qualification_fail_node,
        condition = "User explicitly rejects or refuses financial support."
    )

    payment_strategy_inquiry.transit_to(
        node= vehicle_registration_inquiry,
        condition="User indicates the car is bought with cash or financing is already paid off."
    )

    payment_strategy_inquiry.transit_to(
        node= qualification_fail_node,
        condition="User indicates there is no car under his/her name or the car is still being financed."
    )

    vehicle_registration_inquiry.transit_to(
        node= handoff_wechat_collector,
        condition="User confirms the vehicle registration is available."
    )

    vehicle_registration_inquiry.transit_to(
        node= qualification_fail_node,
        condition="User indicates the vehicle registration is not available or is mortgaged."
    )

    flow = ConversationFlow(
        nodes=[
            greeting,
            financial_support_inquiry,
            payment_strategy_inquiry,
            vehicle_registration_inquiry,
            qualification_fail_node,
            handoff_wechat_collector,
            flex_node
        ],
    )

    flow = Composed(
    components=[
        financial_assistant_node,
        colloquial_style_node, 
        dry_node,
        flow,
        forbiddent_topics_node,
        language_node,
        customer_context_node
        ],
    sep = '\n\n'
    )
    
    return flow


if __name__ == "__main__":
    flow = create_yx_flow()
    with open("yx_financial_assistant_flow.md", "w", encoding="utf-8") as f:
        f.write("```json\n" + flow.format() + "\n```")


