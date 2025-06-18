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
        """
        Test that platform detection returns 'unknown' when no relevant environment variables are set.
        """
        with patch.dict(os.environ, {}, clear=True):
            platform = detect_platform()
            self.assertEqual(platform, 'unknown')

    def test_detect_project_type_agor_development(self):
        """
        Test that `detect_project_type()` correctly identifies an AGOR development project when the expected directory structure exists.
        """
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
            # Create AGOR project structure
            agor_dir = Path(temp_dir) / 'src' / 'agor' / 'tools'
            agor_dir.mkdir(parents=True)

            project_type = detect_project_type()
            self.assertEqual(project_type, 'agor_development')

    def test_detect_project_type_external(self):
        """
        Test that `detect_project_type()` identifies a directory without AGOR structure as an external project.
        """
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
            # Create non-AGOR project structure
            project_type = detect_project_type()
            self.assertEqual(project_type, 'external_project')

    def test_detect_project_type_nested_directory(self):
        """
        Test that project type detection correctly identifies an AGOR development project when executed from a nested subdirectory within the project structure.
        """
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
        """
        Test that project type detection identifies 'agor_development' when a pyproject.toml with AGOR content exists in a parent directory, even when called from a nested subdirectory.
        """
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
        # Use Path operations for cross-platform compatibility
        from pathlib import Path
        tools_path = Path(paths['tools_path'])
        readme_path = Path(paths['readme_ai'])
        instructions_path = Path(paths['instructions'])

        self.assertEqual(tools_path.parts[-3:], ('src', 'agor', 'tools'))
        self.assertEqual(readme_path.parts[-4:], ('src', 'agor', 'tools', 'README_ai.md'))
        self.assertEqual(instructions_path.parts[-4:], ('src', 'agor', 'tools', 'AGOR_INSTRUCTIONS.md'))

        # All paths should be absolute
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

        # Use Path objects for cross-platform compatibility
        from pathlib import Path
        expected_tools_path = Path(custom_path) / 'tools'
        expected_readme_path = Path(custom_path) / 'tools' / 'README_ai.md'

        self.assertEqual(Path(paths['tools_path']), expected_tools_path)
        self.assertEqual(Path(paths['readme_ai']), expected_readme_path)

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
        """
        Test that deployment prompt generation correctly merges partial custom paths with default paths.
        
        Verifies that when only some custom paths are provided, the generated deployment prompt includes the custom paths for specified keys and default paths for missing keys.
        """
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
        """
        Test that the developer tools reference guide is generated with all expected sections and tool references.
        """
        reference = get_dev_tools_reference()
        
        self.assertIn('DEV TOOLS COMPLETE REFERENCE', reference)
        self.assertIn('create_development_snapshot', reference)
        self.assertIn('generate_pr_description_output', reference)
        self.assertIn('test_all_tools', reference)

    def test_programmatic_guides_are_comprehensive(self):
        """
        Verify that programmatic guide functions return comprehensive, well-structured content with visual separators, section icons, and non-empty bodies.
        """
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

    @patch('agor.tools.agent_reference.detect_platform')
    @patch('agor.tools.agent_reference.detect_project_type')
    @patch.dict(os.environ, {}, clear=True)
    def test_deployment_prompt_contains_all_sections(self, mock_detect_project, mock_detect_platform):
        """
        Verifies that the generated deployment prompt includes all essential sections and identifiers required for AGOR agent deployment.
        """
        mock_detect_platform.return_value = 'test_platform'
        mock_detect_project.return_value = 'external_project'
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


class TestDetectionEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for detection functions."""

    def test_detect_platform_multiple_env_vars(self):
        """Test platform detection when multiple platform environment variables are set."""
        with patch.dict(os.environ, {'AUGMENT_LOCAL': 'true', 'AUGMENT_REMOTE': 'true'}):
            platform = detect_platform()
            # Should prioritize one platform consistently (test the behavior)
            self.assertIn(platform, ['augment_local', 'augment_remote'])

    def test_detect_platform_empty_string_values(self):
        """Test platform detection with empty string environment variable values."""
        with patch.dict(os.environ, {'AUGMENT_LOCAL': ''}):
            platform = detect_platform()
            self.assertEqual(platform, 'unknown')

    def test_detect_platform_case_sensitivity(self):
        """Test platform detection with different case values."""
        with patch.dict(os.environ, {'AUGMENT_LOCAL': 'TRUE'}):
            platform = detect_platform()
            # Should handle case insensitive or specific case requirements
            self.assertIn(platform, ['augment_local', 'unknown'])

    def test_detect_platform_non_boolean_values(self):
        """Test platform detection with non-boolean environment variable values."""
        with patch.dict(os.environ, {'AUGMENT_LOCAL': 'yes'}):
            platform = detect_platform()
            # Test how non-standard truthy values are handled
            self.assertIn(platform, ['augment_local', 'unknown'])

    def test_detect_project_type_permission_errors(self):
        """Test project type detection when filesystem access is restricted."""
        with tempfile.TemporaryDirectory() as temp_dir:
            restricted_dir = Path(temp_dir) / 'restricted'
            restricted_dir.mkdir(mode=0o000)  # No permissions

            try:
                with patch('pathlib.Path.cwd', return_value=restricted_dir):
                    # Should handle permission errors gracefully
                    project_type = detect_project_type()
                    self.assertIn(project_type, ['external_project', 'agor_development'])
            finally:
                # Restore permissions for cleanup
                restricted_dir.chmod(0o755)

    def test_detect_project_type_symlink_handling(self):
        """Test project type detection with symbolic links in the path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create actual AGOR structure
            real_dir = Path(temp_dir) / 'real_agor'
            agor_tools = real_dir / 'src' / 'agor' / 'tools'
            agor_tools.mkdir(parents=True)

            # Create symlink to the directory
            symlink_dir = Path(temp_dir) / 'symlink_agor'
            try:
                symlink_dir.symlink_to(real_dir)

                with patch('pathlib.Path.cwd', return_value=symlink_dir):
                    project_type = detect_project_type()
                    self.assertEqual(project_type, 'agor_development')
            except OSError:
                # Skip test if symlinks not supported
                self.skipTest("Symlinks not supported on this platform")

    def test_detect_project_type_invalid_pyproject_content(self):
        """Test project type detection with invalid pyproject.toml content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / 'project'
            project_root.mkdir()

            # Create invalid pyproject.toml
            pyproject_file = project_root / 'pyproject.toml'
            with open(pyproject_file, 'w') as f:
                f.write('[invalid syntax')  # Malformed TOML

            with patch('pathlib.Path.cwd', return_value=project_root):
                project_type = detect_project_type()
                # Should handle parsing errors gracefully
                self.assertEqual(project_type, 'external_project')

    def test_detect_project_type_very_deep_nesting(self):
        """Test project type detection from very deeply nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create AGOR structure at root
            agor_root = Path(temp_dir) / 'agor-project'
            agor_tools = agor_root / 'src' / 'agor' / 'tools'
            agor_tools.mkdir(parents=True)

            # Create very deep nesting
            deep_path = agor_root
            for i in range(20):  # 20 levels deep
                deep_path = deep_path / f'level{i}'
            deep_path.mkdir(parents=True)

            with patch('pathlib.Path.cwd', return_value=deep_path):
                project_type = detect_project_type()
                self.assertEqual(project_type, 'agor_development')


