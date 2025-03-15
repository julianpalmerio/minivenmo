"""
Questions:
 

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this
   

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.
"""

"""
MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful
baby. In order to make this happen, you must write a social payment app.
Implement a program that will feature users, credit cards, and payment feeds.
"""

import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')

    def retrieve_feed(self):
        # TODO: add code here
        return []

    def add_friend(self, new_friend):
        # TODO: add code here
        pass

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        # TODO: add logic to pay with card or balance
        pass

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        # TODO: add code here
        pass

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        new_user = User(username)
        new_user.add_to_balance(balance)
        new_user.add_credit_card(credit_card_number)
        return new_user

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestMiniVenmo(unittest.TestCase):

    def test_create_user_success(self):
        venmo = MiniVenmo()
        user = venmo.create_user("Bobby", 5.00, "4111111111111111")
        self.assertEqual(user.username, "Bobby")
        self.assertEqual(user.balance, 5.00)
        self.assertEqual(user.credit_card_number, "4111111111111111")

class TestUser(unittest.TestCase):

    def test_add_to_balance(self):
        user = User("Bobby")
        user.add_to_balance(5.00)
        self.assertEqual(user.balance, 5.00)

    def test_add_credit_card_success(self):
        user = User("Bobby")
        user.add_credit_card("4111111111111111")
        self.assertEqual(user.credit_card_number, "4111111111111111")

    def test_add_credit_card_failure(self):
        user = User("Bobby")
        with self.assertRaises(CreditCardException):
            user.add_credit_card("123456")
        user.add_credit_card("4111111111111111")
        with self.assertRaises(CreditCardException):
            user.add_credit_card("4242424242424242")

    def test_pay_with_balance_success(self):
        bobby = User("Bobby")
        carol = User("Carol")
        bobby.add_to_balance(5.00)
        payment = bobby.pay_with_balance(carol, 5.00, "Coffee")
        self.assertEqual(bobby.balance, 0.00)
        self.assertEqual(carol.balance, 5.00)
        self.assertEqual(payment.amount, 5.00)
        self.assertEqual(payment.actor, bobby)
        self.assertEqual(payment.target, carol)
        self.assertEqual(payment.note, "Coffee")

    def test_pay_with_balance_failure(self):
        bobby = User("Bobby")
        carol = User("Carol")
        with self.assertRaises(PaymentException):
            bobby.pay_with_balance(carol, 0.00, "Coffee")
        with self.assertRaises(PaymentException):
            bobby.pay_with_balance(carol, 5.00, "Coffee")
        with self.assertRaises(PaymentException):
            bobby.pay_with_balance(bobby, 5.00, "Coffee")

    def test_pay_with_card_success(self):
        bobby = User("Bobby")
        carol = User("Carol")
        bobby.add_credit_card("4111111111111111")
        payment = bobby.pay_with_card(carol, 5.00, "Coffee")
        self.assertEqual(bobby.balance, 0.00)
        self.assertEqual(carol.balance, 5.00)
        self.assertEqual(payment.amount, 5.00)
        self.assertEqual(payment.actor, bobby)
        self.assertEqual(payment.target, carol)
        self.assertEqual(payment.note, "Coffee")

    def test_pay_with_card_failure(self):
        bobby = User("Bobby")
        carol = User("Carol")
        with self.assertRaises(PaymentException):
            bobby.pay_with_card(bobby, 5.00, "Coffee")
        with self.assertRaises(PaymentException):
            bobby.pay_with_card(carol, 0.00, "Coffee")
        with self.assertRaises(PaymentException):
            bobby.pay_with_card(carol, 5.00, "Coffee")

if __name__ == '__main__':
    unittest.main()
