"""
Tests for the main module
"""

import unittest
from discotify.main import main


class TestMain(unittest.TestCase):
    """Test cases for the main module"""
    
    def test_main(self):
        """Test main function with demo action"""
        
        # Mock sys.argv to simulate command line arguments
        test_args = ['discotify', '--action', 'demo', '--name', 'TestDemo']
    #end
#end


if __name__ == '__main__':
    unittest.main()
#end
