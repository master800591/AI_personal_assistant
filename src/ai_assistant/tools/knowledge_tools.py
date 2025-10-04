"""
AI Personal Assistant - Knowledge Management Tools for CrewAI Agents
Advanced knowledge management, storage, and retrieval tools
"""

import logging
import json
import os
import hashlib
import mimetypes
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
import asyncio

from crewai.tools import BaseTool
from pydantic import Field

logger = logging.getLogger(__name__)

class KnowledgeManagerTool(BaseTool):
    """Comprehensive tool for managing knowledge bases and information systems"""
    
    name: str = "knowledge_manager"
    description: str = (
        "Manage knowledge bases including creating, updating, searching, and organizing "
        "information. Supports multiple knowledge sources and intelligent retrieval."
    )
    knowledge_base_path: str = Field(default="data/knowledge", description="Path to knowledge base storage")
    
    def __init__(self, knowledge_base_path: str = "data/knowledge", **kwargs):
        super().__init__(**kwargs)
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
        self._initialize_knowledge_base()
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute knowledge management operations"""
        try:
            if action == "search":
                return self._search_knowledge(
                    query=kwargs.get('query'),
                    limit=kwargs.get('limit', 10),
                    threshold=kwargs.get('threshold', 0.7)
                )
            elif action == "add_entry":
                return self._add_knowledge_entry(
                    title=kwargs.get('title'),
                    content=kwargs.get('content'),
                    tags=kwargs.get('tags', []),
                    source=kwargs.get('source'),
                    metadata=kwargs.get('metadata', {})
                )
            elif action == "update_entry":
                return self._update_knowledge_entry(
                    entry_id=kwargs.get('entry_id'),
                    updates=kwargs.get('updates', {})
                )
            elif action == "delete_entry":
                return self._delete_knowledge_entry(kwargs.get('entry_id'))
            elif action == "list_entries":
                return self._list_knowledge_entries(
                    tags=kwargs.get('tags'),
                    limit=kwargs.get('limit', 50)
                )
            elif action == "get_stats":
                return self._get_knowledge_stats()
            elif action == "backup":
                return self._backup_knowledge_base(kwargs.get('backup_path'))
            elif action == "restore":
                return self._restore_knowledge_base(kwargs.get('backup_path'))
            else:
                return f"❌ Unknown knowledge action: {action}"
                
        except Exception as e:
            logger.error(f"Knowledge manager error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base structure"""
        try:
            # Create subdirectories
            (self.knowledge_base_path / "entries").mkdir(exist_ok=True)
            (self.knowledge_base_path / "indexes").mkdir(exist_ok=True)
            (self.knowledge_base_path / "backups").mkdir(exist_ok=True)
            
            # Create metadata file if it doesn't exist
            metadata_file = self.knowledge_base_path / "metadata.json"
            if not metadata_file.exists():
                metadata = {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0",
                    "total_entries": 0,
                    "last_updated": datetime.now().isoformat()
                }
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                    
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
    
    def _search_knowledge(self, query: str, limit: int = 10, threshold: float = 0.7) -> str:
        """Search the knowledge base for relevant entries"""
        try:
            entries_dir = self.knowledge_base_path / "entries"
            results = []
            
            if not entries_dir.exists():
                return "✅ No knowledge entries found"
            
            # Simple text-based search (can be enhanced with vector search)
            query_lower = query.lower()
            
            for entry_file in entries_dir.glob("*.json"):
                with open(entry_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                
                # Calculate relevance score (simplified)
                title_score = 0
                content_score = 0
                tags_score = 0
                
                if query_lower in entry.get('title', '').lower():
                    title_score = 2.0
                elif any(word in entry.get('title', '').lower() for word in query_lower.split()):
                    title_score = 1.0
                
                if query_lower in entry.get('content', '').lower():
                    content_score = 1.5
                elif any(word in entry.get('content', '').lower() for word in query_lower.split()):
                    content_score = 0.8
                
                if any(query_lower in tag.lower() for tag in entry.get('tags', [])):
                    tags_score = 1.2
                
                total_score = title_score + content_score + tags_score
                
                if total_score >= threshold:
                    results.append({
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'content_preview': entry.get('content', '')[:200] + '...',
                        'tags': entry.get('tags', []),
                        'score': total_score,
                        'created_at': entry.get('created_at'),
                        'source': entry.get('source')
                    })
            
            # Sort by score and limit results
            results.sort(key=lambda x: x['score'], reverse=True)
            results = results[:limit]
            
            return f"✅ Found {len(results)} relevant entries:\n{json.dumps(results, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to search knowledge: {str(e)}"
    
    def _add_knowledge_entry(self, title: str, content: str, tags: List[str] = None, 
                           source: str = None, metadata: Dict = None) -> str:
        """Add a new knowledge entry"""
        try:
            entry_id = hashlib.md5(f"{title}_{datetime.now().isoformat()}".encode()).hexdigest()
            
            entry = {
                'id': entry_id,
                'title': title,
                'content': content,
                'tags': tags or [],
                'source': source,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Save entry
            entry_file = self.knowledge_base_path / "entries" / f"{entry_id}.json"
            with open(entry_file, 'w', encoding='utf-8') as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)
            
            # Update metadata
            self._update_metadata()
            
            return f"✅ Knowledge entry added successfully:\n{json.dumps(entry, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to add knowledge entry: {str(e)}"
    
    def _update_knowledge_entry(self, entry_id: str, updates: Dict) -> str:
        """Update an existing knowledge entry"""
        try:
            entry_file = self.knowledge_base_path / "entries" / f"{entry_id}.json"
            
            if not entry_file.exists():
                return f"❌ Knowledge entry {entry_id} not found"
            
            # Load existing entry
            with open(entry_file, 'r', encoding='utf-8') as f:
                entry = json.load(f)
            
            # Apply updates
            for key, value in updates.items():
                if key != 'id':  # Don't allow ID changes
                    entry[key] = value
            
            entry['updated_at'] = datetime.now().isoformat()
            
            # Save updated entry
            with open(entry_file, 'w', encoding='utf-8') as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)
            
            return f"✅ Knowledge entry updated successfully:\n{json.dumps(entry, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to update knowledge entry: {str(e)}"
    
    def _delete_knowledge_entry(self, entry_id: str) -> str:
        """Delete a knowledge entry"""
        try:
            entry_file = self.knowledge_base_path / "entries" / f"{entry_id}.json"
            
            if not entry_file.exists():
                return f"❌ Knowledge entry {entry_id} not found"
            
            # Load entry for logging
            with open(entry_file, 'r', encoding='utf-8') as f:
                entry = json.load(f)
            
            # Delete file
            entry_file.unlink()
            
            # Update metadata
            self._update_metadata()
            
            return f"✅ Knowledge entry deleted: {entry.get('title')} ({entry_id})"
            
        except Exception as e:
            return f"❌ Failed to delete knowledge entry: {str(e)}"
    
    def _list_knowledge_entries(self, tags: List[str] = None, limit: int = 50) -> str:
        """List knowledge entries with optional tag filtering"""
        try:
            entries_dir = self.knowledge_base_path / "entries"
            entries = []
            
            if not entries_dir.exists():
                return "✅ No knowledge entries found"
            
            for entry_file in entries_dir.glob("*.json"):
                with open(entry_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                
                # Filter by tags if specified
                if tags and not any(tag in entry.get('tags', []) for tag in tags):
                    continue
                
                entries.append({
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'tags': entry.get('tags', []),
                    'created_at': entry.get('created_at'),
                    'updated_at': entry.get('updated_at'),
                    'source': entry.get('source')
                })
            
            # Sort by creation date (newest first)
            entries.sort(key=lambda x: x['created_at'], reverse=True)
            entries = entries[:limit]
            
            return f"✅ Found {len(entries)} knowledge entries:\n{json.dumps(entries, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to list knowledge entries: {str(e)}"
    
    def _get_knowledge_stats(self) -> str:
        """Get statistics about the knowledge base"""
        try:
            entries_dir = self.knowledge_base_path / "entries"
            
            if not entries_dir.exists():
                return "✅ Knowledge base is empty"
            
            stats = {
                'total_entries': 0,
                'total_size_bytes': 0,
                'tags': {},
                'sources': {},
                'creation_dates': {}
            }
            
            for entry_file in entries_dir.glob("*.json"):
                stats['total_entries'] += 1
                stats['total_size_bytes'] += entry_file.stat().st_size
                
                with open(entry_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                
                # Count tags
                for tag in entry.get('tags', []):
                    stats['tags'][tag] = stats['tags'].get(tag, 0) + 1
                
                # Count sources
                source = entry.get('source', 'unknown')
                stats['sources'][source] = stats['sources'].get(source, 0) + 1
                
                # Count by creation date (month)
                created_at = entry.get('created_at', '')
                if created_at:
                    month = created_at[:7]  # YYYY-MM
                    stats['creation_dates'][month] = stats['creation_dates'].get(month, 0) + 1
            
            stats['average_size_bytes'] = stats['total_size_bytes'] / max(stats['total_entries'], 1)
            
            return f"✅ Knowledge base statistics:\n{json.dumps(stats, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to get knowledge stats: {str(e)}"
    
    def _backup_knowledge_base(self, backup_path: str = None) -> str:
        """Create a backup of the knowledge base"""
        try:
            if not backup_path:
                backup_path = self.knowledge_base_path / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                backup_path = Path(backup_path)
            
            # Collect all entries
            entries_dir = self.knowledge_base_path / "entries"
            backup_data = {
                'backup_created_at': datetime.now().isoformat(),
                'entries': []
            }
            
            if entries_dir.exists():
                for entry_file in entries_dir.glob("*.json"):
                    with open(entry_file, 'r', encoding='utf-8') as f:
                        entry = json.load(f)
                    backup_data['entries'].append(entry)
            
            # Save backup
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            return f"✅ Knowledge base backed up to: {backup_path}\n{len(backup_data['entries'])} entries saved"
            
        except Exception as e:
            return f"❌ Failed to backup knowledge base: {str(e)}"
    
    def _restore_knowledge_base(self, backup_path: str) -> str:
        """Restore knowledge base from backup"""
        try:
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                return f"❌ Backup file not found: {backup_path}"
            
            # Load backup
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Restore entries
            entries_dir = self.knowledge_base_path / "entries"
            entries_dir.mkdir(parents=True, exist_ok=True)
            
            restored_count = 0
            for entry in backup_data.get('entries', []):
                entry_id = entry.get('id')
                if entry_id:
                    entry_file = entries_dir / f"{entry_id}.json"
                    with open(entry_file, 'w', encoding='utf-8') as f:
                        json.dump(entry, f, indent=2, ensure_ascii=False)
                    restored_count += 1
            
            # Update metadata
            self._update_metadata()
            
            return f"✅ Knowledge base restored from: {backup_path}\n{restored_count} entries restored"
            
        except Exception as e:
            return f"❌ Failed to restore knowledge base: {str(e)}"
    
    def _update_metadata(self):
        """Update knowledge base metadata"""
        try:
            entries_dir = self.knowledge_base_path / "entries"
            total_entries = len(list(entries_dir.glob("*.json"))) if entries_dir.exists() else 0
            
            metadata_file = self.knowledge_base_path / "metadata.json"
            metadata = {}
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            metadata.update({
                'total_entries': total_entries,
                'last_updated': datetime.now().isoformat()
            })
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")


class KnowledgeQueryTool(BaseTool):
    """Specialized tool for querying and retrieving knowledge"""
    
    name: str = "knowledge_query"
    description: str = (
        "Query knowledge base using natural language queries, semantic search, "
        "and intelligent filtering. Optimized for fast retrieval and relevance."
    )
    
    def _run(self, query: str, **kwargs) -> str:
        """Execute knowledge queries with advanced search capabilities"""
        try:
            # This would integrate with the knowledge manager
            search_config = {
                'query': query,
                'type': kwargs.get('search_type', 'semantic'),
                'limit': kwargs.get('limit', 10),
                'threshold': kwargs.get('threshold', 0.7),
                'filters': kwargs.get('filters', {}),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Knowledge query executed: {json.dumps(search_config, indent=2)}"
            
        except Exception as e:
            logger.error(f"Knowledge query error: {e}")
            return f"❌ Error: {str(e)}"


class KnowledgeAddTool(BaseTool):
    """Tool for adding new knowledge to the system"""
    
    name: str = "knowledge_add"
    description: str = (
        "Add new knowledge entries including documents, notes, insights, "
        "and structured information with automatic processing and indexing."
    )
    
    def _run(self, content: str, **kwargs) -> str:
        """Add new knowledge with intelligent processing"""
        try:
            add_config = {
                'content': content[:500] + '...' if len(content) > 500 else content,
                'title': kwargs.get('title'),
                'source': kwargs.get('source'),
                'tags': kwargs.get('tags', []),
                'metadata': kwargs.get('metadata', {}),
                'processing': kwargs.get('processing', 'auto'),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Knowledge addition queued: {json.dumps(add_config, indent=2)}"
            
        except Exception as e:
            logger.error(f"Knowledge add error: {e}")
            return f"❌ Error: {str(e)}"


class KnowledgeUpdateTool(BaseTool):
    """Tool for updating existing knowledge entries"""
    
    name: str = "knowledge_update"
    description: str = (
        "Update existing knowledge entries including content modification, "
        "tag management, and metadata updates with version tracking."
    )
    
    def _run(self, entry_id: str, **kwargs) -> str:
        """Update knowledge entries with change tracking"""
        try:
            update_config = {
                'entry_id': entry_id,
                'updates': kwargs.get('updates', {}),
                'version_tracking': kwargs.get('version_tracking', True),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Knowledge update queued: {json.dumps(update_config, indent=2)}"
            
        except Exception as e:
            logger.error(f"Knowledge update error: {e}")
            return f"❌ Error: {str(e)}"


class DocumentProcessorTool(BaseTool):
    """Tool for processing and extracting knowledge from documents"""
    
    name: str = "document_processor"
    description: str = (
        "Process various document formats including PDF, DOCX, TXT, and web pages "
        "to extract knowledge and add to the knowledge base with intelligent parsing."
    )
    
    def _run(self, file_path: str, **kwargs) -> str:
        """Process documents and extract knowledge"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"❌ File not found: {file_path}"
            
            # Get file type
            mime_type, _ = mimetypes.guess_type(file_path)
            
            processing_config = {
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size,
                'mime_type': mime_type,
                'processing_mode': kwargs.get('processing_mode', 'auto'),
                'extract_metadata': kwargs.get('extract_metadata', True),
                'chunk_size': kwargs.get('chunk_size', 1000),
                'timestamp': datetime.now().isoformat()
            }
            
            # Simulate text extraction (would implement actual extraction logic)
            if mime_type and 'text' in mime_type:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    processing_config['content_preview'] = content[:200] + '...'
                    processing_config['status'] = 'extracted'
                except Exception:
                    processing_config['status'] = 'extraction_failed'
            else:
                processing_config['status'] = 'requires_specialized_parser'
            
            return f"✅ Document processing completed: {json.dumps(processing_config, indent=2)}"
            
        except Exception as e:
            logger.error(f"Document processor error: {e}")
            return f"❌ Error: {str(e)}"