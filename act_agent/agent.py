# import asyncio
# import logging
# import os
# from azure.ai.projects import AIProjectClient
# from azure.identity import DefaultAzureCredential
# from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
# from dotenv import load_dotenv
#
# from .user_functions import user_functions
#
# logging.basicConfig(level=logging.INFO, )
# logger = logging.getLogger(__name__)
#
# load_dotenv()
#
async def invoke_act_agent(prompt: str) -> str:
    return "disabled for now"
#     project_client = AIProjectClient.from_connection_string(
#         credential=DefaultAzureCredential(),
#         conn_str=os.environ["PROJECT_CONNECTION_STRING"],
#     )
#
#     with project_client:
#         # Initialize agent toolset with user functions and code interpreter
#         # [START create_agent_toolset]
#         functions = FunctionTool(user_functions)
#         code_interpreter = CodeInterpreterTool()
#
#         toolset = ToolSet()
#         toolset.add(functions)
#         toolset.add(code_interpreter)
#
#         # To enable tool calls executed automatically
#         project_client.agents.enable_auto_function_calls(toolset=toolset)
#
#         agent = project_client.agents.create_agent(
#             model=os.environ["MODEL_DEPLOYMENT_NAME"],
#             name="my-assistant",
#             instructions="You are a web server. Do not use markdown for formatting. "
#                          "Do exactly what the user asks. Do not use markdown in your response. "
#                          "You are not talking to an actual user. You will try to use a tool in your tool set to do what the user is asking"
#                          "Produce minimal output, but include files modified or other potentially useful details coming from tool output.",
#             toolset=toolset,
#         )
#         # [END create_agent_toolset]
#         logger.info(f"Created agent, ID: {agent.id}")
#
#         # Create thread for communication
#         thread = project_client.agents.create_thread()
#         logger.info(f"Created thread, ID: {thread.id}")
#
#         # Create message to thread
#         message = project_client.agents.create_message(
#             thread_id=thread.id,
#             role="user",
#             content=prompt,
#         )
#         logger.info(f"Created message, ID: {message.id}")
#
#         # Create and process agent run in thread with tools
#         run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
#
#         logger.info(f"Run finished with status: {run.status}")
#
#         if run.status == "failed":
#             logger.info(f"Run failed: {run.last_error}")
#
#         # Delete the assistant when done
#         project_client.agents.delete_agent(agent.id)
#         logger.info("Deleted agent")
#
#         # Fetch and log all messages
#         messages = project_client.agents.list_messages(thread_id=thread.id)
#         logger.info(f"Messages: {messages}")
#         return messages.data[0].content[0].text.value
#
# if __name__ == "__main__":
#     result = asyncio.run(invoke_act_agent("Save the following data: {\"name\": \"John\", \"age\": 30}"))
#     print(result)