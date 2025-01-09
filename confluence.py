from atlassian import Confluence

class ConfluenceConnector:
    def __init__(self, server_url, username, password):
        """
        Initialize Confluence connector with server details
        """
        self.confluence = Confluence(
            url=server_url,
            username=username,
            password=password,
            verify_ssl=True  # Set to False if using self-signed certificates
        )
    
    def test_connection(self):
        """
        Test if connection is successful
        """
        try:
            # Try to get user information to test connection
            self.confluence.get_current_user()
            print("Successfully connected to Confluence")
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def search_content(self, query, space_key=None, limit=10):
        """
        Search Confluence content using CQL
        Parameters:
            query (str): Search text
            space_key (str): Optional space key to limit search
            limit (int): Maximum number of results to return
        """
        try:
            cql = f'text ~ "{query}"'
            if space_key:
                cql += f' AND space = "{space_key}"'
            
            results = self.confluence.cql(cql, limit=limit)
            return results
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return None

def main():
    # Configuration
    server_url = input("Enter Confluence server URL (e.g., https://confluence.company.com): ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Create connector instance
    connector = ConfluenceConnector(server_url, username, password)
    
    # Test connection
    if not connector.test_connection():
        print("Exiting due to connection failure")
        return

    while True:
        # Get search parameters
        search_query = input("\nEnter search query (or 'quit' to exit): ")
        if search_query.lower() == 'quit':
            break
            
        space = input("Enter space key (optional, press Enter to skip): ")
        
        # Perform search
        results = connector.search_content(
            search_query,
            space_key=space if space else None
        )
        
        # Display results
        if results and results.get('results'):
            print("\nSearch Results:")
            for result in results['results']:
                print(f"\nTitle: {result['title']}")
                print(f"Type: {result['type']}")
                if 'webui' in result.get('_links', {}):
                    print(f"URL: {result['_links']['webui']}")
                if 'space' in result:
                    print(f"Space: {result['space']['key']}")
                print("-" * 50)
            print(f"\nTotal results found: {len(results['results'])}")
        else:
            print("No results found or search failed")

if __name__ == "__main__":
    main()