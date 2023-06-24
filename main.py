import requests
import json

with open("creds.json") as f:
    CREDS = json.loads(f.read())


def get_profile_collection(api_key, uuid, profile_id):
    url = f"https://api.hypixel.net/skyblock/profile?key={api_key}&profile={profile_id}&uuid={uuid}"
    response = requests.get(url)
    return response.json()


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Set your Hypixel API key here
api_key = CREDS["api_key"]

# Set the UUID for which you want to track collections
uuid = CREDS["uuid"]
profile_id = CREDS["profile_id"]

# Get the collection data from the API
response_json = get_profile_collection(api_key, uuid, profile_id)
print(response_json)
with open("test.json","w") as f:
    f.write(json.dumps(response_json))

# Check if profile and members data exists in the response
if 'profile' in response_json and 'members' in response_json['profile']:
    members = response_json['profile']['members']

    # Check if the UUID exists in the members data
    if uuid in members:
        profile_data = members[uuid]

        # Check if unlocked_coll_tiers exists and is a list
        if 'unlocked_coll_tiers' in profile_data and isinstance(profile_data['unlocked_coll_tiers'], list):
            unlocked_coll_tiers = profile_data['unlocked_coll_tiers']

            # Sort the unlocked collection tiers
            sorted_coll_tiers = sorted(unlocked_coll_tiers)

            # Save the sorted collection tiers to a JSON file
            #save_to_json('unlocked_coll_tiers.json', sorted_coll_tiers)
            print("Unlocked collection tiers saved and sorted to 'unlocked_coll_tiers.json' file.")
        else:
            print("No unlocked collection tiers found for the UUID.")
    else:
        print("UUID not found in profile members.")
else:
    print("Invalid response or profile data not found.")
