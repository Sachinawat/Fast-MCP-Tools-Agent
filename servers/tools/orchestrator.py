import json
import os
from servers.config import logger
from servers.tools import research_rag, math_science, analytics
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class AgentOrchestrator:
    def __init__(self):
        # Initialize the planner LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        else:
            self.llm = None

    def _planner_llm(self, query: str):
        """
        Uses GPT-4o-mini to decide which tools to call.
        """
        if not self.llm:
            return [{"tool": "research_agent", "args": {"query": query}}]

        system_prompt = """
        You are a Routing Agent. Available Tools:
        1. research_agent(query): General knowledge.
        2. math_agent(expression): Math calc.
        3. audit_tool(action='view'): Logs.
        4. finance_agent(ticker): Get stock prices (e.g., 'AAPL'). <--- ADD THIS

        Return a JSON array of steps. Example:
        User: "Research Apple and check its price" 
        -> [
             {"tool": "research_agent", "args": {"query": "Apple company info"}},
             {"tool": "finance_agent", "args": {"ticker": "AAPL"}}
           ]
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", query)
        ])
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({})
            content = result.content.strip()
            
            # Clean up potential markdown code blocks from LLM
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"Planning Error: {e}")
            # Fallback
            return [{"tool": "research_agent", "args": {"query": query}}]

    def execute_workflow(self, user_query: str, session_id: str) -> str:
        logger.info(f"Orchestrator received: {user_query}")
        
        # 1. Plan
        plan = self._planner_llm(user_query)
        final_response = ""

        # 2. Execute
        for step in plan:
            tool = step.get('tool')
            args = step.get('args')
            
            if tool == "research_agent":
                res = research_rag.execute_research(args.get('query'))
                final_response += str(res.get('data', ''))
            
            elif tool == "math_agent":
                res = math_science.execute_math(args.get('expression'))
                final_response += f"\nCalculation Result: {res.get('result')}"
            
            elif tool == "audit_tool":
                res = analytics.get_logs()
                final_response += f"\nLogs found: {len(res)}"

        return final_response

manager = AgentOrchestrator()