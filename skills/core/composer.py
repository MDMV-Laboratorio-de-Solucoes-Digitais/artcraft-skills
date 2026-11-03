"""Skill composition utilities."""

from typing import Dict, Any, List
from .base_skill import BaseSkill, SkillResult


class SkillComposer:
    """Compose multiple skills into workflows."""
    
    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
    
    def register(self, skill: BaseSkill):
        """Register a skill."""
        self.skills[skill.name] = skill
    
    def compose(self, skill_sequence: List[str], inputs: Dict[str, Any]) -> SkillResult:
        """Compose skills in sequence."""
        current_data = inputs
        
        for skill_name in skill_sequence:
            if skill_name not in self.skills:
                return SkillResult(success=False, error=f"Skill {skill_name} not found")
            
            skill = self.skills[skill_name]
            if not skill.validate_inputs(current_data):
                return SkillResult(success=False, error=f"Invalid inputs for {skill_name}")
            
            result = skill.execute(current_data)
            if not result.success:
                return result
            
            current_data = result.data if isinstance(result.data, dict) else {'result': result.data}
        
        return SkillResult(success=True, data=current_data)
    
    def compose_parallel(self, skill_names: List[str], inputs: Dict[str, Any]) -> List[SkillResult]:
        """Compose skills in parallel."""
        results = []
        for skill_name in skill_names:
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                results.append(skill.execute(inputs))
            else:
                results.append(SkillResult(success=False, error=f"Skill {skill_name} not found"))
        return results
