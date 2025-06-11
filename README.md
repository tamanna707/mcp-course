# Building AI Agents with MCP: Complete Course Materials

This repository contains all the demo code, examples, and hands-on materials for the O'Reilly Live Training course "Building AI Agents with MCP: The HTTP Moment of AI?"

## 🎯 Course Overview

The Model Context Protocol (MCP) is revolutionizing how AI applications connect to external tools and data sources. This course provides comprehensive, hands-on experience with MCP through practical demos and real-world examples.

### What You'll Learn

- **MCP Fundamentals**: Core concepts, architecture, and capabilities
- **MCP Capabilities**: Tools, Resources, Prompts, and Sampling
- **Agent Development**: Building agents with Google ADK, and OpenAI SDK
- **Consumer Applications**: Using MCP with Claude Desktop and Cursor IDE
- **Security Best Practices**: Securing MCP implementations and preventing attacks

## 📁 Repository Structure

```
mcp-course/
├── README.md                           # This file - complete course guide
├── Makefile                           # Automation scripts
├── presentation/                      # Course presentation slides
│   └── presentation.html
└── notebooks/                        # All demo materials organized by topic
    ├── 01-introduction-to-mcp/       # MCP basics and first server
    ├── 02-first-mcp-server/          # Building your first MCP server
    ├── 03-tools-resources-prompts-sampling/  # Core MCP capabilities
    ├── 04-google-adk-agents/         # Google Agent Development Kit demos
    ├── 05-openai-agents/             # OpenAI Agents SDK with MCP
    ├── 06-claude-desktop-cursor-demos/  # Consumer app integration
    ├── 07-security-tips/             # Security best practices
    └── assets-resources/             # Images and supporting materials
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (Required for all demos)
- **Node.js 18+** (Required for some MCP servers)
- **Git** (For repository operations)

### API Keys Needed

Depending on which demos you want to run:

- [**OpenAI API Key**](https://platform.openai.com/docs/quickstart?api-mode=chat) (for OpenAI demos)
- [**Anthropic API Key**](https://docs.anthropic.com/en/docs/get-started) (for Claude-based demos)
- [**Google Cloud Project**](https://arc.net/l/quote/pyqkrzxd) (for ADK demos)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd mcp-course

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install base dependencies
pip install mcp mcp[cli] google-adk python-dotenv
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```env
# API Keys (add the ones you have)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id

# Optional: Custom paths
MCP_DEMO_PATH=/path/to/your/demo/files
```

### 3. Quick Test

Test your setup with a basic MCP server:

```bash
cd notebooks/01-introduction-to-mcp
pip install -r requirements.txt
python basic_server.py
```

## 📚 Demo Sections Guide

### 01. Introduction to MCP

**What it covers**: MCP fundamentals, basic server implementation, client interaction

**Files**:
- `basic_server.py` - Minimal MCP server
- `test_client.py` - Test client for interaction
- `README.md` - Detailed explanation

**Running**:
```bash
cd notebooks/01-introduction-to-mcp
pip install -r requirements.txt

# Terminal 1: Start the server
python basic_server.py

# Terminal 2: Test with client
python test_client.py
```

**Key Learning**: Understanding MCP architecture and basic client-server communication.

---

### 02. First MCP Server

**What it covers**: Building a practical weather server, Claude Desktop integration

**Files**:
- `weather_server.py` - Complete weather MCP server
- `claude_desktop_config.json` - Configuration for Claude Desktop
- `README.md` - Setup instructions

**Running**:
```bash
cd notebooks/02-first-mcp-server
pip install -r requirements.txt

# Start the weather server
python weather_server.py

# Optional: Configure with Claude Desktop
# Copy claude_desktop_config.json to ~/.claude_desktop_config.json
```

**Key Learning**: Building real-world MCP servers and integrating with consumer applications.

---

### 03. Tools, Resources, Prompts & Sampling

**What it covers**: All four core MCP capabilities with comprehensive examples

**Files**:
- `comprehensive_mcp_server.py` - Server implementing all capabilities
- `test_client.py` - Client testing all capabilities
- `README.md` - Detailed capability explanations

**Running**:
```bash
cd notebooks/03-tools-resources-prompts-sampling
pip install -r requirements.txt

# Terminal 1: Start comprehensive server
python comprehensive_mcp_server.py

# Terminal 2: Test all capabilities
python test_client.py
```

**Key Learning**: Deep dive into MCP's four core capabilities and their use cases.

---

### 04. Google ADK Agents

**What it covers**: Building agents with Google's Agent Development Kit that use MCP tools

**Prerequisites**: Google Cloud account and project

**Files**:
- `adk_mcp_agent.py` - Main ADK agent with MCP integration
- `weather_mcp_server.py` - Sample weather server
- `database_mcp_server.py` - Sample database server

**Running**:
```bash
cd notebooks/04-google-adk-agents
pip install -r requirements.txt

