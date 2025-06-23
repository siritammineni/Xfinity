# agent_graph.py

from langgraph.graph import StateGraph, END
from agents.extraction_agent import ExtractionAgent
from agents.transformation_agent import TransformationAgent
from agents.loading_agent import LoadingAgent
from agents.job_agent import JobAgent
from agents.pseudocode_agent import PseudocodeAgent

def build_conversion_graph():
    # Shared input schema
    class ScriptState(dict):
        bods_script: str
        xml_code: str
        pseudocode: str
        extraction_result: str
        transformation_result: str
        loading_result: str
        job_result: str
        target: str

    # Initialize all agents
    extraction_agent = ExtractionAgent()
    transformation_agent = TransformationAgent()
    loading_agent = LoadingAgent()
    job_agent = JobAgent()
    pseudocode_agent = PseudocodeAgent()

    def run_pseudocode_agent(state: ScriptState) -> ScriptState:
        print("Entered Pseudocode Agent")
        xml_code = state["xml_code"]
        if xml_code:
            pseudocode = pseudocode_agent.run(xml_code)
            state["pseudocode"] = pseudocode
        return state


    # Node functions
    def run_extraction_agent(state: ScriptState) -> ScriptState:
        print("Entered Extraction Agent")
        bods_script = state["bods_script"]
        target = state["target"]
        if not bods_script:
            raise ValueError("Missing 'bods_script' in state")
        extraction_result = extraction_agent.run(bods_script,target)
        state["extraction_result"] = extraction_result
        return state

    def run_transformation_agent(state: ScriptState) -> ScriptState:
        print("Entered Transformation Agent")
        bods_script = state["bods_script"]
        target = state["target"]
        if not bods_script:
            raise ValueError("Missing 'bods_script' in state")
        transformation_result = transformation_agent.run(bods_script,target)
        state["transformation_result"] = transformation_result
        return state

    def run_loading_agent(state: ScriptState) -> ScriptState:
        print("Entered Loading Agent")
        bods_script = state["bods_script"]
        target = state["target"]
        if not bods_script:
            raise ValueError("Missing 'bods_script' in state")
        loading_result = loading_agent.run(bods_script,target)
        state["loading_result"] = loading_result
        return state

    def run_job_agent(state: ScriptState) -> ScriptState:
        print("Entered Job Agent")
        bods_script = state["bods_script"]
        target = state["target"]
        if not bods_script:
            raise ValueError("Missing 'bods_script' in state")
        job_result = job_agent.run(bods_script,target)
        state["job_result"] = job_result
        return state
    
    def entry_router(state: ScriptState):
        if state.get("xml_code"):
            return "Pseudocode"
        else:
            return "Extraction"
    
    workflow = StateGraph(ScriptState)


    # Add nodes (agents)
    workflow.add_node("Extraction", run_extraction_agent)
    workflow.add_node("Transformation", run_transformation_agent)
    workflow.add_node("Loading", run_loading_agent)
    workflow.add_node("Job", run_job_agent)
    workflow.add_node("Pseudocode", run_pseudocode_agent)

    # Define flow between agents
    workflow.set_entry_point(entry_router)
    workflow.add_edge("Pseudocode", "Extraction")
    workflow.add_edge("Extraction", "Transformation")
    workflow.add_edge("Transformation", "Loading")
    workflow.add_edge("Loading", "Job")
    workflow.add_edge("Job", END)

    app = workflow.compile()
    return app
