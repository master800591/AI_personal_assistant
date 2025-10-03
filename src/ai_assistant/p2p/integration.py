#!/usr/bin/env python3
"""
P2P Integration for AI Corporation
Distributed networking capabilities for autonomous operations
"""

import asyncio
import time
from typing import Dict, Any, Optional

def check_integration_dependencies():
    """Check if P2P and Ollama toolkits are available"""
    components = {
        'p2p': False,
        'ollama': False
    }
    
    try:
        # Try to import real P2P toolkit (may not exist)
        from p2p_toolkit import P2PNode
        components['p2p'] = True
        print("[OK] P2P Toolkit available")
    except ImportError:
        print("[MOCK] P2P Toolkit not available - using simulation")
    
    try:
        # Try to import Ollama toolkit
        import ollama_toolkit
        components['ollama'] = True
        print("[OK] Ollama Toolkit available")
    except ImportError:
        print("[MOCK] Ollama Toolkit not available - using simulation")
    
    return components

class DistributedOllamaNode:
    """AI Corporation distributed node with P2P capabilities"""
    
    def __init__(self, name: str = None, port: int = 8888):
        """Initialize the distributed node"""
        self.components = check_integration_dependencies()
        self.name = name or "AI-Corporation-Node"
        self.port = port
        self.running = False
        
        # Initialize P2P node (mock if real one not available)
        self.p2p_node = self.create_p2p_node()
        
        print(f"[INIT] {self.name} initialized on port {self.port}")
        print(f"  P2P: {'✓' if self.p2p_node else '✗'}")
        print(f"  Ollama: {'✓' if self.components['ollama'] else '✗'}")
    
    def create_p2p_node(self):
        """Create P2P node (real or mock)"""
        if self.components['p2p']:
            # Use real P2P toolkit if available
            from p2p_toolkit import P2PNode
            return P2PNode(name=self.name, port=self.port)
        else:
            # Create mock P2P node for testing
            class MockP2PNode:
                def __init__(self, name, port):
                    self.name = name
                    self.port = port
                    self.peers = []
                    
                async def start(self):
                    print(f"[MOCK-P2P] {self.name} started on port {self.port}")
                    return True
                    
                async def stop(self):
                    print(f"[MOCK-P2P] {self.name} stopped")
                    return True
                    
                async def broadcast(self, message):
                    print(f"[MOCK-P2P] Broadcasting: {message}")
                    return True
            
            return MockP2PNode(self.name, self.port)
    
    async def start_services(self):
        """Start all distributed services"""
        try:
            self.running = True
            print(f"[START] Starting {self.name} services...")
            
            # Start P2P networking
            if self.p2p_node:
                await self.p2p_node.start()
            
            # Discover network peers
            await self.discover_peers()
            
            # Start monitoring
            asyncio.create_task(self.health_monitor())
            
            print(f"[OK] {self.name} fully operational")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start services: {e}")
            return False
    
    async def stop_services(self):
        """Stop all services gracefully"""
        self.running = False
        if self.p2p_node:
            await self.p2p_node.stop()
        print(f"[STOP] {self.name} services stopped")
    
    async def discover_peers(self):
        """Discover other AI Corporation nodes in the network"""
        print("[P2P] Discovering network peers...")
        
        # Simulate peer discovery
        mock_peers = [
            "ai-corp-alpha:8889",
            "ai-corp-beta:8890",
            "ai-corp-gamma:8891"
        ]
        
        print(f"[P2P] Found {len(mock_peers)} potential peers")
        for peer in mock_peers:
            print(f"  → {peer}")
        
        return mock_peers
    
    async def health_monitor(self):
        """Background health monitoring"""
        while self.running:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                if self.running:
                    print(f"[HEALTH] {self.name} - Status: Operational ✓")
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[HEALTH] Monitor error: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current node status"""
        return {
            'name': self.name,
            'port': self.port,
            'running': self.running,
            'p2p_enabled': self.p2p_node is not None,
            'ollama_enabled': self.components['ollama'],
            'timestamp': time.time()
        }

# Test and demo functions
async def demo_p2p_integration():
    """Demonstrate P2P integration capabilities"""
    print("=== AI Corporation P2P Integration Demo ===")
    
    # Create node
    node = DistributedOllamaNode("Demo-Node", port=8888)
    
    try:
        # Start services
        await node.start_services()
        
        # Run for demonstration
        print("Running demo for 5 seconds...")
        await asyncio.sleep(5)
        
        # Show status
        status = node.get_status()
        print(f"Node Status: {status}")
        
    finally:
        # Clean shutdown
        await node.stop_services()

if __name__ == "__main__":
    # Run demo
    try:
        asyncio.run(demo_p2p_integration())
    except KeyboardInterrupt:
        print("\nDemo interrupted")