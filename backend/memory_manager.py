"""
memory_manager.py - Conversation Memory System
Stores and retrieves chat conversations in JSON format
Lightweight and optimized for low-compute laptops
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import uuid

from logger import logger

class MemoryManager:
    """
    Manages conversation history storage and retrieval.
    
    Uses JSON files for simplicity and portability.
    Each conversation has a unique session ID.
    """
    
    def __init__(self, memory_dir: str = "../memory"):
        """
        Initialize the memory manager.
        
        Args:
            memory_dir: Directory where conversations will be stored
        """
        self.memory_dir = Path(memory_dir)
        self.conversations_file = self.memory_dir / "conversations.json"
        
        # Create memory directory if it doesn't exist
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize conversations file if it doesn't exist
        if not self.conversations_file.exists():
            self._initialize_storage()
        
        logger.info(f"Memory manager initialized. Storage: {self.conversations_file}")
    
    def _initialize_storage(self):
        """Create initial empty storage file."""
        initial_data = {
            "sessions": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_messages": 0,
                "total_sessions": 0
            }
        }
        self._save_data(initial_data)
        logger.info("Initialized new conversation storage")
    
    def _load_data(self) -> Dict:
        """Load conversation data from JSON file."""
        try:
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading conversation data: {e}")
            return self._get_empty_data()
    
    def _save_data(self, data: Dict):
        """Save conversation data to JSON file."""
        try:
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving conversation data: {e}")
            raise
    
    def _get_empty_data(self) -> Dict:
        """Return empty data structure."""
        return {
            "sessions": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_messages": 0,
                "total_sessions": 0
            }
        }
    
    def create_session(self, user_id: str = "anonymous") -> str:
        """
        Create a new conversation session.
        
        Args:
            user_id: User identifier
        
        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        
        data = self._load_data()
        
        new_session = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "messages": [],
            "message_count": 0
        }
        
        data["sessions"].append(new_session)
        data["metadata"]["total_sessions"] += 1
        
        self._save_data(data)
        
        logger.info(f"Created new session: {session_id} for user: {user_id}")
        return session_id
    
    def add_message(
        self, 
        session_id: str, 
        message: str, 
        sender: str,
        response: Optional[str] = None
    ) -> bool:
        """
        Add a message to a session.
        
        Args:
            session_id: Session identifier
            message: User message text
            sender: Who sent the message ('user' or 'ai')
            response: AI response (if sender is 'user')
        
        Returns:
            bool: Success status
        """
        try:
            data = self._load_data()
            
            # Find the session
            session = None
            for s in data["sessions"]:
                if s["session_id"] == session_id:
                    session = s
                    break
            
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            # Create message entry
            message_entry = {
                "timestamp": datetime.now().isoformat(),
                "sender": sender,
                "message": message
            }
            
            if response and sender == "user":
                message_entry["response"] = response
            
            # Add to session
            session["messages"].append(message_entry)
            session["message_count"] += 1
            session["last_updated"] = datetime.now().isoformat()
            
            data["metadata"]["total_messages"] += 1
            
            self._save_data(data)
            
            logger.info(f"Added message to session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return False
    
    def get_session_history(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            Session data with messages, or None if not found
        """
        try:
            data = self._load_data()
            
            for session in data["sessions"]:
                if session["session_id"] == session_id:
                    logger.info(f"Retrieved session: {session_id}")
                    return session
            
            logger.warning(f"Session not found: {session_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving session: {e}")
            return None
    
    def get_recent_sessions(self, limit: int = 10, user_id: Optional[str] = None) -> List[Dict]:
        """
        Get recent conversation sessions.
        
        Args:
            limit: Maximum number of sessions to return
            user_id: Filter by user ID (optional)
        
        Returns:
            List of recent sessions
        """
        try:
            data = self._load_data()
            sessions = data["sessions"]
            
            # Filter by user_id if provided
            if user_id:
                sessions = [s for s in sessions if s.get("user_id") == user_id]
            
            # Sort by last_updated (most recent first)
            sessions.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
            
            # Return limited results
            return sessions[:limit]
            
        except Exception as e:
            logger.error(f"Error retrieving recent sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session.
        
        Args:
            session_id: Session to delete
        
        Returns:
            bool: Success status
        """
        try:
            data = self._load_data()
            
            # Find and remove session
            original_count = len(data["sessions"])
            data["sessions"] = [s for s in data["sessions"] if s["session_id"] != session_id]
            
            if len(data["sessions"]) < original_count:
                data["metadata"]["total_sessions"] -= 1
                self._save_data(data)
                logger.info(f"Deleted session: {session_id}")
                return True
            else:
                logger.warning(f"Session not found for deletion: {session_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            data = self._load_data()
            
            stats = {
                "total_sessions": data["metadata"]["total_sessions"],
                "total_messages": data["metadata"]["total_messages"],
                "storage_created": data["metadata"]["created"],
                "active_sessions": len(data["sessions"]),
                "storage_size_kb": round(os.path.getsize(self.conversations_file) / 1024, 2)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def clear_all_sessions(self) -> bool:
        """
        Clear all conversation history (use with caution!).
        
        Returns:
            bool: Success status
        """
        try:
            self._initialize_storage()
            logger.warning("All conversation history cleared!")
            return True
        except Exception as e:
            logger.error(f"Error clearing sessions: {e}")
            return False


# Create a singleton instance
memory_manager = MemoryManager()
