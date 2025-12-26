"""
Intent Parser Agent - Parse natural language and route to appropriate agent.

This agent is the front-line that understands user requests and routes them
to the appropriate specialized agent.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .security import (
    sanitize_spec_id,
    sanitize_query,
    InvalidInputError
)


class IntentType(Enum):
    """Types of user intents"""
    STATUS_QUERY = "status_query"
    ORCHESTRATION = "orchestration"
    BUG_FIX = "bug_fix"
    VALIDATION = "validation"
    MODIFICATION = "modification"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Parsed user intent"""
    type: IntentType
    spec_id: Optional[str]
    target_agent: str
    context: Dict[str, Any]
    confidence: float
    original_input: str


class IntentParserAgent:
    """
    Intent Parser Agent - Parse natural language and route requests.
    
    Capabilities:
    - Parse natural language input
    - Identify user intent
    - Extract entities (spec ID, error message, etc.)
    - Route to appropriate agent
    - Provide context to target agent
    """
    
    def __init__(self):
        # Intent patterns (keywords)
        self.patterns = {
            IntentType.STATUS_QUERY: [
                "งานถึงไหน", "เหลืออะไร", "ต้องทำอะไรต่อ", "มีปัญหาไหม", "เมื่อไหร่เสร็จ",
                "progress", "status", "what's left", "remaining", "next step", "eta",
                "สถานะ", "ความคืบหน้า"
            ],
            IntentType.ORCHESTRATION: [
                "ทำต่อ", "เริ่ม", "run", "start", "continue", "next", "พัฒนา", "ดำเนินการ"
            ],
            IntentType.BUG_FIX: [
                "แก้", "bug", "error", "fix", "ผิดพลาด", "ไม่ทำงาน", "broken", "issue"
            ],
            IntentType.VALIDATION: [
                "ตรวจสอบ", "validate", "check", "verify", "ผิด", "ถูกต้อง", "correct"
            ],
            IntentType.MODIFICATION: [
                "เปลี่ยน", "เพิ่ม", "ลบ", "แก้ไข", "ปรับปรุง",
                "change", "add", "remove", "modify", "update", "refactor"
            ]
        }
        
        # Agent mapping
        self.agent_mapping = {
            IntentType.STATUS_QUERY: "status",
            IntentType.ORCHESTRATION: "orchestrator",
            IntentType.BUG_FIX: "bug_fixer",
            IntentType.VALIDATION: "validation",
            IntentType.MODIFICATION: "spec_modifier",
            IntentType.UNKNOWN: "orchestrator"  # Default to orchestrator
        }
    
    def parse(self, user_input: str) -> Intent:
        """
        Parse user input and extract intent.
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Intent object with parsed information
            
        Raises:
            InvalidInputError: If input is invalid
        """
        # Sanitize input
        try:
            user_input = sanitize_query(user_input, max_length=1000)
        except InvalidInputError as e:
            # Return UNKNOWN intent if input is invalid
            return Intent(
                type=IntentType.UNKNOWN,
                spec_id=None,
                target_agent="orchestrator",
                context={"error": str(e)},
                confidence=0.0,
                original_input=user_input[:100]  # Truncate for safety
            )
        
        """
        Parse user input and return intent.
        
        Args:
            user_input: Natural language input from user
        
        Returns:
            Intent with type, target agent, and context
        """
        # Extract spec ID
        spec_id = self._extract_spec_id(user_input)
        
        # Identify intent type
        intent_type = self._identify_intent(user_input)
        
        # Extract context based on intent type
        context = self._extract_context(user_input, intent_type)
        
        # Calculate confidence
        confidence = self._calculate_confidence(user_input, intent_type)
        
        # Determine target agent
        target_agent = self.agent_mapping[intent_type]
        
        return Intent(
            type=intent_type,
            spec_id=spec_id,
            target_agent=target_agent,
            context=context,
            confidence=confidence,
            original_input=user_input
        )
    
    def _extract_spec_id(self, text: str) -> Optional[str]:
        """Extract spec ID from text"""
        import re
        
        # Pattern: spec-xxx-yyy-zzz
        pattern = r'(spec-[a-z0-9_-]+)'
        match = re.search(pattern, text.lower())
        
        if match:
            spec_id = match.group(1)
            # Validate extracted spec_id
            try:
                return sanitize_spec_id(spec_id)
            except InvalidInputError:
                return None
        
        # Pattern: just the ID part (e.g., "core-001")
        pattern = r'([a-z]+-\d{3})'
        match = re.search(pattern, text.lower())
        
        if match:
            spec_id = f"spec-{match.group(1)}"
            try:
                return sanitize_spec_id(spec_id)
            except InvalidInputError:
                return None
        
        return None
    
    def _identify_intent(self, text: str) -> IntentType:
        """Identify intent type from text"""
        text_lower = text.lower()
        
        # Count matches for each intent type
        scores = {}
        for intent_type, keywords in self.patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[intent_type] = score
        
        # Get intent with highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return IntentType.UNKNOWN
    
    def _extract_context(self, text: str, intent_type: IntentType) -> Dict[str, Any]:
        """Extract context based on intent type"""
        context = {}
        
        if intent_type == IntentType.STATUS_QUERY:
            # Extract question
            context["question"] = text
        
        elif intent_type == IntentType.ORCHESTRATION:
            # Extract command (run, start, continue)
            if "run" in text.lower() or "เริ่ม" in text.lower():
                context["action"] = "run"
            elif "continue" in text.lower() or "ทำต่อ" in text.lower():
                context["action"] = "continue"
            else:
                context["action"] = "run"
        
        elif intent_type == IntentType.BUG_FIX:
            # Extract error message
            import re
            error_pattern = r'error[:\s]+(.+?)(?:\n|$)'
            match = re.search(error_pattern, text, re.IGNORECASE)
            if match:
                context["error_message"] = match.group(1).strip()
            else:
                context["error_message"] = text
        
        elif intent_type == IntentType.VALIDATION:
            # Extract target (implementation, api, ui, etc.)
            targets = ["implementation", "api", "ui", "data model", "tests"]
            for target in targets:
                if target in text.lower():
                    context["target"] = target
                    break
            else:
                context["target"] = "implementation"  # Default
        
        elif intent_type == IntentType.MODIFICATION:
            # Extract change description
            context["change_description"] = text
            
            # Identify modification type
            if "เพิ่ม" in text.lower() or "add" in text.lower():
                context["modification_type"] = "add"
            elif "ลบ" in text.lower() or "remove" in text.lower():
                context["modification_type"] = "remove"
            elif "เปลี่ยน" in text.lower() or "change" in text.lower():
                context["modification_type"] = "change"
            else:
                context["modification_type"] = "modify"
        
        return context
    
    def _calculate_confidence(self, text: str, intent_type: IntentType) -> float:
        """Calculate confidence score"""
        if intent_type == IntentType.UNKNOWN:
            return 0.0
        
        # Count keyword matches
        keywords = self.patterns[intent_type]
        matches = sum(1 for keyword in keywords if keyword in text.lower())
        
        # Confidence based on matches
        if matches >= 3:
            return 0.95
        elif matches == 2:
            return 0.80
        elif matches == 1:
            return 0.60
        else:
            return 0.30
    
    def format_intent(self, intent: Intent) -> str:
        """Format intent as human-readable text"""
        lines = [
            f"# Parsed Intent",
            f"",
            f"**Type:** {intent.type.value}",
            f"**Target Agent:** {intent.target_agent}",
            f"**Confidence:** {intent.confidence:.0%}",
            f""
        ]
        
        if intent.spec_id:
            lines.append(f"**Spec ID:** {intent.spec_id}")
            lines.append(f"")
        
        if intent.context:
            lines.append(f"**Context:**")
            for key, value in intent.context.items():
                lines.append(f"- {key}: {value}")
            lines.append(f"")
        
        lines.append(f"**Original Input:** {intent.original_input}")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Create agent
    agent = IntentParserAgent()
    
    print("Intent Parser Agent Test")
    print("=" * 50)
    print()
    
    # Test cases
    test_cases = [
        "spec-core-001-authentication งานถึงไหนแล้ว?",
        "เริ่มพัฒนา spec-core-002-authorization",
        "แก้ bug ใน spec-core-001 error: undefined variable",
        "ตรวจสอบ implementation ของ spec-core-001",
        "เพิ่มฟังก์ชัน password reset ใน spec-core-001",
        "run spec-core-001",
        "เหลืออะไรบ้างใน spec-core-002?",
        "ทำอะไรต่อ?"
    ]
    
    for test_input in test_cases:
        print(f"Input: {test_input}")
        print("-" * 50)
        
        intent = agent.parse(test_input)
        print(agent.format_intent(intent))
        print()
