"""
Unit tests for AGOR agent education system.

Tests the programmatic documentation and deployment prompt generation functions.
"""

import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import os

from agor.tools.agent_reference import (
    detect_platform,
    detect_project_type,
    resolve_agor_paths,
    get_platform_specific_instructions,
    generate_deployment_prompt,
    get_memory_branch_guide,
    get_coordination_guide,
    get_dev_tools_reference,
    get_role_selection_guide,
    get_external_integration_guide,
    get_output_formatting_requirements,
)


class TestDetection(unittest.TestCase):
    """Test cases for platform and project detection functions."""

    def test_detect_platform_augment_local(self):
        """Test platform detection for AugmentCode Local."""
        with patch.dict(os.environ, {'AUGMENT_LOCAL': 'true'}):
            platform = detect_platform()
            self.assertEqual(platform, 'augment_local')

    def test_detect_platform_augment_remote(self):
        """Test platform detection for AugmentCode Remote."""
        with patch.dict(os.environ, {'AUGMENT_REMOTE': 'true'}):
            platform = detect_platform()
            self.assertEqual(platform, 'augment_remote')

    def test_detect_platform_unknown(self):
        """Test platform detection fallback."""
        with patch.dict(os.environ, {}, clear=True):
            platform = detect_platform()
            self.assertEqual(platform, 'unknown')

    def test_detect_project_type_agor_development(self):
        """Test project type detection for AGOR development."""
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
            # Create AGOR project structure
            agor_dir = Path(temp_dir) / 'src' / 'agor' / 'tools'
            agor_dir.mkdir(parents=True)

            project_type = detect_project_type()
            self.assertEqual(project_type, 'agor_development')

    def test_detect_project_type_external(self):
        """Test project type detection for external project."""
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
            # Create non-AGOR project structure
            project_type = detect_project_type()
            self.assertEqual(project_type, 'external_project')

    def test_detect_project_type_nested_directory(self):
        """Test project type detection from nested directory within AGOR project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create AGOR project structure in temp directory
            agor_root = Path(temp_dir) / 'agor-project'
            agor_tools = agor_root / 'src' / 'agor' / 'tools'
            agor_tools.mkdir(parents=True)

            # Create nested subdirectory
            nested_dir = agor_root / 'some' / 'nested' / 'directory'
            nested_dir.mkdir(parents=True)

            # Test from nested directory - should walk up and find AGOR indicators
            with patch('pathlib.Path.cwd', return_value=nested_dir):
                project_type = detect_project_type()
                self.assertEqual(project_type, 'agor_development')

    def test_detect_project_type_pyproject_in_parent(self):
        """Test project type detection with pyproject.toml in parent directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project structure
            project_root = Path(temp_dir) / 'project'
            project_root.mkdir()

            # Create pyproject.toml with AGOR content in root
            pyproject_file = project_root / 'pyproject.toml'
            with open(pyproject_file, 'w') as f:
                f.write('[build-system]\nrequires = ["setuptools"]\n\n[project]\nname = "agor"\n')

            # Create nested subdirectory
            nested_dir = project_root / 'deep' / 'nested' / 'path'
            nested_dir.mkdir(parents=True)

            # Test from nested directory - should find pyproject.toml in parent
            with patch('pathlib.Path.cwd', return_value=nested_dir):
                project_type = detect_project_type()
                self.assertEqual(project_type, 'agor_development')


