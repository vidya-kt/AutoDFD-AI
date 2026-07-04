from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from utils.helpers import (
    is_invalid_description,
    is_ambiguous_description
)

from services.groq_service import generate_dfd

dfd_bp = Blueprint(
    "dfd",
    __name__
)

# Homepage Route
@dfd_bp.route("/")
def home():
    return render_template("index.html")


# Generate DFD Route
@dfd_bp.route("/generate-dfd", methods=["POST"])
def generate_dfd_route():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No input received"
            }), 400

        description = data.get("description")

        if not description:

            return jsonify({
                "success": False,
                "error": "Description required"
            }), 400

        # Length validation
        if len(description) > 3000:

            return jsonify({
                "success": False,
                "error": "Input too large"
            }), 400
        
        if is_invalid_description(description):

            return jsonify({
                "success": False,
                "error":
                "Please enter a meaningful system description."
            }), 400


        if is_ambiguous_description(description):

            return jsonify({
                "success": False,
                "error":
                "Description is too vague. Please describe the workflow, processes, and data flow."
            }), 400

        result = generate_dfd(description)

        return jsonify({
            "success": True,
            "mermaid": result["mermaid"],
            "level": result["level"]
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500