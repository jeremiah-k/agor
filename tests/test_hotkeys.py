"""
Comprehensive unit tests for hotkeys module.
Tests HotkeyManager class and global hotkey functions using pytest framework.
"""

import pytest
from unittest.mock import Mock, patch
import threading
import time
import sys
import os

# Add the source directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agor.tools.hotkeys import (
    HotkeyManager,
    register_hotkey,
    unregister_hotkey,
    get_registered_hotkeys,
    clear_all_hotkeys,
    start_hotkey_manager,
    stop_hotkey_manager,
    global_hotkey_manager,
)

@pytest.fixture
def hotkey_manager():
    """Fixture providing a clean HotkeyManager instance for each test."""
    manager = HotkeyManager()
    yield manager
    # Cleanup any registered hotkeys after each test
    manager.stop()

@pytest.fixture
def mock_keyboard():
    """Fixture providing a mocked keyboard module."""
    with patch('agor.tools.hotkeys.keyboard') as mock_kb:
        yield mock_kb

@pytest.fixture
def mock_logger():
    """Fixture providing a mocked logger."""
    with patch('agor.tools.hotkeys.logger') as mock_log:
        yield mock_log

@pytest.fixture(autouse=True)
def reset_global_manager():
    """Automatically reset global manager state before each test."""
    global_hotkey_manager.stop()
    yield
    global_hotkey_manager.stop()

