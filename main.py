import cmd
from conection import Neo4jConnection
from user import UserManager
from business import BusinessManager, TaxManager
from account import AccountManager
from transactions import DepositManager, WithdrawalManager, RecordManager

class MainCmd(cmd.Cmd):
    intro = 'Neo4j Fraud Management CLI. Type help or ? to list commands.\n'
    prompt = '(neo4j) '

    def __init__(self):
        super().__init__()
        self.neo4j_conn = Neo4jConnection()
        self.user_manager = UserManager(self.neo4j_conn)
        self.business_manager = BusinessManager(self.neo4j_conn)
        self.account_manager = AccountManager(self.neo4j_conn)
        self.tax_manager = TaxManager(self.neo4j_conn)
        self.deposit_manager = DepositManager(self.neo4j_conn)
        self.withdrawal_manager = WithdrawalManager(self.neo4j_conn)
        self.record_manager = RecordManager(self.neo4j_conn)

    def do_exit(self, arg):
        """Exit the application."""
        print("Closing connection and exiting...")
        self.neo4j_conn.close()
        return True  # this will stop the Cmd application loop

    def do_users(self, arg):
        """For actions done with users\nCommands:
            \n- list\n- add\n- remove\n- update\n- search
        """
        args = arg.split()
        action = args[0] if args else 'list'  # Default action
        {
            'list': self.user_manager.list_users,
            'add' : self.user_manager.add_users, # crea usuario
            'remove' : self.user_manager.remove_users, # acorde al dpi lo quita
            'update' : self.user_manager.update_users, # actualizar un usuario o actualizar el nodo
            'search' : self.user_manager.search_users # filtrar dada(s) cierta(s) propiedad(es)
            
            
        }.get(action, lambda: print("Invalid user command"))()

    
    def do_businesses(self, arg):
        """Manage business info\nCommands:
            \n- list\n- label\n- unlabel
        """
        args = arg.split()
        action = args[0] if args else 'list'  # Default action
        {
            'list': self.business_manager.list_businesses,
            'label': self.business_manager.add_label,
            'unlabel': self.business_manager.remove_labels
            
        }.get(action, lambda: print("Invalid business command"))()

    def do_accounts(self, arg):
        """Manage account info"\nCommands:
            \n- list\n- relate\n- unrelate\n- search
        """
        arg = arg.split()
        action = arg[0] if arg else 'list'
        {
            'list' : self.account_manager.list_accounts,
            'relate': self.account_manager.create_relationships,
            'unrelate': self.account_manager.break_relationships,
            'search': self.account_manager.search_account   

        }.get(action, lambda: print("Invalid account command"))

    def do_tax(self, arg):
        """Handle tax operations\nCommands:
            \n- list\n- download\n- upload
        """
        args = arg.split()
        action = args[0] if args else 'list'
        {
            'list': self.tax_manager.list_taxes,
            'download': self.tax_manager.download_csv,
            'upload': self.tax_manager.upload_csv
        }.get(action, lambda: print("Invalid tax command"))()


    def do_deposit(self, arg):
        """Handle deposit operations\nCommands:
            \n- list\n- make
        
        """
        args = arg.split()
        action = args[0] if args else 'list'
        {
            'list': self.deposit_manager.list_deposits,
            'make': self.deposit_manager.make_deposit
        }.get(action, lambda: print("Invalid deposit command"))()

    def do_withdrawal(self, arg):
        """Handle withdrawal operations\nCommands:
            \n- list\n- make
        """
        args = arg.split()
        action = args[0] if args else 'list'
        {
            'list': self.withdrawal_manager.list_withdrawal,
            'make': self.withdrawal_manager.make_withdrawal
        }.get(action, lambda: print("Invalid withdrawal command"))()

    
    def do_record(self, arg):
        """Handle record operations\nCommands:
            \n- list\n- analyze
        """
        args = arg.split()
        action = args[0] if args else 'list'
        {
            'list': self.record_manager.list_records,
            'analyze': self.record_manager.analyze_records
        }.get(action, lambda: print("Invalid record command"))()

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