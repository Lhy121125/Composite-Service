import unittest
from main import app

class AppTest(unittest.TestCase):
    
    def setUp(self):
        # this set up the test client
        self.app = app.test_client()
        self.app.testing = True
        
    def test_async_dashboard_data(self):
        # Test Async
        response = self.app.get('/dashboard/0')
        self.assertEquals(response.status_code, 200)
    
    def test_sync_user_detail(self):
        # Test the sync
        response = self.app.get('/get-user-details/0')
        self.assertEqual(response.status_code, 200)
    

if __name__ == '__main__':
    unittest.main()