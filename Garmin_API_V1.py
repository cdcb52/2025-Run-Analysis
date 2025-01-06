# import libraries

from pathlib import Path
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectTooManyRequestsError, GarminConnectAuthenticationError
import pandas as pd
import json
import sys
sys.path.insert(0, r'./')
sys.path.insert(0, r'./..')



# uncomment to save the account info above in json format the easy way
# json.dump(garmin_account, open(account_path / 'garmin.json', 'w'))



with open('garmin.json', 'r') as file:
    garminaccount = json.load(file)


try:
    client = Garmin(garminaccount['email'], garminaccount['password'])
    client.login()
    # Fetches the xx most recent activities
    activities = client.get_activities(0, 500)

except (GarminConnectConnectionError, GarminConnectAuthenticationError, GarminConnectTooManyRequestsError) as err:
    print(f"Error occurred: {err}")

# create dataframe
activitydata = pd.DataFrame(activities)

activitydata['distance'] = activitydata['distance'] / 1609.34
activitydata['duration'] = activitydata['duration'] / 60
activitydata['pace'] = activitydata['duration'] / activitydata['distance']

activitydata['activityType'] = activitydata['activityType'].apply(
    lambda x: x['typeKey'])

# list of columns to keep
keep_columns = ['startTimeLocal', 'pace', 'activityId', 'activityName', 'activityType', 'distance', 'duration', 'elapsedDuration', 'movingDuration', 'elevationGain', 'elevationLoss', 'averageSpeed', 'maxSpeed', 'calories', 'averageHR', 'maxHR', 'averageRunningCadenceInStepsPerMinute',
                'maxRunningCadenceInStepsPerMinute', 'avgPower', 'maxPower', 'aerobicTrainingEffect', 'anaerobicTrainingEffect', 'normPower', 'avgStrideLength', 'vO2MaxValue', 'minElevation', 'maxElevation', 'locationName', 'waterEstimated', 'activityTrainingLoad', 'avgGradeAdjustedSpeed']

# drop all columns except the ones in keep_columns
activitydata = activitydata.drop(
    columns=[col for col in activitydata.columns if col not in keep_columns])

activitydata['date'] = pd.to_datetime(
    activitydata['startTimeLocal'], format='%Y-%m-%d %H:%M:%S')
activitydata.drop(columns=['startTimeLocal'], inplace=True)

