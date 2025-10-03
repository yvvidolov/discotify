"""
Unit tests for the Discotify class
"""

import unittest
from pathlib import Path
import threading
import socket
import time

from discotify import Discotify

class TestDiscotify(unittest.TestCase):
    """Test cases for the Discotify class"""
    
    def test_init(self):
        """Test Discotify initialization"""
        dis = Discotify()
        self.assertNotEqual(str(dis.get_config_path()), "")
    #end
    
    def test_constructor_args(self):
        """Test Discotify Constructor"""
        dis = Discotify(tag='my_tag', mentions=['thunder_trlr'], channels='notifications', username="bot", no_config_file=True)
        dis = Discotify(tag='my_tag', mentions='thunder_trlr', channels=['notifications', 'main'], custom_config_file='./config.json')
        self.assertEqual(Path(dis.get_config_path()), Path('./config.json'))
    #end
    
    def test_add_remove_temporal(self):
        """Test if we can add and remove aliases without creating a config file"""
        dis = Discotify(no_config_file=True, custom_config_file='./config.json')
        
        dis.user_add('asd', '123')
        dis.user_add('tyu', '456')
        dis.user_add('poq', '789')
        dis.user_add('rei', '000')
        dis.user_add('bau', '111')
        
        removed = 0
        removed += dis.user_remove(user_id='rei', alias='rei')
        removed += dis.user_remove(user_id='111')
        removed += dis.user_remove(alias='tyu')
        
        users = dis.get_users_alias()
        self.assertTrue(len(users) == 2, f'User count {len(users)}')
        self.assertEqual(removed, 3, f'Removed == {removed}')
        
        dis.hook_add('asd', '123')
        dis.hook_add('tyu', '456')
        dis.hook_add('poq', '789')
        dis.hook_add('rei', '000')
        dis.hook_add('bau', '111')
        
        removed = 0
        removed += dis.hook_remove(hook_url='rei', alias='rei')
        removed += dis.hook_remove(hook_url='111')
        removed += dis.hook_remove(alias='tyu')
        
        hooks = dis.get_hooks_alias()
        self.assertTrue(len(hooks) == 2, f'Hook count {len(hooks)}')
        self.assertEqual(removed, 3, f'Removed == {removed}')
        
        self.assertFalse(Path(dis.get_config_path()).exists())
    #end
    
    def test_config_file(self):
        """Test reading and writing to a config file and a new Discotify session"""
        config_path = Path('./config_KjjVdoD1h7hXa35zxASsd.json')
        
        self.assertFalse(config_path.exists())
        
        dis = Discotify(custom_config_file=str(config_path))
        dis.user_add('asd', '123')
        dis.user_add('bom', '456')
        dis.user_remove(alias='bom')
        dis.hook_add('rei', '000')
        dis.hook_add('awq', '222')
        dis.hook_remove(hook_url='222')
        self.assertFalse(dis.user_remove(user_id='invalid'))
        self.assertFalse(dis.user_remove(alias='invalid'))
        del dis
        
        self.assertTrue(config_path.exists())
        
        dis = Discotify(no_config_file=True)
        self.assertEqual(len(dis.get_users_alias()), 0)
        self.assertEqual(len(dis.get_hooks_alias()), 0)
        
        dis = Discotify(custom_config_file=str(config_path))
        users = dis.get_users_alias()
        hooks = dis.get_hooks_alias()
        self.assertEqual(len(users), 1)
        self.assertEqual(len(hooks), 1)
        self.assertEqual(users['asd'], '123')
        self.assertEqual(hooks['rei'], '000')
        
        config_path.unlink()
        self.assertFalse(config_path.exists())
    #end
    
    def test_send(self):
        """Test sending"""
        
        test_port = 53414
        server_initialized = [False]
        def start_server():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', test_port))
            server.listen(1)
            server_initialized[0] = True
            
            conn, addr = server.accept()
            data = conn.recv(4096)
            print(addr, data)

            # Send HTTP 200 OK response
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: {}\r\n"
                "Connection: close\r\n"
                "\r\n"
                "{}"
            ).format(len(data), data.decode(errors="replace"))
            conn.sendall(response.encode())

            conn.close()
            server.close()
            return data
        #end
        
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        
        while server_initialized is False:
            time.sleep(0.05)
        
        dis = Discotify(no_config_file=True)
        dis.hook_add('localhost', f'127.0.0.1:{test_port}')
        dis.user_add('thundy', '25926523946234')
        
        dis.send(tag='test', text='test string', mentions='123456', channels=f'http://127.0.0.1:{test_port}')
        dis.send(text='hello discord')
        
        self.assertTrue(True)
    #end
    
    def test_impossible_cases(self):
        """Test for logical errors"""
        dis = Discotify(no_config_file=True)
        
        try:
            dis.config_read(filepath='')
            self.assertTrue(False)
        except RuntimeError:
            pass
        
        try:
            dis.config_write(filepath='')
            self.assertTrue(False)
        except RuntimeError:
            pass
        
        dis = Discotify(no_config_file=False, custom_config_file='./tests/test_discotify.py')
        
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