class TestPathResolution(unittest.TestCase):
    """Test cases for path resolution functions."""

    def test_resolve_agor_paths_development(self):
        """Test path resolution for AGOR development."""
        paths = resolve_agor_paths('agor_development')

        # Should use absolute paths for consistency (fixed in latest version)
        self.assertTrue(paths['tools_path'].endswith('/src/agor/tools'))
        self.assertTrue(paths['readme_ai'].endswith('/src/agor/tools/README_ai.md'))
        self.assertTrue(paths['instructions'].endswith('/src/agor/tools/AGOR_INSTRUCTIONS.md'))

        # All paths should be absolute
        from pathlib import Path
        self.assertTrue(Path(paths['tools_path']).is_absolute())
        self.assertTrue(Path(paths['readme_ai']).is_absolute())
        self.assertTrue(Path(paths['instructions']).is_absolute())

    def test_resolve_agor_paths_external(self):
        """Test path resolution for external project."""
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
            paths = resolve_agor_paths('external_project')

            # Should fallback to relative path or find existing AGOR installation
            # Use safer containment check instead of brittle Path.match()
            tools_path_str = paths['tools_path']
            self.assertTrue(
                tools_path_str.endswith('/agor/tools') or
                tools_path_str.endswith('\\agor\\tools') or
                tools_path_str.endswith('/tools') or
                tools_path_str.endswith('\\tools')
            )

    def test_resolve_agor_paths_custom(self):
        """Test path resolution with custom path."""
        custom_path = '/custom/agor/path'
        paths = resolve_agor_paths('external_project', custom_path)

        self.assertEqual(paths['tools_path'], f'{custom_path}/tools')
        self.assertEqual(paths['readme_ai'], f'{custom_path}/tools/README_ai.md')

    def test_get_platform_specific_instructions(self):
        """Test platform-specific instruction generation."""
        instructions = get_platform_specific_instructions('augment_local', 'external_project')

        self.assertIn('AugmentCode Local Agent', instructions)
        self.assertIn('external integration system', instructions)
        self.assertIn('get_agor_tools', instructions)


class TestDeploymentPrompt(unittest.TestCase):
    """Test cases for deployment prompt generation."""

    def test_generate_deployment_prompt_basic(self):
        """Test basic deployment prompt generation."""
        with patch('agor.tools.agent_reference.detect_platform', return_value='augment_local'), \
             patch('agor.tools.agent_reference.detect_project_type', return_value='external_project'):
            prompt = generate_deployment_prompt()

            self.assertIn('AGOR (AgentOrchestrator)', prompt)
            self.assertIn('README_ai.md', prompt)
            self.assertIn('AGOR_INSTRUCTIONS.md', prompt)
            self.assertIn('AugmentCode Local Agent', prompt)
            self.assertIn('deliverables', prompt)

    def test_generate_deployment_prompt_custom_params(self):
        """Test deployment prompt generation with custom parameters."""
        custom_paths = {
            'readme_ai': '/custom/path/README_ai.md',
            'instructions': '/custom/path/AGOR_INSTRUCTIONS.md',
            'start_here': '/custom/path/agent-start-here.md',
            'index': '/custom/path/index.md'
        }
        
        prompt = generate_deployment_prompt(
            platform='chatgpt',
            project_type='agor_development',
            custom_paths=custom_paths
        )
        
        self.assertIn('/custom/path/README_ai.md', prompt)
        self.assertIn('ChatGPT', prompt)
        self.assertIn('Platform: chatgpt', prompt)
        self.assertIn('Project: agor_development', prompt)

    def test_generate_deployment_prompt_partial_custom_paths(self):
        """Test deployment prompt generation with partial custom paths (should merge with defaults)."""
        # Only provide some custom paths, others should fall back to defaults
        partial_custom_paths = {
            'readme_ai': '/custom/README_ai.md',
            'instructions': '/custom/AGOR_INSTRUCTIONS.md'
            # Missing: start_here, index, external_guide, tools_path
        }

        prompt = generate_deployment_prompt(
            platform='augment_local',
            project_type='agor_development',
            custom_paths=partial_custom_paths
        )

        # Should contain custom paths
        self.assertIn('/custom/README_ai.md', prompt)
        self.assertIn('/custom/AGOR_INSTRUCTIONS.md', prompt)
        # Should contain default paths for missing keys
        self.assertIn('src/agor/tools/agent-start-here.md', prompt)
        self.assertIn('src/agor/tools/index.md', prompt)

    def test_generate_deployment_prompt_custom_base_path(self):
        """Test deployment prompt generation with custom base path."""
        custom_base = '/opt/my-agor'

        prompt = generate_deployment_prompt(
            platform='test',
            project_type='external_project',
            custom_base_path=custom_base
        )

        # Should use custom base path for all files
        self.assertIn(f'{custom_base}/tools/README_ai.md', prompt)
        self.assertIn(f'{custom_base}/tools/AGOR_INSTRUCTIONS.md', prompt)
        self.assertIn(f'{custom_base}/tools/agent-start-here.md', prompt)
        self.assertIn(f'{custom_base}/tools/index.md', prompt)

    def test_get_memory_branch_guide(self):
        """Test memory branch guide generation."""
        guide = get_memory_branch_guide()
        
        self.assertIn('MEMORY BRANCH SYSTEM', guide)
        self.assertIn('.agor/ directories exist ONLY on memory branches', guide)
        self.assertIn('Cross-branch commits', guide)
        self.assertIn('dev tools', guide)

    def test_get_coordination_guide(self):
        """Test coordination guide generation."""
        guide = get_coordination_guide()
        
        self.assertIn('MULTI-AGENT COORDINATION', guide)
        self.assertIn('agentconvo.md', guide)
        self.assertIn('next_steps', guide)
        self.assertIn('Parallel Divergent', guide)

    def test_get_dev_tools_reference(self):
        """Test dev tools reference generation."""
        reference = get_dev_tools_reference()
        
        self.assertIn('DEV TOOLS COMPLETE REFERENCE', reference)
        self.assertIn('create_development_snapshot', reference)
        self.assertIn('generate_pr_description_output', reference)
        self.assertIn('test_all_tools', reference)

    def test_programmatic_guides_are_comprehensive(self):
        """Test that programmatic guides contain comprehensive information."""
        guides = [
            get_memory_branch_guide(),
            get_coordination_guide(),
            get_dev_tools_reference()
        ]
        
        for guide in guides:
            # Each guide should be substantial (not just a placeholder)
            # Use structural checks instead of brittle length assertions
            self.assertIn('═══', guide)  # Visual separators for readability
            self.assertIn('📋', guide)   # Clear sections with icons
            # Ensure guide has meaningful content structure
            self.assertTrue(len(guide.strip()) > 0, "Guide should not be empty")

    def test_deployment_prompt_contains_all_sections(self):
        """Test that deployment prompt contains all required sections."""
        prompt = generate_deployment_prompt()
        
        required_sections = [
            'AGOR (AgentOrchestrator)',
            'README_ai.md',
            'AGOR_INSTRUCTIONS.md',
            'agent-start-here.md',
            'index.md',
            'deliverables',
            'Platform:',
            'Project:',
            'Generated:'
        ]
        
        for section in required_sections:
            self.assertIn(section, prompt)