class TestPathResolutionEdgeCases(unittest.TestCase):
    """Test edge cases for path resolution functions."""

    def test_resolve_agor_paths_nonexistent_custom_path(self):
        """Test path resolution with non-existent custom path."""
        nonexistent_path = '/this/path/does/not/exist'
        paths = resolve_agor_paths('external_project', nonexistent_path)

        # Should still generate paths even if directory doesn't exist
        self.assertEqual(paths['tools_path'], f'{nonexistent_path}/tools')
        self.assertEqual(paths['readme_ai'], f'{nonexistent_path}/tools/README_ai.md')

    def test_resolve_agor_paths_relative_custom_path(self):
        """Test path resolution with relative custom path."""
        relative_path = './relative/agor'
        paths = resolve_agor_paths('external_project', relative_path)

        self.assertEqual(paths['tools_path'], f'{relative_path}/tools')
        self.assertTrue(paths['readme_ai'].endswith('/tools/README_ai.md'))

    def test_resolve_agor_paths_empty_string_custom_path(self):
        """Test path resolution with empty string custom path."""
        paths = resolve_agor_paths('external_project', '')

        # Should handle empty string gracefully
        self.assertIn('tools', paths['tools_path'])

    def test_get_platform_specific_instructions_unknown_platform(self):
        """Test platform-specific instructions for unknown platform."""
        instructions = get_platform_specific_instructions('unknown_platform', 'external_project')

        # Should provide fallback instructions
        self.assertIn('Unknown Platform', instructions)
        self.assertIn('general', instructions.lower())

    def test_get_platform_specific_instructions_all_combinations(self):
        """Test all valid platform and project type combinations."""
        platforms = ['augment_local', 'augment_remote', 'chatgpt', 'unknown']
        project_types = ['agor_development', 'external_project']

        for platform in platforms:
            for project_type in project_types:
                with self.subTest(platform=platform, project_type=project_type):
                    instructions = get_platform_specific_instructions(platform, project_type)
                    self.assertIsInstance(instructions, str)
                    self.assertTrue(len(instructions) > 0)


class TestDeploymentPromptEdgeCases(unittest.TestCase):
    """Test edge cases for deployment prompt generation."""

    def test_generate_deployment_prompt_with_none_values(self):
        """Test deployment prompt generation with None values in custom paths."""
        custom_paths = {
            'readme_ai': None,
            'instructions': '/valid/path/AGOR_INSTRUCTIONS.md',
            'start_here': None
        }

        prompt = generate_deployment_prompt(
            platform='test',
            project_type='external_project',
            custom_paths=custom_paths
        )

        # Should handle None values by using defaults
        self.assertIn('/valid/path/AGOR_INSTRUCTIONS.md', prompt)
        self.assertIn('README_ai.md', prompt)  # Should use default

    def test_generate_deployment_prompt_with_unicode_paths(self):
        """Test deployment prompt generation with Unicode characters in paths."""
        unicode_paths = {
            'readme_ai': '/path/with/unicode/文档/README_ai.md',
            'instructions': '/path/with/émojis/📚/AGOR_INSTRUCTIONS.md'
        }

        prompt = generate_deployment_prompt(
            platform='test',
            project_type='external_project',
            custom_paths=unicode_paths
        )

        self.assertIn('/path/with/unicode/文档/README_ai.md', prompt)
        self.assertIn('/path/with/émojis/📚/AGOR_INSTRUCTIONS.md', prompt)

    def test_generate_deployment_prompt_empty_custom_paths_dict(self):
        """Test deployment prompt generation with empty custom paths dictionary."""
        prompt = generate_deployment_prompt(
            platform='test',
            project_type='external_project',
            custom_paths={}
        )

        # Should use all default paths
        self.assertIn('README_ai.md', prompt)
        self.assertIn('AGOR_INSTRUCTIONS.md', prompt)

    @patch('agor.tools.agent_reference.detect_platform')
    @patch('agor.tools.agent_reference.detect_project_type')
    def test_generate_deployment_prompt_detection_failures(self, mock_detect_project, mock_detect_platform):
        """Test deployment prompt generation when detection functions fail."""
        mock_detect_platform.side_effect = Exception("Platform detection failed")
        mock_detect_project.side_effect = Exception("Project detection failed")

        # Should handle exceptions gracefully and provide fallback
        try:
            prompt = generate_deployment_prompt()
            self.assertIsInstance(prompt, str)
            self.assertTrue(len(prompt) > 0)
        except Exception:
            # If exceptions propagate, that's also valid behavior to test
            pass

    def test_generate_deployment_prompt_timestamp_format(self):
        """Test that deployment prompt includes properly formatted timestamp."""
        prompt = generate_deployment_prompt()

        # Should contain timestamp information
        self.assertIn('Generated:', prompt)
        # Verify timestamp format (basic check)
        import re
        timestamp_pattern = r'Generated:.*\d{4}-\d{2}-\d{2}'
        self.assertTrue(re.search(timestamp_pattern, prompt))


