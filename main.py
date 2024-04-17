import cmd
from conection import Neo4jConnection
from user import UserManager
from business import BusinessManager

class MainCmd(cmd.Cmd):
    intro = 'Welcome to the Neo4j Fraud Management CLI. Type help or ? to list commands.\n'
    prompt = '(neo4j) '

    def __init__(self):
        super().__init__()
        self.neo4j_conn = Neo4jConnection()
        self.user_manager = UserManager(self.neo4j_conn)
        self.business_manager = BusinessManager(self.neo4j_conn)

    def do_exit(self, arg):
        """Exit the application."""
        print("Closing connection and exiting...")
        self.neo4j_conn.close()
        return True  # this will stop the Cmd application loop

    def do_users(self, arg):
        """Manage user information."""
        # Example command: users list
        args = arg.split()
        if not args:
            print("No action specified. Try 'users list', 'users add', etc.")
            return
        if args[0] == 'list':
            self.user_manager.list_users()
        elif args[0] == 'add':
            pass
        elif args[0] == 'delete':
            pass
        elif args[0] == 'update':
            pass
        else:
            print("Invalid user command.")
    
    def do_businesses(self, arg):
        """Manage business information."""
        args = arg.split()
        if not args:
            print("No action specified. Try 'businesses list', 'businesses add', etc.")
            return
        if args[0] == 'list':
            self.business_manager.list_businesses()
        else:
            print("Invalid business command.")


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