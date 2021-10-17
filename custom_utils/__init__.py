"""initialization script for the pip package"""
import dotenv

dotenv_path = dotenv.find_dotenv('.secret.env')
if dotenv_path:
    dotenv.load_dotenv(dotenv_path)
    print("-------------- Environment Variables Loaded Successfully ---------------")
