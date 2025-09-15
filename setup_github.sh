#!/bin/bash

# HackMerlin Agent - GitHub Repository Setup Script
# This script helps set up the GitHub repository for the HackMerlin Agent project

echo "🚀 Setting up HackMerlin Agent GitHub Repository"
echo "================================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: HackMerlin Agent with autonomous puzzle solving capabilities

- Web automation using Selenium WebDriver
- AI-powered password extraction with OpenAI GPT-4
- Support for 7 different puzzle types
- Robust error handling and retry mechanisms
- Comprehensive logging and monitoring
- 71.4% success rate (5/7 levels completed)

Features:
- Level 1: Direct password extraction
- Level 2-3: Reverse word with AI correction
- Level 4-5: Acrostic poem extraction
- Level 6: Acrostic poem extraction (needs improvement)
- Level 7: Last word acrostic (complex prompts)

Dependencies: selenium, openai, python-dotenv, webdriver-manager"

# Set up remote repository
echo "🔗 Setting up remote repository..."
echo "Using your existing repository: https://github.com/ShivramSriramulu/HackmerlinSpearbit.git"
echo ""
echo "git remote add origin https://github.com/ShivramSriramulu/HackmerlinSpearbit.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""

# Create .env.example file
echo "📄 Creating .env.example file..."
cat > .env.example << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Groq API for alternative AI provider
GROQ_API_KEY=your_groq_api_key_here

# Optional: Logging configuration
LOG_LEVEL=INFO
EOF

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a repository on GitHub at https://github.com/hrkrshnn/hackmerlin-agent"
echo "2. Run the git remote commands shown above"
echo "3. Copy .env.example to .env and add your API keys"
echo "4. Run 'python working_agent.py' to test the agent"
echo ""
echo "🎉 Happy coding!"
