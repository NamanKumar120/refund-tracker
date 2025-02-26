from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///refunds.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Refund Model
class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=False)
    orderID = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Create the database tables (only runs once)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Backend is working!"

# API to add refund
@app.route("/add_refund", methods=["POST"])
def add_refund():
    data = request.get_json()
    new_refund = Refund(
        platform=data["platform"],
        orderID=data["orderID"],
        amount=float(data["amount"]),
        date=data["date"],
        status=data["status"]
    )
    db.session.add(new_refund)
    db.session.commit()
    return jsonify({"message": "Refund added successfully!"})

# API to get all refunds
@app.route("/get_refunds", methods=["GET"])
def get_refunds():
    refunds = Refund.query.all()
    refund_list = [
        {
            "platform": refund.platform,
            "orderID": refund.orderID,
            "amount": refund.amount,
            "date": refund.date,
            "status": refund.status
        }
        for refund in refunds
    ]
    return jsonify(refund_list)

if __name__ == "__main__":
    app.run(debug=True)