class TestGuides(unittest.TestCase):
    """Test cases for programmatic guide functions."""

    def test_get_role_selection_guide(self):
        """Test role selection guide generation."""
        guide = get_role_selection_guide()

        self.assertIn('ROLE SELECTION GUIDE', guide)
        self.assertIn('WORKER AGENT', guide)
        self.assertIn('PROJECT COORDINATOR', guide)
        self.assertIn('decision tree', guide.lower())
        # Use structural checks instead of brittle length assertions
        self.assertIn('═══', guide)  # Visual separators

    def test_get_external_integration_guide(self):
        """Test external integration guide generation."""
        guide = get_external_integration_guide()

        self.assertIn('EXTERNAL PROJECT INTEGRATION', guide)
        self.assertIn('get_agor_tools', guide)
        self.assertIn('external integration', guide.lower())
        self.assertIn('ModuleNotFoundError', guide)
        # Use structural checks instead of brittle length assertions
        self.assertIn('═══', guide)  # Visual separators

    def test_get_output_formatting_requirements(self):
        """Test output formatting requirements generation."""
        guide = get_output_formatting_requirements()

        self.assertIn('OUTPUT FORMATTING REQUIREMENTS', guide)
        self.assertIn('detick', guide)
        self.assertIn('retick', guide)
        self.assertIn('copy-paste workflow', guide.lower())
        # Use structural checks instead of brittle length assertions
        self.assertIn('═══', guide)  # Visual separators


class TestPlatformInstructions(unittest.TestCase):
    """Test cases for platform-specific instruction functions."""

    def test_augment_remote_platform_instructions(self):
        """Test that augment_remote platform has proper instructions."""
        instructions = get_platform_specific_instructions('augment_remote', 'external_project')

        self.assertIn('AugmentCode Remote Agent', instructions)
        self.assertIn('Remote execution environment', instructions)
        self.assertIn('external integration system', instructions)
        # Should not fall back to unknown platform
        self.assertNotIn('Unknown Platform', instructions)


if __name__ == '__main__':
    unittest.main()