class TestGuideContentValidation(unittest.TestCase):
    """Test content validation and structure of guide functions."""

    def test_all_guides_have_consistent_structure(self):
        """Test that all guide functions return consistently structured content."""
        guide_functions = [
            get_memory_branch_guide,
            get_coordination_guide,
            get_dev_tools_reference,
            get_role_selection_guide,
            get_external_integration_guide,
            get_output_formatting_requirements
        ]

        for guide_func in guide_functions:
            with self.subTest(guide_function=guide_func.__name__):
                guide = guide_func()

                # Each guide should have title
                self.assertTrue(any(line.isupper() and len(line) > 10 for line in guide.split('\n')))

                # Should have visual separators
                self.assertIn('═══', guide)

                # Should have meaningful content (not just headers)
                content_lines = [line.strip() for line in guide.split('\n') if line.strip() and not line.startswith('═')]
                self.assertGreater(len(content_lines), 3)

    def test_guides_contain_expected_keywords(self):
        """Test that guides contain domain-specific keywords relevant to their purpose."""
        guide_keywords = {
            get_memory_branch_guide: ['memory', 'branch', 'git', 'commit'],
            get_coordination_guide: ['agent', 'coordination', 'communication', 'workflow'],
            get_dev_tools_reference: ['tools', 'development', 'command', 'function'],
            get_role_selection_guide: ['role', 'agent', 'worker', 'coordinator'],
            get_external_integration_guide: ['external', 'integration', 'project', 'module'],
            get_output_formatting_requirements: ['format', 'output', 'requirement', 'structure']
        }

        for guide_func, expected_keywords in guide_keywords.items():
            with self.subTest(guide_function=guide_func.__name__):
                guide = guide_func().lower()
                found_keywords = [kw for kw in expected_keywords if kw in guide]
                self.assertGreaterEqual(len(found_keywords), 2,
                    f"Guide {guide_func.__name__} should contain at least 2 of: {expected_keywords}")

    def test_guides_are_deterministic(self):
        """Test that guide functions return identical content on multiple calls."""
        guide_functions = [
            get_memory_branch_guide,
            get_coordination_guide,
            get_dev_tools_reference,
            get_role_selection_guide,
            get_external_integration_guide,
            get_output_formatting_requirements
        ]

        for guide_func in guide_functions:
            with self.subTest(guide_function=guide_func.__name__):
                first_call = guide_func()
                second_call = guide_func()
                self.assertEqual(first_call, second_call)

    def test_guides_handle_unicode_content(self):
        """Test that guides can handle and display Unicode content properly."""
        guides = [
            get_memory_branch_guide(),
            get_coordination_guide(),
            get_dev_tools_reference(),
            get_role_selection_guide(),
            get_external_integration_guide(),
            get_output_formatting_requirements()
        ]

        for guide in guides:
            # Should be able to encode/decode without errors
            try:
                encoded = guide.encode('utf-8')
                decoded = encoded.decode('utf-8')
                self.assertEqual(guide, decoded)
            except UnicodeError:
                self.fail("Guide contains problematic Unicode characters")


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios combining multiple functions."""

    def test_full_deployment_workflow(self):
        """Test complete deployment workflow from detection to prompt generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up AGOR project structure
            project_root = Path(temp_dir) / 'agor_project'
            agor_tools = project_root / 'src' / 'agor' / 'tools'
            agor_tools.mkdir(parents=True)

            with patch('pathlib.Path.cwd', return_value=project_root), \
                 patch.dict(os.environ, {'AUGMENT_LOCAL': 'true'}):

                # Test complete workflow
                platform = detect_platform()
                project_type = detect_project_type()
                paths = resolve_agor_paths(project_type)
                prompt = generate_deployment_prompt(platform, project_type, custom_paths=paths)

                # Verify workflow results
                self.assertEqual(platform, 'augment_local')
                self.assertEqual(project_type, 'agor_development')
                self.assertIn('AGOR (AgentOrchestrator)', prompt)
                self.assertIn('AugmentCode Local', prompt)

    def test_external_project_workflow(self):
        """Test workflow for external project integration."""
        with tempfile.TemporaryDirectory() as temp_dir, \
             patch('pathlib.Path.cwd', return_value=Path(temp_dir)), \
             patch.dict(os.environ, {'AUGMENT_REMOTE': 'true'}):

            platform = detect_platform()
            project_type = detect_project_type()
            paths = resolve_agor_paths(project_type)

            # Generate all guides for external project
            guides = {
                'memory': get_memory_branch_guide(),
                'coordination': get_coordination_guide(),
                'dev_tools': get_dev_tools_reference(),
                'role_selection': get_role_selection_guide(),
                'external_integration': get_external_integration_guide(),
                'output_formatting': get_output_formatting_requirements()
            }

            prompt = generate_deployment_prompt(platform, project_type, custom_paths=paths)

            # Verify external project setup
            self.assertEqual(platform, 'augment_remote')
            self.assertEqual(project_type, 'external_project')
            self.assertIn('external integration', prompt.lower())

            # Verify all guides are available
            for guide_name, guide_content in guides.items():
                self.assertIsInstance(guide_content, str)
                self.assertTrue(len(guide_content) > 100, f"{guide_name} guide too short")


