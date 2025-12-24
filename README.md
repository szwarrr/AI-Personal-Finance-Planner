# 💰 AI Personal Finance Planner

A powerful Streamlit application that leverages **OpenAI GPT-4o** and **SerpAPI** to create personalized financial plans. Get AI-powered budgets, investment strategies, and savings recommendations tailored to your unique financial situation.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

- **🎯 Personalized Financial Planning** - AI-generated budgets, investment plans, and savings strategies
- **🔍 Smart Web Research** - Automated search for current financial advice and market trends using SerpAPI
- **📊 Risk Assessment** - Customized recommendations based on your risk tolerance and time horizon
- **💾 Export Plans** - Download your financial plans as text or markdown files
- **📜 History Tracking** - Save and review your previous financial plans
- **🎨 Professional UI** - Modern, intuitive interface with real-time status updates

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- An **OpenAI API key** (for GPT-4o access)
- A **SerpAPI key** (for web search functionality)

---

## 🚀 Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/ai-finance-planner.git
cd ai-finance-planner
```

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
streamlit>=1.28.0
openai>=1.0.0
agno>=0.1.0
serpapi>=2.4.0
```

### 3. Get Your API Keys

#### **OpenAI API Key:**
1. Visit [https://platform.openai.com](https://platform.openai.com)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy and save your API key securely

#### **SerpAPI Key:**
1. Visit [https://serpapi.com](https://serpapi.com)
2. Create a free account
3. Go to your **Dashboard**
4. Copy your API key from the dashboard

---

## 💻 Running the Application

Start the Streamlit application with:

```bash
streamlit run finance_agent.py
```

The app will automatically open in your default browser at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Enter API Keys
1. Open the application in your browser
2. In the **sidebar**, locate the "🔑 API Keys" section
3. Enter your **OpenAI API Key**
4. Enter your **SerpAPI Key**

### Step 2: Configure Settings (Optional)
Customize your experience in the sidebar:
- **Enable Web Research** - Toggle real-time web search
- **Save Plan History** - Keep track of generated plans
- **Plan Detail Level** - Choose between Basic, Standard, Detailed, or Comprehensive

### Step 3: Complete Your Financial Profile

#### **Quick Profile:**
- Select your **Age Range**
- Choose your **Annual Income** bracket
- Set your **Risk Tolerance** (Conservative to Aggressive)
- Define your **Investment Time Horizon**

#### **Financial Goals:**
Describe what you want to achieve:
```
Example: "Save $50,000 for a house down payment in 3 years, 
build an emergency fund of $10,000, and start investing for retirement."
```

#### **Current Financial Situation:**
Provide details about:
- Monthly income and expenses
- Existing savings and investments
- Outstanding debts (credit cards, loans, mortgage)
- Number of dependents
- Current assets

```
Example: "Monthly income: $5,000, Expenses: $3,500, 
Savings: $15,000, Credit card debt: $8,000, No dependents."
```

### Step 4: Generate Your Plan
1. Click the **"🚀 Generate My Financial Plan"** button
2. Wait while the AI:
   - 🔍 Researches current financial information
   - 📊 Analyzes your situation
   - 📝 Creates your personalized plan
3. Review your comprehensive financial strategy

### Step 5: Export and Save
- **📄 Download as Text** - Plain text format
- **📝 Download as Markdown** - Formatted markdown file
- **📜 View History** - Access previously generated plans

---

## 🛠️ Application Architecture

The application uses two AI agents working together:

### 1. **Researcher Agent**
- Generates relevant search queries based on your goals
- Searches the web using SerpAPI
- Analyzes and filters results
- Returns the 10 most relevant findings

### 2. **Planner Agent**
- Reviews your profile and research results
- Generates personalized recommendations
- Creates actionable financial strategies
- Provides balanced, evidence-based advice

---

## 📁 Project Structure

```
ai-finance-planner/
│
├── finance_agent.py          # Main application file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

---

## 🔧 Code Overview

### Key Components

**Agent Configuration:**
```python
researcher = Agent(
    name="Researcher",
    role="Searches for financial advice and investment opportunities",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[SerpApiTools(api_key=serp_api_key)]
)

planner = Agent(
    name="Planner",
    role="Generates personalized financial plans",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key)
)
```

**User Input Collection:**
```python
financial_goals = st.text_area("What are your financial goals?")
current_situation = st.text_area("Describe your current financial situation")
age_range = st.selectbox("Age Range", ["18-25", "26-35", ...])
risk_tolerance = st.select_slider("Risk Tolerance", options=[...])
```

**Plan Generation:**
```python
research_response = researcher.run(user_profile, stream=False)
plan_response = planner.run(user_profile, stream=False)
st.markdown(plan_response.content)
```

---

## 🎯 Use Cases

### Personal Budgeting
Create monthly budgets aligned with your income and goals

### Investment Planning
Develop diversified investment strategies based on your risk profile

### Retirement Planning
Calculate retirement needs and contribution strategies

### Debt Management
Get prioritized debt payoff plans and consolidation advice

### Emergency Fund
Determine appropriate fund size and savings timeline

### Major Purchase Planning
Save strategically for homes, cars, or education

---

## 🔒 Security Best Practices

### Protecting Your API Keys

**Option 1: Environment Variables**

Create a `.env` file:
```env
OPENAI_API_KEY=sk-your-key-here
SERPAPI_KEY=your-serpapi-key-here
```

Update your code:
```python
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
serp_api_key = os.getenv("SERPAPI_KEY")
```

**Option 2: Streamlit Secrets**

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-key-here"
SERPAPI_KEY = "your-serpapi-key-here"
```

Access in code:
```python
openai_api_key = st.secrets["OPENAI_API_KEY"]
serp_api_key = st.secrets["SERPAPI_KEY"]
```

### Important Security Notes
- ⚠️ **Never commit API keys to version control**
- 🔐 Add `.env` and `secrets.toml` to `.gitignore`
- 🔄 Rotate keys regularly
- 💳 Monitor API usage for unexpected charges

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"Invalid API Key"** | Verify keys are correct and active |
| **"Module not found"** | Run `pip install -r requirements.txt` |
| **"Rate limit exceeded"** | Check API usage limits and quotas |
| **"No search results"** | Verify SerpAPI key and account status |
| **Slow performance** | Reduce detail level or disable web research |

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ⚠️ Important Disclaimer

**This application provides general financial guidance for educational purposes only.**

- ❌ **NOT professional financial advice**
- ❌ **NOT a substitute for licensed financial advisors**
- ❌ **NOT guaranteed to be accurate or suitable for your situation**

**Always consult with qualified financial professionals before making significant financial decisions.**

The creators assume no liability for financial losses or decisions made using this tool.

---

## 📈 Future Enhancements

- [ ] Integration with bank accounts (Plaid API)
- [ ] Interactive charts and visualizations
- [ ] Goal tracking dashboard
- [ ] Multi-language support
- [ ] PDF export with custom branding
- [ ] Email notifications for milestones
- [ ] Collaborative planning for couples
- [ ] Mobile-responsive improvements

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For GPT-4o API
- **SerpAPI** - For web search capabilities
- **Streamlit** - For the amazing framework
- **Agno** - For agent orchestration
- The open-source community

