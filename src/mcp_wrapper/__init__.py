"""
CyberHunt MCP Wrapper

Wrapper dla integracji narzędzi OSINT CyberHunt z protokołem MCP (Model Context Protocol).
Umożliwia AI korzystanie z narzędzi OSINT przez standardowy interfejs MCP.
"""

from .client import CyberHuntMCPClient, MCPToolHandler

__version__ = "1.0.0"
__all__ = ["CyberHuntMCPClient", "MCPToolHandler"]
