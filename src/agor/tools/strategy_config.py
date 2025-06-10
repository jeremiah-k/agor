"""
Strategy Configuration System for AGOR 0.5.1

This module provides a config-driven approach to strategy logic, replacing
hardcoded patterns and handlers with flexible configuration.

Key Features:
- YAML-based strategy definitions
- Pluggable role handlers
- Configurable action generators
- Extensible pattern matching
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


@dataclass
class StrategyPattern:
    """Configuration for detecting strategy types."""

    name: str
    detection_patterns: List[str]
    parser_class: str
    default_phase: str = "active"


@dataclass
class RoleConfig:
    """Configuration for agent roles within strategies."""

    role_name: str
    conditions: Dict[str, Any]
    actions: List[str]
    status_indicators: List[str] = field(default_factory=list)


@dataclass
class StrategyConfig:
    """Complete configuration for a strategy type."""

    strategy_type: str
    patterns: StrategyPattern
    roles: List[RoleConfig]
    phase_transitions: Dict[str, str] = field(default_factory=dict)
    custom_handlers: Dict[str, str] = field(default_factory=dict)


class StrategyConfigManager:
    """
    Manages strategy configurations and provides config-driven coordination logic.

    This replaces the hardcoded strategy patterns and role handlers in agent_coordination.py
    with a flexible, configuration-based approach.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the strategy configuration manager.

        Args:
            config_path: Path to strategy configuration file. Defaults to built-in config.
        """
        self.config_path = (
            config_path or Path(__file__).parent / "strategy_configs.json"
        )
        self.strategies: Dict[str, StrategyConfig] = {}
        self.pattern_handlers: Dict[str, Callable] = {}
        self._load_configurations()
        self._register_default_handlers()

    def _validate_config_structure(self, config_data: Dict[str, Any]) -> bool:
        """
        Validate that the configuration data has the expected structure.

        Args:
            config_data: Configuration data to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(config_data, dict):
            return False

        if "strategies" not in config_data:
            return False

        strategies = config_data["strategies"]
        if not isinstance(strategies, dict):
            return False

        # Validate each strategy has required structure
        for _strategy_name, strategy_data in strategies.items():
            if not isinstance(strategy_data, dict):
                return False

            # Check for required keys
            if "patterns" not in strategy_data:
                return False

            patterns = strategy_data["patterns"]
            if not isinstance(patterns, dict):
                return False

            # Check required pattern fields
            required_pattern_fields = ["name", "detection_patterns", "parser_class"]
            for field in required_pattern_fields:
                if field not in patterns:
                    return False

            # Validate roles structure if present
            if "roles" in strategy_data:
                roles = strategy_data["roles"]
                if not isinstance(roles, list):
                    return False

                for role in roles:
                    if not isinstance(role, dict):
                        return False
                    if (
                        "role_name" not in role
                        or "conditions" not in role
                        or "actions" not in role
                    ):
                        return False

        return True

    def _load_configurations(self) -> None:
        """Load strategy configurations from file or create defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    config_data = json.load(f)

                # Validate configuration structure
                if not self._validate_config_structure(config_data):
                    print("⚠️ Invalid configuration structure, using defaults")
                    self._create_default_configurations()
                    return

                self._parse_configurations(config_data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Error loading strategy config: {e}")
                self._create_default_configurations()
        else:
            self._create_default_configurations()

    def _parse_configurations(self, config_data: Dict[str, Any]) -> None:
        """Parse configuration data into StrategyConfig objects."""
        for strategy_name, strategy_data in config_data.get("strategies", {}).items():
            # Parse pattern configuration
            pattern_data = strategy_data.get("patterns", {})
            patterns = StrategyPattern(
                name=pattern_data.get("name", strategy_name),
                detection_patterns=pattern_data.get("detection_patterns", []),
                parser_class=pattern_data.get("parser_class", "default"),
                default_phase=pattern_data.get("default_phase", "active"),
            )

            # Parse role configurations
            roles = []
            for role_data in strategy_data.get("roles", []):
                role = RoleConfig(
                    role_name=role_data.get("role_name", "participant"),
                    conditions=role_data.get("conditions", {}),
                    actions=role_data.get("actions", []),
                    status_indicators=role_data.get("status_indicators", []),
                )
                roles.append(role)

            # Create strategy configuration
            strategy_config = StrategyConfig(
                strategy_type=strategy_name,
                patterns=patterns,
                roles=roles,
                phase_transitions=strategy_data.get("phase_transitions", {}),
                custom_handlers=strategy_data.get("custom_handlers", {}),
            )

            self.strategies[strategy_name] = strategy_config

    def _create_default_configurations(self) -> None:
        """Create default strategy configurations."""
        default_config = {
            "strategies": {
                "parallel_divergent": {
                    "patterns": {
                        "name": "Parallel Divergent Strategy",
                        "detection_patterns": ["Parallel Divergent Strategy"],
                        "parser_class": "parallel_divergent_parser",
                        "default_phase": "setup",
                    },
                    "roles": [
                        {
                            "role_name": "divergent_worker",
                            "conditions": {
                                "phase": "divergent",
                                "has_assignment": True,
                            },
                            "actions": [
                                "Post to agentconvo.md: '{agent_id}: [timestamp] - CLAIMING ASSIGNMENT'",
                                "Create branch: git checkout -b solution-{agent_id}",
                                "Initialize memory file: .agor/{agent_id}-memory.md",
                                "Plan your unique approach to the problem",
                                "Begin independent implementation (NO coordination with other agents)",
                            ],
                            "status_indicators": [
                                "ready_to_claim",
                                "available",
                                "working",
                            ],
                        },
                        {
                            "role_name": "reviewer",
                            "conditions": {"phase": "convergent"},
                            "actions": [
                                "Review all agent solutions on their branches",
                                "Use review template in strategy-active.md",
                                "Post reviews to agentconvo.md",
                                "Identify strengths and weaknesses",
                                "Propose synthesis approach",
                            ],
                        },
                        {
                            "role_name": "synthesizer",
                            "conditions": {"phase": "synthesis"},
                            "actions": [
                                "Combine best approaches from all solutions",
                                "Create unified implementation",
                                "Test integrated solution",
                                "Document final approach",
                            ],
                        },
                    ],
                    "phase_transitions": {
                        "setup": "divergent",
                        "divergent": "convergent",
                        "convergent": "synthesis",
                        "synthesis": "complete",
                    },
                },
                "pipeline": {
                    "patterns": {
                        "name": "Pipeline Strategy",
                        "detection_patterns": ["Pipeline Strategy"],
                        "parser_class": "pipeline_parser",
                    },
                    "roles": [
                        {
                            "role_name": "stage_worker",
                            "conditions": {"stage_available": True},
                            "actions": [
                                "Post to agentconvo.md: '[agent-id]: [timestamp] - CLAIMING STAGE {stage_num}: {stage_name}'",
                                "Create working branch: git checkout -b stage-{stage_num}-{stage_name}",
                                "Read stage instructions in strategy-active.md",
                                "Complete stage deliverables",
                                "Create snapshot document for next stage",
                            ],
                        },
                        {
                            "role_name": "observer",
                            "conditions": {"stage_claimed": True},
                            "actions": [
                                "Monitor current stage progress in agentconvo.md",
                                "Prepare for next stage if applicable",
                                "Review upcoming stage requirements",
                            ],
                        },
                    ],
                },
                "swarm": {
                    "patterns": {
                        "name": "Swarm Strategy",
                        "detection_patterns": ["Swarm Strategy"],
                        "parser_class": "swarm_parser",
                    },
                    "roles": [
                        {
                            "role_name": "task_worker",
                            "conditions": {"available_tasks": "> 0"},
                            "actions": [
                                "Check available tasks: cat .agor/task-queue.json",
                                "Pick a task that matches your skills",
                                "Edit task-queue.json to claim the task (status: in_progress, assigned_to: your_id)",
                                "Post to agentconvo.md: '[agent-id]: [timestamp] - CLAIMED TASK [N]: [description]'",
                                "Begin task work independently",
                            ],
                        },
                        {
                            "role_name": "helper",
                            "conditions": {
                                "available_tasks": "= 0",
                                "in_progress_tasks": "> 0",
                            },
                            "actions": [
                                "Check if any agents need help in agentconvo.md",
                                "Look for completed tasks to verify",
                                "Wait for new tasks to become available",
                            ],
                        },
                    ],
                },
            }
        }

        # Save default configuration
        # Ensure parent directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(default_config, f, indent=2)

        # Parse the default configuration
        self._parse_configurations(default_config)

    def _register_default_handlers(self) -> None:
        """Register default pattern handlers."""
        self.pattern_handlers.update(
            {
                "parallel_divergent_parser": self._parse_parallel_divergent,
                "pipeline_parser": self._parse_pipeline,
                "swarm_parser": self._parse_swarm,
                "default": self._parse_generic,
            }
        )

    def detect_strategy(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Detect active strategy using configured patterns.

        Args:
            content: Strategy file content to analyze

        Returns:
            Dictionary containing strategy information, or None if no strategy detected
        """
        for _strategy_type, config in self.strategies.items():
            for pattern in config.patterns.detection_patterns:
                if pattern in content:
                    parser_class = config.patterns.parser_class
                    parser = self.pattern_handlers.get(
                        parser_class, self.pattern_handlers["default"]
                    )
                    return parser(content, config)

        return None

    def get_role_for_agent(
        self,
        strategy_info: Dict[str, Any],
        agent_id: Optional[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determine agent role using configured role conditions.

        Args:
            strategy_info: Information about the current strategy
            agent_id: Optional agent identifier
            context: Additional context for role determination

        Returns:
            Dictionary containing role information
        """
        strategy_type = strategy_info.get("type")
        config = self.strategies.get(strategy_type)

        if not config:
            return {
                "role": "participant",
                "message": f"Unknown strategy: {strategy_type}",
            }

        # Evaluate role conditions
        for role_config in config.roles:
            if self._evaluate_conditions(
                role_config.conditions, strategy_info, context
            ):
                return {
                    "role": role_config.role_name,
                    "actions": role_config.actions,
                    "message": f"Assigned role: {role_config.role_name}",
                    "status": self._determine_status(role_config, context),
                }

        return {"role": "participant", "message": "No specific role assigned"}

    def _evaluate_conditions(
        self,
        conditions: Dict[str, Any],
        strategy_info: Dict[str, Any],
        context: Dict[str, Any],
    ) -> bool:
        """Evaluate role assignment conditions."""
        for condition_key, condition_value in conditions.items():
            if condition_key == "phase":
                if strategy_info.get("phase") != condition_value:
                    return False
            elif condition_key == "has_assignment":
                # Custom logic for assignment checking
                if not context.get("has_assignment", False):
                    return False
            elif condition_key == "stage_available":
                if not context.get("stage_available", False):
                    return False
            elif condition_key == "available_tasks":
                available = context.get("available_tasks", 0)
                if not self._evaluate_numeric_condition(available, condition_value):
                    return False
            # Add more condition types as needed

        return True

    def _evaluate_numeric_condition(self, value: int, condition: str) -> bool:
        """Evaluate numeric conditions like '> 0', '= 0', etc."""
        if condition.startswith("> "):
            return value > int(condition[2:])
        elif condition.startswith("= "):
            return value == int(condition[2:])
        elif condition.startswith("< "):
            return value < int(condition[2:])
        return False

    def _determine_status(
        self, role_config: RoleConfig, context: Dict[str, Any]
    ) -> str:
        """Determine role status based on context."""
        # Default status determination logic
        if context.get("claimed", False):
            return "working"
        elif context.get("available", True):
            return "available"
        else:
            return "waiting"

    # Parser methods (simplified versions of the original hardcoded parsers)
    def _parse_parallel_divergent(
        self, content: str, config: StrategyConfig
    ) -> Dict[str, Any]:
        """Parse Parallel Divergent strategy using configuration."""
        task = self._extract_task_from_content(content)
        phase = self._extract_pd_phase(content)

        return {
            "type": "parallel_divergent",
            "phase": phase,
            "task": task,
            "config": config,
        }

    def _parse_pipeline(self, content: str, config: StrategyConfig) -> Dict[str, Any]:
        """Parse Pipeline strategy using configuration."""
        task = self._extract_task_from_content(content)
        current_stage = self._extract_current_stage(content)

        return {
            "type": "pipeline",
            "phase": "active",
            "task": task,
            "current_stage": current_stage,
            "config": config,
        }

    def _parse_swarm(self, content: str, config: StrategyConfig) -> Dict[str, Any]:
        """Parse Swarm strategy using configuration."""
        task = self._extract_task_from_content(content)

        return {"type": "swarm", "phase": "active", "task": task, "config": config}

    def _parse_generic(self, content: str, config: StrategyConfig) -> Dict[str, Any]:
        """Generic parser for unknown strategy types."""
        task = self._extract_task_from_content(content)

        return {
            "type": config.strategy_type,
            "phase": config.patterns.default_phase,
            "task": task,
            "config": config,
        }

    def _extract_task_from_content(self, content: str) -> str:
        """Extract task description from strategy content."""
        task_match = re.search(r"### Task: (.+)", content)
        return task_match.group(1) if task_match else "Unknown task"

    def _extract_pd_phase(self, content: str) -> str:
        """Extract current phase from Parallel Divergent strategy content."""
        phase_patterns = {
            "Phase 1 - Divergent Execution (ACTIVE)": "divergent",
            "Phase 2 - Convergent Review (ACTIVE)": "convergent",
            "Phase 3 - Synthesis (ACTIVE)": "synthesis",
        }

        for pattern, phase in phase_patterns.items():
            if pattern in content:
                return phase
        return "setup"

    def _extract_current_stage(self, content: str) -> Dict[str, Any]:
        """Extract current stage from Pipeline strategy content."""
        current_stage_match = re.search(
            r"### Status: Stage (\d+) - ([^(]+) \(ACTIVE\)", content
        )
        if current_stage_match:
            return {
                "number": int(current_stage_match.group(1)),
                "name": current_stage_match.group(2).strip(),
            }
        return {"number": 1, "name": "Unknown"}
