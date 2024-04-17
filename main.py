import cmd
from app import Neo4jConnection


class MainCmd(cmd.Cmd):
    intro = 'Welcome to the Neo4j Management CLI. Type help or ? to list commands.\n'
    prompt = '(neo4j) '

    def __init__(self):
        super().__init__()
        self.neo4j_conn = Neo4jConnection()

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
            self.list_users()
        else:
            print("Invalid user command.")
    
    def list_users(self):
        try:
            query = "MATCH (n:User) RETURN n"
            users = self.neo4j_conn.query(query)
            for user in users:
                print(user)
        except Exception as e:
            print(f"An error occurred: {e}")

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