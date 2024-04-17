import cmd
from conection import Neo4jConnection
from user import UserManager
from business import BusinessManager
from account import AccountManager

class MainCmd(cmd.Cmd):
    intro = 'Welcome to the Neo4j Fraud Management CLI. Type help or ? to list commands.\n'
    prompt = '(neo4j) '

    def __init__(self):
        super().__init__()
        self.neo4j_conn = Neo4jConnection()
        self.user_manager = UserManager(self.neo4j_conn)
        self.business_manager = BusinessManager(self.neo4j_conn)
        self.account_manager = AccountManager(self.neo4j_conn)

    def do_exit(self, arg):
        """Exit the application."""
        print("Closing connection and exiting...")
        self.neo4j_conn.close()
        return True  # this will stop the Cmd application loop

    def do_users(self, arg):
        args = arg.split()
        action = args[0] if args else 'list'  # Default action
        {
            'list': self.user_manager.list_users,
            'add' : self.user_manager.add_users,
            'remove' : self.user_manager.remove_users, # acorde al dpi
            'update' : self.user_manager.update_users,
            'search' : self.user_manager.search_users
            
            # Add more actions here
        }.get(action, lambda: print("Invalid user command\n Try users list\nusers add\nusers remove\nusers update\nusers search"))()

    
    def do_businesses(self, arg):
        """Manage business info."""
        args = arg.split()
        action = args[0] if args else 'list'  # Default action
        {
            'list': self.business_manager.list_businesses
            # Add more actions here
        }.get(action, lambda: print("Invalid business command"))()

    def do_accounts(self, arg):
        '''Manage account info'''
        arg = arg.split()
        action = arg[0] if arg else 'list'
        {
            'list' : self.account_manager.list_accounts   
        }.get(action, lambda: print("Invalid account command"))


    def do_query(self, arg):
        """Run a custom Neo4j query. Usage: query <your_query_here>"""
        try:
            result = self.neo4j_conn.query(arg)
            for record in result:
                print(record)
        except Exception as e:
            print(f"An error occurred: {e}")

# Additional commands for User, Business, Account, Tax, etc.

if __name__ == '__main__':
    MainCmd().cmdloop()