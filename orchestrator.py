from typing import Dict, List
from typing_extensions import TypedDict
from agents.message_handling_agent import analyze_message  
from agents.query_handling_agent import handle_query
from agents.complaint_handling_agent import handle_complaint
import traceback  
from langgraph.graph import StateGraph
 
class OrchestratorState(TypedDict):
   user_message: str
   sentiment: str
   category: str
   response: str
   buttons: List[Dict[str, str]]
   needs_confirmation: bool
   harmful_content: str
   contains_sensitive_info: str
   xfinity_related: str
 
def handle_confirmation(state: OrchestratorState) -> Dict[str, str]:
   print("[INFO] Handling Confirmation...")
   user_response = state["user_message"].strip().lower()
   if "yes" in user_response:
       return {
           **state,
           "response": "I'm so glad that I could help! Let me know if you have more queries.",
           "buttons": [],
           "needs_confirmation": False  
       }
   elif "no" in user_response:
       return {
           **state,
           "response": "I’m sorry I couldn’t fully clarify your question. Would you like to rephrase it or speak to an agent?",
           "buttons": [
               {"label": "Chat with Agent", "action": "chat_agent"},
               {"label": "Call the Agent", "action": "call_agent"}
           ],
           "needs_confirmation": False  
       }
   else:
       return {
           **state,
           "response": "Please enter Yes or No.",
           "buttons": [],
           "needs_confirmation": True
       }
 
def classify_message(state: OrchestratorState) -> OrchestratorState:
   try:
       if state["needs_confirmation"]:
           print("[INFO] Skipping classification, going to confirmation.")
           return state  
       print("[INFO] Classifying message...")
       classification = analyze_message({"user_message": state["user_message"]})
       print(f"[INFO] Classification Result: {classification}")
       return {
           **state,
           "sentiment": classification["sentiment"],
           "category": classification["query_type"],
           "xfinity_related": classification["xfinity_related"],
           "harmful_content": classification["harmful_content"],
           "contains_sensitive_info": classification["contains_sensitive_info"],
           "needs_confirmation": False
       }
   except Exception as e:
       print("[ERROR] Classification failed:", str(e))
       traceback.print_exc()
       return {
           **state,
           "sentiment": "Neutral",
           "category": "General Query",
           "xfinity_related": "No",
           "harmful_content": "No",
           "contains_sensitive_info": "No",
           "needs_confirmation": False
       }
def handle_query_agent(state: OrchestratorState) -> Dict[str, str]:
   print("[INFO] Handling General Query...")
   if state["xfinity_related"] == "No":
       return {
           **state,
           "response": "I think this query might be out of context. Please ask a query related to Xfinity.",
           "buttons": [],
           "needs_confirmation": False
       }
   query_result = handle_query({"user_message": state["user_message"]})
 
   return {
       **state,
       "response": query_result["response"],
       "buttons": query_result.get("buttons", []),
       "needs_confirmation": False
}
def guardrails(state: OrchestratorState) -> Dict[str, str]:
   print("[INFO] Checking Guardrails...")
   if state["harmful_content"] == "Yes":
       return {
           **state,
           "response": "We are unable to process this request as it contains unsafe content.",
           "buttons": [],
           "needs_confirmation": False
       }
   if state["contains_sensitive_info"] == "Yes":
       return {
           **state,
           "response": "For security reasons, we cannot process sensitive personal data.",
           "buttons": [],
           "needs_confirmation": False
       }
   return state  
 
def handle_feedback(state: OrchestratorState) -> Dict[str, str]:
   print("[INFO] Handling Feedback...")
   return {
       **state,
       "response": "Thank you for your feedback! We appreciate your input.",
       "buttons": [],
       "needs_confirmation": False
   }
def ask_user(state: OrchestratorState) -> Dict[str, str]:
   print("[INFO] Asking user for clarification...")
   return {
       **state,
       "response": "I'm not sure how to assist you with that. Can you provide more details?",
       "buttons": [{"label": "Clarify Request", "action": "clarify_request"}],
       "needs_confirmation": False
   }
 
def decide_next_step(state: OrchestratorState) -> str:
   if state["needs_confirmation"]:
       return "handle_confirmation"
   if state["harmful_content"] == "Yes" or state["contains_sensitive_info"] == "Yes":
       return "guardrails"
   if state["category"] == "General Query":
       return "handle_query_agent"
   if state["category"] == "Complaint":
       return "handle_complaint"
   if state["category"] == "Feedback":
       return "handle_feedback"
   return "ask_user"  
 
 
 
graph = StateGraph(OrchestratorState)
 
graph.add_node("classify_message", classify_message)
graph.add_node("handle_query_agent", handle_query_agent)
graph.add_node("handle_complaint", handle_complaint)
graph.add_node("handle_feedback", handle_feedback)
graph.add_node("handle_confirmation", handle_confirmation)
graph.add_node("guardrails", guardrails)
graph.add_node("ask_user", ask_user)
 
graph.set_entry_point("classify_message")
 
graph.add_conditional_edges("classify_message", decide_next_step)
graph.set_finish_point("handle_query_agent")
graph.set_finish_point("handle_complaint")
graph.set_finish_point("handle_feedback")
graph.set_finish_point("handle_confirmation")
graph.set_finish_point("guardrails")
graph.set_finish_point("ask_user")
 
 
orchestrator_agent = graph.compile()
 