# Set up Google Cloud credentials
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Start MCP servers (separate terminals)
python weather_mcp_server.py &
python database_mcp_server.py &

# Run ADK agent
python adk_mcp_agent.py
```

**Key Learning**: Integrating MCP with Google's enterprise agent framework.

---

### 05. OpenAI Agents

**What it covers**: Building agents with OpenAI's Agents SDK that connect to MCP servers

**Prerequisites**: OpenAI API key

**Files**:
- `openai_mcp_agent.py` - Main OpenAI agent with MCP integration
- `mcp_server_examples.py` - Sample MCP servers for testing

**Running**:
```bash
cd notebooks/06-openai-agents
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-openai-api-key"

# Start sample MCP servers
python mcp_server_examples.py --mode weather &
python mcp_server_examples.py --mode calculator &

# Run OpenAI agents
python openai_mcp_agent.py
```

**Key Learning**: Native MCP integration in OpenAI's Agents SDK.

---

### 06. Claude Desktop & Cursor Demos

**What it covers**: End-user MCP experiences with consumer applications

**Prerequisites**: Claude Desktop app installed

**Files**:
- `development_mcp_server.py` - Development-focused MCP server
- `claude_desktop_configs/` - Sample configurations
- `README.md` - Setup instructions

**Running**:
```bash
cd notebooks/07-claude-desktop-cursor-demos
pip install -r requirements.txt

# Start development server
python development_mcp_server.py

# Configure Claude Desktop
cp claude_desktop_configs/development.json ~/.claude_desktop_config.json

# Restart Claude Desktop to load new configuration
```

**Key Learning**: Practical MCP usage in real applications for enhanced productivity.

---

### 07. Security Tips

**What it covers**: Security vulnerabilities, best practices, and mitigation strategies

**Files**:
- `security_audit_server.py` - Security auditing tools
- `vulnerable_server.py` - Intentionally vulnerable examples
- `secure_server.py` - Hardened implementation
- `README.md` - Complete security guide

**Running**:
```bash
cd notebooks/08-security-tips
pip install -r requirements.txt

# Run security audit
python security_audit_server.py --audit-mode

# Test vulnerabilities (educational only)
python vulnerable_server.py &
python security_tests.py
```

**Key Learning**: Understanding and mitigating MCP security risks.

## 🛠️ Automation with Makefile

The repository includes a Makefile for common tasks:

```bash
# Set up all environments
make setup-all

# Run all tests
make test-all

# Clean up all environments
make clean-all

# Start all demo servers
make start-servers

# Stop all demo servers
make stop-servers
```

## 🔧 Troubleshooting

### Common Issues

1. **"mcp module not found"**
   ```bash
   pip install mcp model-context-protocol
   ```

2. **"Permission denied" errors**
   ```bash
   chmod +x *.py
   ```

3. **Claude Desktop not recognizing MCP servers**
   - Check configuration file location: `~/.claude_desktop_config.json`
   - Verify server paths are absolute
   - Restart Claude Desktop after configuration changes

4. **API rate limiting**
   - Use API keys with sufficient quota
   - Implement rate limiting in custom servers
   - Add delays between requests in test scripts

### Getting Help

1. **Check the README** in each demo directory for specific instructions
2. **Review error logs** for detailed error messages
3. **Test MCP servers independently** before integrating with agents
4. **Use the MCP Inspector** tool for debugging:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

## 📖 Additional Resources

### Official Documentation
- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)

### Agent Frameworks
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

### Community Resources
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [MCP Community Examples](https://github.com/esxr/langgraph-mcp)
- [Glama MCP Directory](https://glama.ai/mcp)

## 🤝 Contributing

Found an issue or want to improve the demos? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This course material is provided for educational purposes. Individual components may have their own licenses - please check specific directories for details.

## 🎓 Course Information

**Instructor**: Lucas Soares  
**Course**: Building AI Agents with MCP: The HTTP Moment of AI?  
**Platform**: O'Reilly Live Training  

### Connect with the Instructor
- 📚 [Blog](https://enkrateialucca.github.io/lucas-landing-page/)
- 🔗 [LinkedIn](https://www.linkedin.com/in/lucas-soares-969044167/)
- 🐦 [Twitter/X](https://x.com/LucasEnkrateia)
- 📺 [YouTube](https://www.youtube.com/@automatalearninglab)
- 📧 Email: lucasenkrateia@gmail.com

---

**Happy Learning! 🚀**

*The Model Context Protocol represents a significant step toward standardized AI-tool integration. Through these hands-on demos, you'll gain practical experience with this revolutionary technology that's shaping the future of AI applications.*
