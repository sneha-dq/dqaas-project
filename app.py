from flask import Flask, request, jsonify
from run_validation import run_validation

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    file_path = data.get("file_path")
    suite_name = data.get("suite_name", "employees_suite")

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    try:
        success = run_validation(file_path, suite_name)
        return jsonify({
            "success": success,
            "message": "Validation completed",
            "data_docs_url": "gx/uncommitted/data_docs/local_site/index.html"
        }), 200 if success else 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
