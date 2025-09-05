import graphene
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# --- Schema ---
class OrderStatus(graphene.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(graphene.ObjectType):
    id = graphene.ID()
    orderNumber = graphene.String()
    totalAmount = graphene.Float()
    status = OrderStatus()
    createdAt = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    orders = graphene.List(Order)

    def resolve_orders(parent, info):
        return [
            Order(
                id="O100",
                orderNumber="ORD-2025-0001",
                totalAmount=249.99,
                status="CONFIRMED",
                createdAt="2025-08-29T10:15:00Z"
            )
        ]

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_user(root, info, id):
        return User(
            id=id,
            name="Alice Johnson",
            email="alice.johnson@example.com"
        )

schema = graphene.Schema(query=Query)

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- GraphQL POST handler ---
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(
        data.get("query"),
        variable_values=data.get("variables")
    )

    response = {}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    if result.data:
        response["data"] = result.data

    return jsonify(response)

# --- Minimal browser UI ---
@app.route("/", methods=["GET"])
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>GraphQL Test Runner</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            textarea { width: 100%; height: 200px; }
            pre { background: #f0f0f0; padding: 10px; }
            button { padding: 10px 20px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>GraphQL Test Runner</h2>
        <p>Type your GraphQL query below and click "Run":</p>
        <textarea id="query">{ user(id: "U123") { id name email orders { id orderNumber totalAmount status createdAt } } }</textarea><br>
        <button onclick="runQuery()">Run</button>
        <h3>Result:</h3>
        <pre id="result"></pre>

        <script>
            async function runQuery() {
                const query = document.getElementById('query').value;
                const res = await fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
