import os
import json
import pytest
from config_values import ConfigValues
from unittest.mock import patch, mock_open

class TestConfigValues:
    def test_default_values(self):
        config = ConfigValues()
        assert config.blur_factor == 50
        assert config.num_windows == 3

    def test_blur_factor_validation(self):
        config = ConfigValues()
        
        # Test valid values
        config.blur_factor = 0
        assert config.blur_factor == 0
        config.blur_factor = 100
        assert config.blur_factor == 100
        
        # Test invalid values
        with pytest.raises(TypeError):
            config.blur_factor = "50"
        with pytest.raises(ValueError):
            config.blur_factor = -1
        with pytest.raises(ValueError):
            config.blur_factor = 101

    def test_num_windows_validation(self):
        config = ConfigValues()
        
        # Test valid values
        config.num_windows = 0
        assert config.num_windows == 0
        config.num_windows = 6
        assert config.num_windows == 6
        
        # Test invalid values
        with pytest.raises(TypeError):
            config.num_windows = "3"
        with pytest.raises(ValueError):
            config.num_windows = -1
        with pytest.raises(ValueError):
            config.num_windows = 7

    @patch('os.path.isfile')
    def test_save_config(self, mock_isfile):
        mock_isfile.return_value = False
        mock_file = mock_open()
        
        with patch('builtins.open', mock_file):
            config = ConfigValues()
            config.blur_factor = 75
            config.num_windows = 4
            config.save()
            
            # Verify file was opened for writing
            mock_file.assert_called_once_with(config._filename, 'w')
            
            # Verify correct JSON was written
            handle = mock_file()
            expected_json = {'blur_factor': 75, 'num_windows': 4}
            written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
            assert json.loads(written_data) == expected_json

    @patch('os.path.isfile')
    def test_load_config(self, mock_isfile):
        mock_isfile.return_value = True
        test_config = {'blur_factor': 25, 'num_windows': 2}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(test_config))):
            config = ConfigValues()
            assert config.blur_factor == 25
            assert config.num_windows == 2

    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_directory_creation(self, mock_mkdir, mock_exists):
        mock_exists.return_value = False
        ConfigValues()
        mock_mkdir.assert_called_once()

    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_no_directory_creation_if_exists(self, mock_mkdir, mock_exists):
        mock_exists.return_value = True
        ConfigValues()
        mock_mkdir.assert_not_called()
