# doing necessary imports
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import log 
import Encoding
import store_predictions

app = Flask(__name__)       # initialising the flask app with the name 'app'
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/',methods=['GET'])
def home_page():
    file = open("app_logging\log.txt","a+")
    log.put_log(file,"Open Home page")
    file.close()
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    try:
        file = open("app_logging\log.txt","a+")
        log.put_log(file,"Predict func called")
        log.put_log(file,"log file opened")
        user_values = list(request.form.values())
        log.put_log(file,"Got values from user")
        features = Encoding.get_features(user_values)
        log.put_log(file,"Values encoded")
        final_features = [np.array(features)]
        prediction = model.predict(final_features)
        log.put_log(file,"Values predicted")

        output = round(prediction[0], 4)
        store_predictions.write_in_file(user_values,output,file)       

        log.put_log(file,f"Got output {output}")
        

        return render_template('index.html', prediction_text='Item Outlet Sales Should be $ {}'.format(output**4))
    
    except Exception as e:
        log.put_log(file,"ERROR!! There is some error!!")
        raise e

    finally:
        log.put_log(file,"log file closed")
        file.close()

if __name__ == "__main__":
    app.run(debug=True)
