# importing flask modules
from flask import Flask , request , render_template , jsonify

# importing firebase_admin module
import firebase_admin

# importing firestore.py module to create firestore client
from firebase_admin import firestore

# importing credentials.py module from firebase_admin folder
from firebase_admin import credentials

# creating authentication file
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "potentiometer-b9db4",
  "private_key_id": "138349c361ec3fdbb4af9b9cbe6135723da33649",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDdVTv8fAS3oTo7\nyQWSiyIuDiQejBCM1Z1maPRUtOBTDfa97mrdv3fvmzC3VodmjtjSLAHv1jpVeWHe\nExvpFWPF4oIi7WgvSbm5/FyhF83IKvs02N2EI2CB/FRbGYMPaKDtv2mqcBVM+V+6\n0eFTt870LZF53iTZXpVeuPpcxdUxmyWkjhvPXkZwJmMvPWGeOpsufnH4DsXb6Wqd\nTp7MJpWdoBeiEz9+h2QWUi+hclKT09JW5bE12jyQCYfhi8GHX8nbLp5jfPLod1C0\n475s3r8nMOUHViw0NwawFliI4y4vWh/zwp5MJzx/pK25QAyclWWJc1Zl4JzzgmSM\nCtnDcVOPAgMBAAECggEAGzja/mRQfjdVvrmsNkhnhUuW9Kzccj3ptIlPF8YBWyW6\nBcU3nptoiG9JcBsz3xDNqRfhixqJpS6fM12dTq8jTNjdkacqa7qBHddkmyme1TI4\nIFlV8WUafxJGW8gI/xGqzWL//4b2j7eSJxueP5o5WX3rSRZh6NxBuds9a8CnRojo\nakskvtHpsXpzW4F1gvmye6bkL7xj40aWm+/oCdb8RbHuzyfydGaCWUPytKAJJqgk\n2eCu7q1i0z8byDoTqC69WoXyRO6QgMPH3lkpM2uIBO7VQjVfaZRWODv7APTIWRDR\nhnLco9LoAiCfVVl1SWZHq6Ab2AbMSY1oG8Rz3Kw/KQKBgQDxtjtArxNYaq6gimtD\n7M3NMV0Y/CEel/hHg2WjTC3Q9Wh87NXGzltWjPrrtJrJNsZAv4yG1uxPeyPke3bm\nWz9T8JY86IbK0DmlB1pKQqvfj5d9k3TjFMRZAh30a4rQtM++rty7B+FgN9dkMHQE\nm5shW60Yegh6r2f4Vr3oOKEQRwKBgQDqap0kFGCzYVw60wmBKrmZ6FDRWYm3mb3p\nhRVFsunquzwdNMuX1WE+HssL8jeyT8iucb5buuE86+3QxduQq+Za2UK/PTnKjTQL\nDGsfIBd7hKSwSt+5vqLZPGQMnkv8K+HP1Rtmdel5+5cPAH2QduJA8Ts22bR1JeS6\nRK+uQU1OeQKBgGL37Jb1mIQxWkMdqgHr6fBEcAwU4DK4os4VPP556KCQezH7fySh\nxcBQhUURc/dDWDWWuKFVSvjYQMAC1ZJIdkuWTM2vn9FXJOMveYbCecFV9/9Q6yE3\nlZWkSkOT7Qi7n/xBeNuTxHIzKxw4wqhIVmJ4OQ22mdYyD+4dBjEZTsltAoGABK+I\n4JW/sRY7H7nkML7H4vmv0990T0U1dJuCZ1hCMLz5YKQThb9wKCu5Z026K0hI/KOt\naGv94JfesxOhZezpt9sr6GKy6weTiL0Azyh3D7MBD70PZ8kVvD3myhHH9wxxgRQD\nbjLhLd0Hkfcyi1a1AxNPWbNUVhshzU9eK5+GihECgYBv2ZyVADZuM20tC7GMeusS\ntD/NeQc/RZxqyWtHYQu3NLoPTFOWzxLsTrc8MhUeUTtHuiGAM0SjjGVIdFOcUi5V\nXkwmM9+HpS7evvfeCdVjNDpVhOIzScCNfm7ZRs5Xj2BQnPJcna0jcLktwd0OAHe8\nbQ2UzrR8G68dVSZhq9YiEg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-zgd03@potentiometer-b9db4.iam.gserviceaccount.com",
  "client_id": "117129197034255587600",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zgd03%40potentiometer-b9db4.iam.gserviceaccount.com"
}
)

# connect this python script/app with firebase using the authentication credentials
firebase_admin.initialize_app(cred)

# creating firestore client
firebase_db = firestore.client()

# creating flask object
app = Flask(__name__)

# first api : index page, only GET requests allowed at this API 
@app.route("/")
def index():
    try:
        document_ref = firebase_db.collection("data")
        data = document_ref.order_by("date",direction="DESCENDING").limit(1).get()[0].to_dict()
        return render_template("/home/home.html",data=data)
    except Exception as e:
        print(str(e))
        return jsonify({
            "status":"Error",
            "message":"No data in database yet"
        }),400



# second api : adding data , only POST request allowed at this API
@app.route("/add-data", methods=["POST"])
def add_data():
    try:
       temperature = request.json.get("temperature")
       humidity = request.json.get("humidity")
       altitude = request.json.get("altitude")
       pressure = request.json.get("pressure")
       document_ref = firebase_db.collection("data")
       add_values = document_ref.document().create(dict(temperature=temperature,humidity=humidity,altitude=altitude,pressure=pressure,date=datetime.datetime.utcnow()))
       return jsonify({
           "status":"success"
       }),201
       
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# start the server
if __name__  ==  "__main__":
    app.run(host = '0.0.0.0' , debug = True)