class TestHotkeyManagerInit:
    """Test HotkeyManager initialization and basic properties."""
    
    def test_init_creates_empty_manager(self):
        """Test that new HotkeyManager starts with empty state."""
        manager = HotkeyManager()
        assert manager.get_registered_keys() == []
        assert manager.is_active() is False
        assert manager._hotkeys == {}
    
    def test_init_with_keyboard_unavailable(self):
        """Test initialization when keyboard module is unavailable."""
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', False):
            manager = HotkeyManager()
            assert manager.is_active() is False
    
    def test_thread_safety_initialization(self):
        """Test that multiple managers can be created concurrently."""
        managers = []
        
        def create_manager():
            managers.append(HotkeyManager())
        
        threads = [threading.Thread(target=create_manager) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        assert len(managers) == 10
        for manager in managers:
            assert isinstance(manager, HotkeyManager)

class TestHotkeyRegistration:
    """Test hotkey registration functionality."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_single_key_hotkey(self, hotkey_manager, mock_keyboard):
        """Test registering a simple single-key hotkey."""
        callback = Mock()
        result = hotkey_manager.register('a', callback)
        
        assert result is True
        assert 'a' in hotkey_manager.get_registered_keys()
        mock_keyboard.add_hotkey.assert_called_once()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_combination_hotkey(self, hotkey_manager, mock_keyboard):
        """Test registering hotkey combinations like ctrl+c."""
        callback = Mock()
        result = hotkey_manager.register('ctrl+c', callback)
        
        assert result is True
        assert 'ctrl+c' in hotkey_manager.get_registered_keys()
        mock_keyboard.add_hotkey.assert_called_once_with('ctrl+c', mock_keyboard.add_hotkey.call_args[0][1])
    
    def test_register_hotkey_with_arguments(self, hotkey_manager, mock_keyboard):
        """Test registering hotkey with callback arguments."""
        callback = Mock()
        args = ('arg1', 'arg2')
        kwargs = {'key': 'value'}
        
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            result = hotkey_manager.register('f1', callback, *args, **kwargs)
        
        assert result is True
        assert 'f1' in hotkey_manager.get_registered_keys()
    
    def test_register_hotkey_empty_string(self, hotkey_manager):
        """Test registration fails with empty hotkey string."""
        callback = Mock()
        
        with pytest.raises(ValueError, match="Hotkey cannot be empty"):
            hotkey_manager.register('', callback)
    
    def test_register_hotkey_whitespace_only(self, hotkey_manager):
        """Test registration fails with whitespace-only hotkey."""
        callback = Mock()
        
        with pytest.raises(ValueError, match="Hotkey cannot be empty"):
            hotkey_manager.register('   ', callback)
    
    def test_register_hotkey_none_callback(self, hotkey_manager):
        """Test registration fails when callback is not callable."""
        with pytest.raises(TypeError, match="Callback must be callable"):
            hotkey_manager.register('a', None)
    
    def test_register_hotkey_non_callable_callback(self, hotkey_manager):
        """Test registration fails when callback is not callable."""
        with pytest.raises(TypeError, match="Callback must be callable"):
            hotkey_manager.register('a', "not_callable")
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_duplicate_hotkey(self, hotkey_manager, mock_keyboard):
        """Test behavior when registering the same hotkey twice."""
        callback1 = Mock()
        callback2 = Mock()
        
        hotkey_manager.register('a', callback1)
        
        with pytest.raises(ValueError, match="Hotkey 'a' already registered"):
            hotkey_manager.register('a', callback2)
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_case_normalization(self, hotkey_manager, mock_keyboard):
        """Test that hotkey registration normalizes case."""
        callback1 = Mock()
        callback2 = Mock()
        
        hotkey_manager.register('A', callback1)
        
        with pytest.raises(ValueError, match="already registered"):
            hotkey_manager.register('a', callback2)
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', False)
    def test_register_keyboard_unavailable(self, hotkey_manager, mock_logger):
        """Test registration when keyboard module is unavailable."""
        callback = Mock()
        result = hotkey_manager.register('a', callback)
        
        assert result is False
        mock_logger.warning.assert_called()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_keyboard_exception(self, hotkey_manager, mock_keyboard, mock_logger):
        """Test registration handles keyboard module exceptions."""
        callback = Mock()
        mock_keyboard.add_hotkey.side_effect = Exception("Keyboard error")
        
        result = hotkey_manager.register('a', callback)
        
        assert result is False
        mock_logger.error.assert_called()

class TestHotkeyUnregistration:
    """Test hotkey unregistration functionality."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_unregister_existing_hotkey(self, hotkey_manager, mock_keyboard):
        """Test unregistering an existing hotkey."""
        callback = Mock()
        hotkey_manager.register('a', callback)
        
        result = hotkey_manager.unregister('a')
        
        assert result is True
        assert 'a' not in hotkey_manager.get_registered_keys()
        mock_keyboard.remove_hotkey.assert_called_once_with('a')
    
    def test_unregister_nonexistent_hotkey(self, hotkey_manager):
        """Test unregistering a hotkey that doesn't exist."""
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            result = hotkey_manager.unregister('nonexistent')
        
        assert result is False
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', False)
    def test_unregister_keyboard_unavailable(self, hotkey_manager):
        """Test unregistration when keyboard module is unavailable."""
        result = hotkey_manager.unregister('a')
        assert result is False
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_unregister_keyboard_exception(self, hotkey_manager, mock_keyboard, mock_logger):
        """Test unregistration handles keyboard module exceptions."""
        callback = Mock()
        hotkey_manager.register('a', callback)
        mock_keyboard.remove_hotkey.side_effect = Exception("Remove error")
        
        result = hotkey_manager.unregister('a')
        
        assert result is False
        mock_logger.error.assert_called()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_clear_all_hotkeys(self, hotkey_manager, mock_keyboard):
        """Test clearing all registered hotkeys."""
        callback1, callback2 = Mock(), Mock()
        hotkey_manager.register('a', callback1)
        hotkey_manager.register('b', callback2)
        
        hotkey_manager.clear_all()
        
        assert len(hotkey_manager.get_registered_keys()) == 0
        assert mock_keyboard.remove_hotkey.call_count == 2
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', False)
    def test_clear_all_keyboard_unavailable(self, hotkey_manager):
        """Test clear_all when keyboard module is unavailable."""
        # Should not raise exception
        hotkey_manager.clear_all()
        assert len(hotkey_manager.get_registered_keys()) == 0
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_clear_all_with_exceptions(self, hotkey_manager, mock_keyboard, mock_logger):
        """Test clear_all handles exceptions during removal."""
        callback = Mock()
        hotkey_manager.register('a', callback)
        mock_keyboard.remove_hotkey.side_effect = Exception("Clear error")
        
        hotkey_manager.clear_all()
        
        assert len(hotkey_manager.get_registered_keys()) == 0
        mock_logger.error.assert_called()

class TestHotkeyManagerLifecycle:
    """Test hotkey manager start/stop and state management."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_start_manager(self, hotkey_manager, mock_logger):
        """Test starting the hotkey manager."""
        result = hotkey_manager.start()
        
        assert result is True
        assert hotkey_manager.is_active() is True
        mock_logger.info.assert_called_with("Hotkey manager started")
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', False)
    def test_start_manager_keyboard_unavailable(self, hotkey_manager, mock_logger):
        """Test starting manager when keyboard is unavailable."""
        result = hotkey_manager.start()
        
        assert result is False
        assert hotkey_manager.is_active() is False
        mock_logger.warning.assert_called()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_stop_manager(self, hotkey_manager, mock_keyboard, mock_logger):
        """Test stopping the hotkey manager."""
        callback = Mock()
        hotkey_manager.start()
        hotkey_manager.register('a', callback)
        
        hotkey_manager.stop()
        
        assert hotkey_manager.is_active() is False
        assert len(hotkey_manager.get_registered_keys()) == 0
        mock_logger.info.assert_called_with("Hotkey manager stopped")
    
    def test_is_active_states(self, hotkey_manager):
        """Test is_active returns correct states."""
        assert hotkey_manager.is_active() is False
        
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            hotkey_manager.start()
            assert hotkey_manager.is_active() is True
            
            hotkey_manager.stop()
            assert hotkey_manager.is_active() is False
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_context_manager_usage(self, mock_keyboard, mock_logger):
        """Test hotkey manager as context manager."""
        callback = Mock()
        
        with HotkeyManager() as manager:
            assert manager.is_active() is True
            manager.register('a', callback)
            assert 'a' in manager.get_registered_keys()
        
        # After context exit, should be stopped and cleared
        assert manager.is_active() is False
        assert len(manager.get_registered_keys()) == 0
    
    def test_context_manager_exception_handling(self, mock_keyboard):
        """Test context manager handles exceptions properly."""
        callback = Mock()
        
        try:
            with HotkeyManager() as manager:
                manager.register('a', callback)
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Manager should still be properly cleaned up
        assert manager.is_active() is False

class TestCallbackExecution:
    """Test hotkey callback execution and error handling."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_callback_execution(self, hotkey_manager, mock_keyboard):
        """Test that callbacks are properly wrapped and can be executed."""
        callback = Mock()
        hotkey_manager.register('a', callback)
        
        # Get the wrapped callback that was registered
        args, kwargs = mock_keyboard.add_hotkey.call_args
        wrapped_callback = args[1]
        
        # Execute the wrapped callback
        wrapped_callback()
        
        callback.assert_called_once()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_callback_with_arguments(self, hotkey_manager, mock_keyboard):
        """Test callback execution with arguments."""
        callback = Mock()
        args = ('test_arg',)
        kwargs = {'key': 'value'}
        
        hotkey_manager.register('ctrl+s', callback, *args, **kwargs)
        
        # Get and execute wrapped callback
        call_args, call_kwargs = mock_keyboard.add_hotkey.call_args
        wrapped_callback = call_args[1]
        wrapped_callback()
        
        callback.assert_called_once_with('test_arg', key='value')
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_callback_exception_handling(self, hotkey_manager, mock_keyboard, mock_logger):
        """Test that exceptions in callbacks are handled gracefully."""
        def failing_callback():
            raise Exception("Test callback exception")
        
        hotkey_manager.register('a', failing_callback)
        
        # Get and execute wrapped callback
        args, kwargs = mock_keyboard.add_hotkey.call_args
        wrapped_callback = args[1]
        
        # Should not raise exception, but log it
        wrapped_callback()
        mock_logger.error.assert_called()
        
        # Verify error message contains relevant information
        error_call = mock_logger.error.call_args[0][0]
        assert "Error in hotkey callback" in error_call
        assert "a" in error_call

class TestGlobalHotkeyFunctions:
    """Test global hotkey management functions."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_register_hotkey_global(self, mock_keyboard):
        """Test global register_hotkey function."""
        callback = Mock()
        result = register_hotkey('a', callback)
        
        assert result is True
        assert 'a' in get_registered_hotkeys()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_unregister_hotkey_global(self, mock_keyboard):
        """Test global unregister_hotkey function."""
        callback = Mock()
        register_hotkey('a', callback)
        
        result = unregister_hotkey('a')
        
        assert result is True
        assert 'a' not in get_registered_hotkeys()
    
    def test_get_registered_hotkeys_global(self):
        """Test global get_registered_hotkeys function."""
        hotkeys = get_registered_hotkeys()
        assert isinstance(hotkeys, list)
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_clear_all_hotkeys_global(self, mock_keyboard):
        """Test global clear_all_hotkeys function."""
        callback = Mock()
        register_hotkey('a', callback)
        register_hotkey('b', callback)
        
        clear_all_hotkeys()
        
        assert len(get_registered_hotkeys()) == 0
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_start_hotkey_manager_global(self, mock_logger):
        """Test global start_hotkey_manager function."""
        result = start_hotkey_manager()
        assert result is True
    
    def test_stop_hotkey_manager_global(self, mock_logger):
        """Test global stop_hotkey_manager function."""
        # Should not raise exception
        stop_hotkey_manager()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_global_manager_isolation(self, mock_keyboard):
        """Test that global manager operations don't interfere with instance managers."""
        callback = Mock()
        instance_manager = HotkeyManager()
        
        # Register on global manager
        register_hotkey('global_key', callback)
        
        # Register on instance manager
        instance_manager.register('instance_key', callback)
        
        # Verify isolation
        assert 'global_key' in get_registered_hotkeys()
        assert 'global_key' not in instance_manager.get_registered_keys()
        assert 'instance_key' in instance_manager.get_registered_keys()
        assert 'instance_key' not in get_registered_hotkeys()
        
        # Cleanup
        instance_manager.stop()

class TestThreadSafety:
    """Test thread safety of hotkey operations."""
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_concurrent_registration(self, mock_keyboard):
        """Test concurrent hotkey registration is thread-safe."""
        manager = HotkeyManager()
        callback = Mock()
        results = []
        
        def register_hotkeys(start_idx):
            for i in range(start_idx, start_idx + 10):
                try:
                    result = manager.register(f'key_{i}', callback)
                    results.append(result)
                except Exception:
                    results.append(False)
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=register_hotkeys, args=(i * 10,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All registrations should succeed
        assert all(results)
        registered_keys = manager.get_registered_keys()
        assert len(registered_keys) == 50
        
        manager.stop()
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_concurrent_registration_and_removal(self, mock_keyboard):
        """Test concurrent registration and removal operations."""
        manager = HotkeyManager()
        callback = Mock()
        
        def register_and_remove():
            for i in range(10):
                try:
                    manager.register(f'temp_key_{threading.current_thread().ident}_{i}', callback)
                    time.sleep(0.001)  # Small delay to encourage race conditions
                    manager.unregister(f'temp_key_{threading.current_thread().ident}_{i}')
                except Exception:
                    pass  # Expected due to race conditions
        
        threads = [threading.Thread(target=register_and_remove) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Manager should be in consistent state
        assert isinstance(manager.get_registered_keys(), list)
        manager.stop()

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_special_key_combinations(self, hotkey_manager, mock_keyboard):
        """Test registration with special key combinations."""
        callback = Mock()
        special_keys = [
            'ctrl+alt+shift+f1',
            'ctrl+shift+tab',
            'alt+space',
            'ctrl+break',
            'shift+f12'
        ]
        
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            for key in special_keys:
                result = hotkey_manager.register(key, callback)
                assert result is True, f"Failed to register special key: {key}"
                hotkey_manager.unregister(key)
    
    def test_unicode_hotkeys(self, hotkey_manager):
        """Test handling of unicode characters in hotkeys."""
        callback = Mock()
        unicode_keys = ['ñ', 'ü', '€']
        
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            with patch('agor.tools.hotkeys.keyboard'):
                for key in unicode_keys:
                    try:
                        result = hotkey_manager.register(key, callback)
                        # Should either succeed or handle gracefully
                        assert isinstance(result, bool)
                    except Exception as e:
                        # Should be a reasonable exception, not a crash
                        assert isinstance(e, (ValueError, TypeError))
    
    @patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True)
    def test_maximum_hotkeys_stress_test(self, hotkey_manager, mock_keyboard):
        """Test behavior with many registered hotkeys."""
        callback = Mock()
        
        # Register many hotkeys
        for i in range(100):
            result = hotkey_manager.register(f'f{i % 12 + 1}+{i}', callback)
            assert result is True
        
        assert len(hotkey_manager.get_registered_keys()) == 100
        
        # Clear all should work
        hotkey_manager.clear_all()
        assert len(hotkey_manager.get_registered_keys()) == 0
    
    def test_very_long_hotkey_string(self, hotkey_manager):
        """Test behavior with very long hotkey strings."""
        callback = Mock()
        very_long_key = 'ctrl+alt+shift+' + '+'.join([f'key{i}' for i in range(50)])
        
        with patch('agor.tools.hotkeys.KEYBOARD_AVAILABLE', True):
            with patch('agor.tools.hotkeys.keyboard'):
                # Should handle gracefully, either succeed or fail with appropriate error
                try:
                    result = hotkey_manager.register(very_long_key, callback)
                    assert isinstance(result, bool)
                except Exception as e:
                    assert isinstance(e, (ValueError, TypeError))