import json
from typing import Optional

import boto3
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("example@demo.com", "demo_password"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("history", "")


@cl.on_message
async def main(message: cl.Message):
    try:
        kb = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

        chat_history = cl.user_session.get("history")
        prompt = f"""# ユーザの入力
{message.content}

# ここまでの会話履歴
{chat_history}
"""
        params = {
            "input": {"text": prompt},
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "[YOUR_KNOWLEDGEBASE_ID",
                    "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {"numberOfResults": 20},
                    },
                },
            },
        }

        response = kb.retrieve_and_generate(**params)

        citations = response["citations"]
        answers = []
        text_elements = []

        source_index = 1
        for citation_idx, citation in enumerate(citations):
            answer = citation["generatedResponsePart"]["textResponsePart"]["text"]
            for ref_idx, reference in enumerate(citation["retrievedReferences"]):
                content_text = reference["content"]["text"]
                url = reference["location"]["s3Location"]["uri"]
                source_name = f"[{source_index}]"
                source_index += 1
                text_elements.append(
                    cl.Text(
                        content=f"Content: {content_text}\n\nSource URL: {url}",
                        name=source_name,
                        display="side",
                    )
                )
                answer += f"\n{source_name}"
            answers.append(answer)

        answers = "\n".join(answers)
        await cl.Message(content=answers, elements=text_elements).send()
        chat_history += (
            f"\nHuman: {message.content} \nBot: {response['output']['text']}"
        )
    except Exception as e:
        await cl.Message(
            content=f"Error: {e}",
        ).send()
    finally:
        cl.user_session.set("history", chat_history)
