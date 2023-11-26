from flask import Flask, jsonify
import asyncio
import aiohttp
import requests
import random

app = Flask(__name__)

async def fetch_data(session, url, service_name):
    # Since microservice 1 is always faster, we introduce this to simulate random network latency to show async
    await asyncio.sleep(random.uniform(0, 2))
    # The asynchronized data fetcher
    async with session.get(url) as response:
        data = await response.json()
        # here is the log to show get response from service
        print(f"Received response from {service_name}")
        return service_name, data

# The async function
async def get_dashboard_data(user_id):
    async with aiohttp.ClientSession() as session:
        # TODO: Filled the url 2 with cover letter one
        user_url = f"http://ec2-18-116-37-42.us-east-2.compute.amazonaws.com:8012/users/{user_id}"
        cover_letter_url = f"https://modular-granite-402517.uc.r.appspot.com/{user_id}/get_template_count"

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

@app.route('/dashboard/<int:user_id>', methods=['GET'])
async def api_get_dashboard_data(user_id: int):
    return await get_dashboard_data(user_id)

def fetch_data_sync(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None  # or handle error appropriately

# The synchronized function
@app.route('/get-user-details/<user_id>', methods=['GET'])
def get_user_details(user_id):
    user_url = f"http://ec2-18-116-37-42.us-east-2.compute.amazonaws.com:8012/users/{user_id}"
    cover_letter_url = f"https://modular-granite-402517.uc.r.appspot.com/{user_id}/get_template_count"

    result = {}
    #synchronized call
    user_data = fetch_data_sync(user_url)
    result['information of user'] = user_data
    cover_letter_status = fetch_data_sync(cover_letter_url)
    result['number of cover letter'] = cover_letter_status

    return result

if __name__ == '__main__':
    app.run(debug=True)