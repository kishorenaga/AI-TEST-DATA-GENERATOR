from ariadne import load_schema_from_path, make_executable_schema, QueryType, ObjectType, graphql_sync
from ariadne.asgi import GraphQL
import uvicorn
import os

# Load schema from file
schema_path = os.path.join(os.path.dirname(__file__), "schema.graphql")
type_defs = load_schema_from_path(schema_path)

# Define resolvers
query = QueryType()
user = ObjectType("User")
order = ObjectType("Order")

# Example resolvers (replace with real logic)
@query.field("users")
def resolve_users(*_):
    return [
        {
            "id": "1",
            "name": "Alice",
            "email": "alice@example.com",
            "orders": []
        },
        {
            "id": "2",
            "name": "Bob",
            "email": "bob@example.com",
            "orders": []
        }
    ]

schema = make_executable_schema(type_defs, [query, user, order])
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run("apollo_server:app", host="0.0.0.0", port=8000, reload=True)