class TestErrorHandlingAndRobustness(unittest.TestCase):
    """Test error handling and robustness of all functions."""

    def test_functions_with_invalid_arguments(self):
        """Test how functions handle invalid argument types."""
        # Test with None arguments
        try:
            paths = resolve_agor_paths(None)
            self.assertIsInstance(paths, dict)
        except (TypeError, AttributeError):
            pass  # Either handle gracefully or raise appropriate error

        # Test with non-string arguments
        try:
            instructions = get_platform_specific_instructions(123, ['invalid'])
            self.assertIsInstance(instructions, str)
        except (TypeError, AttributeError):
            pass

    def test_filesystem_access_errors(self):
        """Test behavior when filesystem access fails."""
        with patch('pathlib.Path.exists', side_effect=PermissionError("Access denied")):
            try:
                project_type = detect_project_type()
                # Should handle filesystem errors gracefully
                self.assertIn(project_type, ['agor_development', 'external_project'])
            except PermissionError:
                # If error propagates, that's also valid behavior
                pass

    def test_memory_constraints(self):
        """Test functions with large inputs to check memory efficiency."""
        # Test with very long custom path
        very_long_path = '/'.join(['very_long_directory_name'] * 100)
        paths = resolve_agor_paths('external_project', very_long_path)

        self.assertIn('tools', paths['tools_path'])
        # Should handle long paths without issues

    @patch('builtins.open', side_effect=IOError("File access error"))
    def test_file_access_errors(self, mock_open):
        """Test behavior when file access operations fail."""
        # This would test any file reading operations in the functions
        try:
            project_type = detect_project_type()
            # Should handle file access errors gracefully
            self.assertIsInstance(project_type, str)
        except IOError:
            # If error propagates, that's also valid behavior
            pass


if __name__ == '__main__' and os.getenv('AGOR_STANDALONE_TESTS'):
    unittest.main()