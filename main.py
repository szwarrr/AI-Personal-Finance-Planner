from textwrap import dedent
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
import streamlit as st
from agno.models.anthropic import Claude
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Personal Finance Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">💰 AI Personal Finance Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create personalized budgets, investment plans, and savings strategies powered by Claude Sonnet 4</p>', unsafe_allow_html=True)

# Sidebar for API Keys and Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Keys Section
    with st.expander("🔑 API Keys", expanded=True):
        anthropic_api_key = st.text_input(
            "Anthropic API Key (Claude)",
            type="password",
            help="Enter your Anthropic API key to access Claude Sonnet 4"
        )
        serp_api_key = st.text_input(
            "SerpAPI Key",
            type="password",
            help="Enter your SerpAPI key for web search functionality"
        )
        
        st.info("""
        **How to get Claude API Key:**
        1. Visit [console.anthropic.com](https://console.anthropic.com)
        2. Sign up or log in
        3. Go to API Keys
        4. Create a new key
        """)
    
    # Settings Section
    with st.expander("🎛️ Advanced Settings"):
        enable_research = st.checkbox("Enable Web Research", value=True, help="Use web search for current financial information")
        save_history = st.checkbox("Save Plan History", value=True, help="Save your generated plans for future reference")
        detail_level = st.select_slider(
            "Plan Detail Level",
            options=["Basic", "Standard", "Detailed", "Comprehensive"],
            value="Standard"
        )
    
    st.divider()
    
    # Information Section
    st.header("📊 About")
    st.info("""
    This AI-powered tool helps you:
    - Create personalized budgets
    - Develop investment strategies
    - Plan savings goals
    - Get current financial advice
    """)
    
    st.warning("⚠️ This tool provides general financial guidance. Always consult with a qualified financial advisor for personalized advice.")

