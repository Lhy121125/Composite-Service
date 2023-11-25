from flask import Flask, jsonify
import asyncio
import aiohttp
import requests

app = Flask(__name__)

async def fetch_data(session, url, service_name):
    # The asynchronized data fetcher
    async with session.get(url) as response:
        data = await response.json
        # here is the log to show get response from service
        print(f"Received response from {service_name}")
        return service_name, data

def fetch_data_sync(url):
    # The synchronized data fetcher
    response = requests.get(url)
    return response.json()

# The async function
async def get_dashboard_data(user_id):
    async with aiohttp.ClientSession() as session:
        # TODO: Filled the url
        user_url = "api of microservice 1"
        cover_letter_url = "api of microservice 2"

        user_task = asyncio.create_task(fetch_data(session, user_url, "Micro-service 1"))
        cover_letter_task = asyncio.create_task(fetch_data(session, cover_letter_url, "Micro-service 2"))

        completion_order = []
        dashboard = {}

        for future in asyncio.as_completed([user_task,cover_letter_task]):
            service_name, data = await future
            completion_order.append(service_name)
            dashboard[service_name] = data

        return {
            "Dashboard Data": dashboard,
            "Async Call Order": completion_order
        }

@app.route('/get-user-details/<user_id>', methods=['GET'])
def get_user_details(user_id):
    user_url = f"http://api/user-service/users/{user_id}"
    cover_letter_url = f"http://api/application-status-service/status/{user_id}"

    #synchronized call
    user_data = fetch_data_sync(user_url)
    application_status = fetch_data_sync(cover_letter_url)

    return jsonify({
        "user": user_data,
        "applicationStatus": application_status
    })

if __name__ == '__main__':
    app.run(debug=True)