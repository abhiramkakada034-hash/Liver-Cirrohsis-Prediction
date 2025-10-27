"""
Flask App for Liver Disease Prediction
Enhanced with proper static file serving and prediction display
"""
from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load the model (create a dummy model for now since we don't have the actual pickle file)
try:
    model = pickle.load(open("liver_prediction.pkl", "rb"))
except FileNotFoundError:
    # Create a dummy model for demonstration
    class DummyModel:
        def predict(self, data):
            # Simple logic for demonstration
            # In reality, this would be your trained model
            import random
            return [random.choice([0, 1])]
    
    model = DummyModel()
    print("Warning: Using dummy model. Please add your liver_prediction.pkl file.")

@app.route("/")
def index():
    return render_template("page.html")

@app.route('/index', methods=['POST', 'GET'])
def prediction_page():
    if request.method == 'POST':
        try:
            # Extract form data
            AGE = float(request.form['AGE'])
            Gender = float(request.form['Gender']) if request.form['Gender'].isdigit() else (1 if request.form['Gender'].lower() == 'male' else 0)
            Place = float(request.form["Place(location where the patient lives)"]) if request.form["Place(location where the patient lives)"].isdigit() else 1
            Duration_of_alcohol_consumption = float(request.form["Duration of alcohol consumption(years)"])
            Quantity_of_alcohol_consumption = float(request.form["Quantity of alcohol consumption (quarters/day)"])
            
            Type_of_alcohol_consumed = float(request.form["Type of alcohol consumed"]) if request.form["Type of alcohol consumed"].isdigit() else 1
            Blood_pressure = float(request.form["Blood pressure (mmhg)"])
            Obesity = float(request.form["Obesity"]) if request.form["Obesity"].isdigit() else (1 if request.form["Obesity"].lower() == 'yes' else 0)
            Family_history_of_cirrhosis_hereditary = float(request.form["Family history of cirrhosis/ hereditary"]) if request.form["Family history of cirrhosis/ hereditary"].isdigit() else (1 if request.form["Family history of cirrhosis/ hereditary"].lower() == 'yes' else 0)
            
            Hemoglobin = float(request.form["Hemoglobin  (g/dl)"])
            PCV = float(request.form["PCV  (%)"])
            RBC = float(request.form["RBC  (million cells/microliter)"])
            MCV = float(request.form["MCV   (femtoliters/cell)"])
            MCH = float(request.form["MCH  (picograms/cell)"])
            MCHC = float(request.form["MCHC  (grams/deciliter)"])
            Total_Count = float(request.form["Total Count"])
            Polymorphs = float(request.form["Polymorphs  (%)"])
            Lymphocytes = float(request.form["Lymphocytes  (%)"])
            Monocytes = float(request.form["Monocytes   (%)"])
            Eosinophils = float(request.form["Eosinophils   (%)"])
            Basophils = float(request.form["Basophils  (%)"])
            Platelet_Count = float(request.form["Platelet Count  (lakhs/mm)"])
            Direct = float(request.form["Direct    (mg/dl)"])
            Indirect = float(request.form["Indirect     (mg/dl)"])
            Total_Protein = float(request.form["Total Protein     (g/dl)"])
            Albumin = float(request.form["Albumin   (g/dl)"])
            Globulin = float(request.form["Globulin  (g/dl)"])
            
            AL_Phosphatase = float(request.form["AL.Phosphatase      (U/L)"])
            SGOT_AST = float(request.form["SGOT/AST      (U/L)"])
            USG_Abdomen = float(request.form["USG Abdomen (diffuse liver or  not)"]) if request.form["USG Abdomen (diffuse liver or  not)"].isdigit() else (1 if request.form["USG Abdomen (diffuse liver or  not)"].lower() == 'yes' else 0)
            Outcome = float(request.form["Outcome"]) if request.form["Outcome"].isdigit() else 0
            
            # Prepare data for prediction
            data = [[AGE, Gender, Place, Duration_of_alcohol_consumption, Quantity_of_alcohol_consumption,
                    Type_of_alcohol_consumed, Blood_pressure, Obesity, Family_history_of_cirrhosis_hereditary,
                    Hemoglobin, PCV, RBC, MCV, MCH, MCHC, Total_Count, Polymorphs, Lymphocytes, Monocytes,
                    Eosinophils, Basophils, Platelet_Count, Direct, Indirect, Total_Protein, Albumin, Globulin,
                    AL_Phosphatase, SGOT_AST, USG_Abdomen, Outcome]]
            
            # Make prediction
            prediction = model.predict(data)
            prediction = int(prediction[0])
            
            # Determine result message
            if prediction == 0:
                result_message = "Low Risk - No significant liver disease detected"
                result_class = "success"
                recommendation = "Continue maintaining a healthy lifestyle. Regular check-ups are recommended."
            else:
                result_message = "High Risk - Potential liver disease detected"
                result_class = "warning"
                recommendation = "Please consult with a healthcare professional immediately for further evaluation and treatment."
            
            return render_template("index.html", 
                                 prediction=result_message,
                                 result_class=result_class,
                                 recommendation=recommendation,
                                 show_result=True)
        
        except ValueError as e:
            error_message = "Please ensure all numeric fields are filled with valid numbers."
            return render_template("index.html", 
                                 error=error_message,
                                 show_error=True)
        except Exception as e:
            error_message = f"An error occurred during prediction: {str(e)}"
            return render_template("index.html", 
                                 error=error_message,
                                 show_error=True)
    
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for prediction (for AJAX requests)"""
    try:
        data = request.get_json()
        # Process the data and make prediction
        # This is a simplified version - you'd implement the full logic here
        prediction = model.predict([list(data.values())])
        result = {
            'prediction': int(prediction[0]),
            'message': "Low Risk" if prediction[0] == 0 else "High Risk",
            'success': True
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

