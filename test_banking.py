import unittest
# Import functions directly from your main code file
from banking_system import users, deposit_funds, withdraw_funds, transfer_funds

class TestAdvancedBankingSystem(unittest.TestCase):

    def setUp(self):
        """
        Sets up clean testing data before each individual test runs,
        matching your exact system limits.
        """
        users["obaid"] = {"password": "0123!", "balance": 5000.0, "role": "customer", "expenses": [], "locked": False}
        users["ali"] = {"password": "User456!", "balance": 2500.0, "role": "customer", "expenses": [], "locked": False}

    # =========================================================================
    # ✅ PASSING CASES (EXPECTED TO PASS - RETURNS TRUE/VALID CODES)
    # =========================================================================
    
    def test_withdraw_sufficient(self):
        """[PASS CASE] Withdrawing 1000 PKR with a 5000 PKR balance returns remaining 4000 PKR"""
        status, new_balance = withdraw_funds(users["obaid"], 1000.0)
        self.assertTrue(status)
        self.assertEqual(new_balance, 4000.0)

    def test_withdraw_insufficient(self):
        """[PASS CASE] Correctly blocks withdrawal requests exceeding account balance"""
        status, message = withdraw_funds(users["obaid"], 6000.0)
        self.assertFalse(status)
        self.assertEqual(message, "Insufficient funds.")

    def test_withdraw_less_than_minimum_limit(self):
        """[PASS CASE] Blocks withdrawals below the updated 500 PKR threshold limit"""
        status, message = withdraw_funds(users["obaid"], 300.0)
        self.assertFalse(status)
        self.assertEqual(message, "Minimum withdrawal limit is PKR 500.0")

    def test_deposit_less_than_minimum_limit(self):
        """[PASS CASE] Blocks deposits below the updated 100 PKR threshold limit"""
        status, message = deposit_funds(users["obaid"], 50.0)
        self.assertFalse(status)
        self.assertEqual(message, "Minimum deposit limit is PKR 100.0")

    def test_transfer_greater_than_maximum_limit(self):
        """[PASS CASE] Blocks individual transfers exceeding the updated 20,000 PKR limit"""
        status, message = transfer_funds("obaid", "ali", 25000.0)
        self.assertFalse(status)
        self.assertEqual(message, "Transfer rejected. Maximum single transfer limit is PKR 20000.0")


    # =========================================================================
    # ❌ FAILING CASES (EXPECTED TO FAIL - EXPOSING LOGICAL SOFTWARE BUGS)
    # =========================================================================

    def test_deposit_negative_invalid(self):
        """
        [FAIL CASE] (Exposes Bug #1):
        We pass a negative deposit (-50). A secure system must return an explicit error 
        like 'Invalid Amount'. Because our logic lacks a dedicated 'amount <= 0' check, 
        it processes it under the default limit error instead of an invalid amount block.
        We assert that the error text must explicitly tell the user negative inputs are invalid.
        """
        status, message = deposit_funds(users["obaid"], -50.0)
        # Your code returns "Minimum deposit limit is PKR 100.0" instead of "Invalid Amount"
        self.assertEqual(message, "Invalid Amount. Negative values not allowed.", 
                         msg="BUG: System does not have a dedicated validation error for negative inputs!")

    def test_transfer_insufficient_overdraft(self):
        """
        [FAIL CASE] (Exposes Bug #2):
        Ali only has 2500 PKR. We transfer 2000 PKR (valid), leaving him with 500 PKR. 
        We then immediately attempt to transfer another 1000 PKR. The system should reject it,
        but because it completely lacks a balance validation check, it processes it anyway—
        dropping Ali into a negative balance (-500 PKR)!
        """
        # First valid transfer within his limits
        transfer_funds("ali", "obaid", 2000.0) 
        
        # Second transfer should return False due to low balance
        status, message = transfer_funds("ali", "obaid", 1000.0)
        
        # This assert expects False, but your code returns True, causing the test to FAIL
        self.assertFalse(status, msg="BUG: Bank processed a transfer exceeding available sender balance!")


if __name__ == '__main__':
    unittest.main()