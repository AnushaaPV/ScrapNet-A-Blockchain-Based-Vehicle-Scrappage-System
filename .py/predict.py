import joblib

def predict(carname, regyear, seater, insurance, fuel, km, owner, transmission, manufacture, milege, engine, maxpower, torque):

# Load the trained model
    model = joblib.load("car_price_prediction_model.pkl")

    # Define a new data point for prediction
    new_data = [[regyear,seater,km,milege,engine,maxpower,torque]]
    print(new_data)


    # Make predictions
    predicted_price = model.predict(new_data)

    print(f"Predicted Price: {predicted_price[0]} lakhs")

    return predicted_price[0]








