# HackMerlin Autonomous Agent

An intelligent web automation agent designed to play the puzzle game [hackmerlin.io](https://hackmerlin.io/) autonomously using Selenium WebDriver and OpenAI's GPT-4 for password extraction.

## 🎯 Project Overview

This project implements an autonomous agent that can navigate through the HackMerlin puzzle game, interact with Merlin (the game's AI), extract passwords from responses, and progress through multiple levels. The agent combines rule-based extraction with AI-powered fallback mechanisms to solve various puzzle types.

## 🚀 Features

- **Web Automation**: Selenium-based browser automation for reliable interaction
- **Intelligent Password Extraction**: Hybrid approach using rule-based logic and AI
- **Multi-Level Support**: Handles 7 different puzzle types with specialized strategies
- **Error Handling**: Robust retry mechanisms and fallback strategies
- **Logging**: Comprehensive logging for debugging and monitoring
- **Environment Configuration**: Secure API key management

## 📁 Project Structure

```
hackmerlin-agent/
├── working_agent.py          # Main automation agent
├── llm_extractor.py          # Password extraction logic
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
└── README.md                 # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Chrome browser
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShivramSriramulu/HackmerlinSpearbit.git
   cd HackmerlinSpearbit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the agent**
   ```bash
   python working_agent.py
   ```

## 🎮 How It Works

### Level-Specific Strategies

| Level | Prompt | Strategy | Extraction Method |
|-------|--------|----------|-------------------|
| 1 | "Password" | Direct extraction | Quoted words, uppercase words |
| 2-3 | "Password in reverse" | Reverse + correct | Reverse letters, AI correction |
| 4-5 | "Acrostic Poem" | First letter acrostic | AI extraction from poem lines |
| 6 | "Acrostic Poem" | First letter acrostic | AI extraction from poem lines |
| 7 | Complex prompts | Last word acrostic | AI extraction from last words |

### Architecture

1. **WebDriver Setup**: Initializes Chrome with optimized settings
2. **Navigation**: Loads hackmerlin.io and waits for React app
3. **Level Solving Loop**:
   - Get appropriate prompt for current level
   - Send prompt to Merlin via chat interface
   - Extract Merlin's response
   - Use rule-based or AI extraction to get password
   - Submit password and handle result
   - Progress to next level

## 📊 Performance Results

### Current Success Rate: 71.4% (5/7 levels)

- ✅ **Level 1**: Direct password extraction
- ✅ **Level 2**: Reverse word with AI correction
- ✅ **Level 3**: Reverse word with AI correction  
- ✅ **Level 4**: Acrostic poem extraction
- ✅ **Level 5**: Acrostic poem extraction
- ❌ **Level 6**: Acrostic extraction (needs improvement)
- ❌ **Level 7**: Last word acrostic (not reached consistently)

## 🔧 Technical Implementation

### Key Components

#### 1. WorkingHackMerlinAgent Class
- Handles web automation and game interaction
- Manages level progression and error handling
- Implements retry logic and fallback mechanisms

#### 2. PasswordExtractor Class
- Rule-based extraction for simple levels
- AI-powered extraction for complex puzzles
- Word validation and correction

#### 3. LLMExtractor Class
- OpenAI GPT-4 integration
- Level-specific prompt engineering
- Response parsing and validation

### Dependencies

```txt
selenium>=4.15.0          # Web automation
webdriver-manager>=4.0.0  # Chrome driver management
python-dotenv>=1.0.0      # Environment variables
openai>=1.0.0             # AI integration
groq>=0.4.0               # Alternative AI provider
```

## 🤔 Analysis & Reflection

### If cost and compute requirements were not an issue, how would you improve the agent?

**1. Advanced AI Models**
- Use GPT-4 Turbo with higher context windows for better understanding
- Implement Claude-3 Opus for superior reasoning capabilities
- Fine-tune models specifically on puzzle-solving tasks

**2. Multi-Modal Capabilities**
- Add computer vision to analyze visual elements
- Implement OCR for text extraction from images
- Use image recognition for pattern detection

**3. Enhanced Reasoning**
- Implement chain-of-thought prompting for complex puzzles
- Add self-reflection mechanisms to verify solutions
- Use multiple AI models in parallel for consensus

**4. Advanced Web Automation**
- Implement headless browser with full rendering
- Add screenshot analysis for visual debugging
- Use more sophisticated element detection

**5. Learning Capabilities**
- Implement reinforcement learning to improve over time
- Add memory of previous attempts and solutions
- Create a knowledge base of puzzle patterns

### If the agent had to be run in a cost-constrained environment, how would you redesign it?

**1. Optimize AI Usage**
- Use smaller, faster models (GPT-3.5-turbo, Claude Haiku)
- Implement caching for repeated patterns
- Reduce API calls through better rule-based logic

**2. Local Processing**
- Implement local LLMs (Llama, Mistral) for basic tasks
- Use rule-based extraction for more levels
- Pre-compute common patterns and solutions

**3. Efficient Architecture**
- Batch API requests where possible
- Implement smart retry logic to avoid unnecessary calls
- Use cheaper models for initial attempts

**4. Hybrid Approach**
- Combine multiple lightweight models
- Use ensemble methods for better accuracy
- Implement fallback chains (cheapest → most expensive)

**5. Resource Management**
- Add request rate limiting
- Implement cost tracking and budgeting
- Use async processing to reduce wait times

### What were unique challenges that you faced building this?

**1. Dynamic Web Interface**
- The React-based interface had changing element IDs
- Required robust element selection strategies
- Needed to handle dynamic content loading

**2. Puzzle Variety**
- Each level required different extraction strategies
- Some puzzles had ambiguous solutions
- Level 7's "last word" acrostic was particularly challenging

**3. AI Prompt Engineering**
- Crafting effective prompts for different puzzle types
- Balancing specificity with flexibility
- Handling edge cases in AI responses

**4. Error Handling**
- Distinguishing between temporary failures and incorrect solutions
- Implementing appropriate retry strategies
- Managing different types of game responses

**5. Rate Limiting & Reliability**
- Managing API rate limits
- Handling network timeouts
- Ensuring consistent performance across runs

**6. Game State Management**
- Tracking level progression accurately
- Handling unexpected game state changes
- Managing browser session persistence

## 🚀 Future Improvements

### Short-term
- Fix Level 6 acrostic extraction
- Improve Level 7 last-word extraction
- Add better error recovery mechanisms

### Medium-term
- Implement visual analysis capabilities
- Add support for more puzzle types
- Create a web interface for monitoring

### Long-term
- Develop machine learning models trained on puzzle data
- Create a general-purpose puzzle-solving framework
- Implement multi-game support

## 📈 Metrics & Monitoring

The agent includes comprehensive logging for:
- Level progression tracking
- Password extraction success rates
- AI API usage and costs
- Error patterns and debugging information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Selenium team for web automation tools
- The HackMerlin game creators for the challenging puzzles

## 📞 Contact

For questions or contributions, please contact:
- GitHub: [@ShivramSriramulu](https://github.com/ShivramSriramulu/)
- Project Repository: [HackmerlinSpearbit](https://github.com/ShivramSriramulu/HackmerlinSpearbit)

---

*This project demonstrates the potential of combining web automation with AI for solving complex puzzle games autonomously. While not perfect, it showcases effective strategies for handling diverse puzzle types and provides a foundation for more advanced implementations.*