# Main Content Area
if not anthropic_api_key or not serp_api_key:
    st.markdown('<div class="warning-box">⚠️ Please enter both API keys in the sidebar to get started.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🔑 How to Get Claude API Key
        
        **Steps to obtain your key:**
        1. Visit [console.anthropic.com](https://console.anthropic.com)
        2. Sign up or log in to your account
        3. Navigate to API Keys section
        4. Click "Create Key"
        5. Copy and save your API key securely
        
        **Features:**
        - ✅ Claude Sonnet 4 - Latest model
        - ✅ Smart and fast
        - ✅ Accurate and detailed results
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 How to Get SerpAPI Key
        
        **Steps to obtain your key:**
        1. Visit [serpapi.com](https://serpapi.com)
        2. Create a free account
        3. Go to Dashboard
        4. Copy your API key
        
        **Free plan includes:**
        - 🎁 100 searches per month free
        - 🌐 Google search access
        - 📊 Structured results
        """)

else:
    # Initialize agents with Claude
    try:
        researcher = Agent(
            name="Researcher",
            role="Searches for financial advice, investment opportunities, and savings strategies",
            model=Claude(id="claude-sonnet-4-20250514", api_key=anthropic_api_key),
            description=dedent(
                """\
            You are a world-class financial researcher. Given a user's financial goals and current financial situation,
            generate a list of search terms for finding relevant financial advice, investment opportunities, and savings strategies.
            Then search the web for each term, analyze the results, and return the 10 most relevant results.
            """
            ),
            instructions=[
                f"Current date: {datetime.now().strftime('%Y-%m-%d')}",
                "Given a user's financial goals and current financial situation, first generate a list of 3 search terms related to those goals.",
                "For each search term, `search_google` and analyze the results.",
                "From the results of all searches, return the 10 most relevant results to the user's preferences.",
                "Remember: the quality of the results is important.",
            ],
            tools=[SerpApiTools(api_key=serp_api_key)] if enable_research else [],
        )
        
        planner = Agent(
            name="Planner",
            role="Generates a personalized financial plan based on user preferences and research results",
            model=Claude(id="claude-sonnet-4-20250514", api_key=anthropic_api_key),
            description=dedent(
                """\
            You are a senior financial planner. Given a user's financial goals, current financial situation, and research results,
            your goal is to generate a personalized financial plan that meets the user's needs and preferences.
            """
            ),
            instructions=[
                f"Current date: {datetime.now().strftime('%Y-%m-%d')}",
                f"Generate a {detail_level.lower()} financial plan that includes suggested budgets, investment plans, and savings strategies.",
                "Ensure the plan is well-structured, informative, and engaging.",
                "Provide a nuanced and balanced plan, quoting facts where possible.",
                "Focus on clarity, coherence, and overall quality.",
                "Never make up facts or plagiarize. Always provide proper attribution.",
                "Include actionable steps and realistic timelines.",
                "Write the plan in a professional and clear manner.",
            ],
        )
        
        st.markdown('<div class="success-box">✅ AI agents initialized successfully using Claude Sonnet 4!</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error initializing agents: {str(e)}")
        st.stop()
    
    # User Input Section
    st.header("📝 Your Financial Information")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Financial Goals
        st.subheader("🎯 Financial Goals")
        financial_goals = st.text_area(
            "What are your financial goals?",
            placeholder="e.g., Save for retirement, buy a house, pay off debt, build emergency fund...",
            height=100,
            help="Be specific about your short-term and long-term financial objectives"
        )
        
        # Current Situation
        st.subheader("💼 Current Financial Situation")
        current_situation = st.text_area(
            "Describe your current financial situation",
            placeholder="Include: income, expenses, debts, savings, investments, dependents, etc.",
            height=150,
            help="Provide details about your income, expenses, existing savings, and any debts"
        )
    
    with col2:
        st.subheader("📊 Quick Profile")
        
        age_range = st.selectbox(
            "Age Range",
            ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
        )
        
        income_range = st.selectbox(
            "Annual Income",
            ["< $25k", "$25k-$50k", "$50k-$75k", "$75k-$100k", "$100k-$150k", "> $150k"]
        )
        
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
            value="Moderate"
        )
        
        time_horizon = st.selectbox(
            "Investment Time Horizon",
            ["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
        )
    
    # Generate Plan Button
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🚀 Generate My Financial Plan", type="primary")
    
    if generate_button:
        if not financial_goals or not current_situation:
            st.warning("⚠️ Please fill in both your financial goals and current situation to generate a plan.")
        else:
            # Create detailed user profile
            user_profile = f"""
            Financial Goals: {financial_goals}
            
            Current Situation: {current_situation}
            
            Profile Details:
            - Age Range: {age_range}
            - Annual Income: {income_range}
            - Risk Tolerance: {risk_tolerance}
            - Investment Time Horizon: {time_horizon}
            """
            
            with st.spinner("🔍 Analyzing your financial situation and researching current market conditions..."):
                try:
                    # Research phase
                    if enable_research:
                        with st.status("Conducting financial research...", expanded=True) as status:
                            st.write("🔍 Searching for relevant financial information...")
                            research_response = researcher.run(user_profile, stream=False)
                            st.write("✅ Research completed!")
                            status.update(label="Research complete!", state="complete")
                    
                    # Planning phase
                    with st.status("Generating your personalized financial plan...", expanded=True) as status:
                        st.write("📊 Creating personalized recommendations...")
                        plan_response = planner.run(user_profile, stream=False)
                        st.write("✅ Plan generated!")
                        status.update(label="Plan complete!", state="complete")
                    
                    # Display Results
                    st.success("✅ Your personalized financial plan is ready!")
                    
                    st.header("📋 Your Personalized Financial Plan")
                    st.markdown(plan_response.content)
                    
                    # Save history option
                    if save_history:
                        if 'plan_history' not in st.session_state:
                            st.session_state.plan_history = []
                        
                        st.session_state.plan_history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'goals': financial_goals,
                            'plan': plan_response.content
                        })
                    
                    # Export options
                    st.divider()
                    st.subheader("💾 Export Your Plan")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📄 Download as Text",
                            data=plan_response.content,
                            file_name=f"financial_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Create a formatted version
                        formatted_plan = f"""
# Personal Financial Plan
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Goals
{financial_goals}

## Current Situation
{current_situation}

## Personalized Plan
{plan_response.content}
"""
                        st.download_button(
                            label="📝 Download as Markdown",
                            data=formatted_plan,
                            file_name=f"financial_plan_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown"
                        )
                    
                    with col3:
                        if st.button("🔄 Generate New Plan"):
                            st.rerun()
                
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("Please check your API keys and try again.")
    
    # Display History
    if save_history and 'plan_history' in st.session_state and st.session_state.plan_history:
        st.divider()
        with st.expander("📜 View Plan History"):
            for i, plan in enumerate(reversed(st.session_state.plan_history)):
                st.markdown(f"**Plan {len(st.session_state.plan_history) - i}** - {plan['timestamp']}")
                st.markdown(f"*Goals:* {plan['goals'][:100]}...")
                if st.button(f"View Full Plan {len(st.session_state.plan_history) - i}", key=f"view_{i}"):
                    st.markdown(plan['plan'])
                st.divider()

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 0;'>
        <p>💡 Remember: This tool provides general guidance. Always consult with a qualified financial advisor for personalized advice.</p>
        <p>Made with ❤️ using Streamlit and Claude Sonnet 4</p>
    </div>
""", unsafe_allow_html=True)
