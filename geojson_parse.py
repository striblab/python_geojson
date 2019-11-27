import gspread, os.path, boto3, json
from geojson import Point, Feature, FeatureCollection, dump
from datetime import datetime
import calendar
from itertools import islice
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



# import Google credentials, sheet ID, AWS creds, etc.
CREDENTIALS = os.environ.get('OAUTH_CREDENTIALS', '')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
SHEET_ID = os.environ.get('GOOGLE_SPREADSHEET_ID', '')
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', '')

# function that parses the 2D array from gspread into geojson format.

def sheet_to_json_onefile(obj1, obj2, obj3, file_name):
    features = []

    for row in islice(obj1, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "type": "nowopen",
                "name": name,
                "desc": desc,
                "address": address,
                "phone": phone,
                "website": website,
                "rel_id": rel_id,
                "image": image,
                "caption": caption,
                "credit": credit,
                "zoom": float(zoom),
                "bearing": float(bearing),
                "pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    for row in islice(obj2, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "type": "announced",
                "name": name,
                "desc": desc,
                "address": address,
                "phone": phone,
                "website": website,
                "rel_id": rel_id,
                "image": image,
                "caption": caption,
                "credit": credit,
                "zoom": float(zoom),
                "bearing": float(bearing),
                "pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    for row in islice(obj3, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "type": "closing",
                "name": name,
                "desc": desc,
                "address": address,
                "phone": phone,
                "website": website,
                "rel_id": rel_id,
                "image": image,
                "caption": caption,
                "credit": credit,
                "zoom": float(zoom),
                "bearing": float(bearing),
                "pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    feature_collection = FeatureCollection(features)

    with open(file_name, 'w') as f:
        dump(feature_collection, f)

    return


def sheet_to_json_1(obj, file_name):
    '''
    Takes the output of gspread and puts it in a dictionary.
    '''
    features = []

    for row in islice(obj, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "nowopen_name": name,
                "nowopen_desc": desc,
                "nowopen_address": address,
                "nowopen_phone": phone,
                "nowopen_website": website,
                "nowopen_rel_id": rel_id,
                "nowopen_image": image,
                "nowopen_caption": caption,
                "nowopen_credit": credit,
                "nowopen_zoom": float(zoom),
                "nowopen_bearing": float(bearing),
                "nowopen_pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    feature_collection = FeatureCollection(features)

    with open(file_name, 'w') as f:
        dump(feature_collection, f)

    return

def sheet_to_json_2(obj, file_name):
    '''
    Takes the output of gspread and puts it in a dictionary.
    '''
    features = []

    for row in islice(obj, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "closing_name": name,
                "closing_desc": desc,
                "closing_address": address,
                "closing_phone": phone,
                "closing_website": website,
                "closing_rel_id": rel_id,
                "closing_image": image,
                "closing_caption": caption,
                "closing_credit": credit,
                "closing_zoom": float(zoom),
                "closing_bearing": float(bearing),
                "closing_pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    feature_collection = FeatureCollection(features)

    with open(file_name, 'w') as f:
        dump(feature_collection, f)

    return

def sheet_to_json_3(obj, file_name):
    '''
    Takes the output of gspread and puts it in a dictionary.
    '''
    features = []

    for row in islice(obj, 1, None):
        # required fields, the script will break without these
        name = row[0]
        desc = row[6]
        obj_lat = row[2]
        obj_long = row[3]
        zoom = row[11] or '0'
        bearing = row[12] or '0'
        pitch = row[13] or '0'

        # non essential fields. uses a python "ternary" operator to populate field with empty string if falsey

        address = row[1] or ''
        phone = row[4] or ''
        website = row[5] or ''
        rel_id = row[7] or ''
        image = row[8] or ''
        caption = row[9] or ''
        credit = row[10] or ''


        # if lat or long field isn't populated, move to the next record
        if not obj_lat or not obj_long:
            continue
        else:
            obj_properties = {
                "announced_name": name,
                "announced_desc": desc,
                "announced_address": address,
                "announced_phone": phone,
                "announced_website": website,
                "announced_rel_id": rel_id,
                "announced_image": image,
                "announced_caption": caption,
                "announced_credit": credit,
                "announced_zoom": float(zoom),
                "announced_bearing": float(bearing),
                "announced_pitch": float(pitch)
            }

            obj_point = Point((float(obj_lat), float(obj_long)))
            obj_feature = Feature(geometry=obj_point, properties=obj_properties)
            features.append(obj_feature)

    feature_collection = FeatureCollection(features)

    with open(file_name, 'w') as f:
        dump(feature_collection, f)

    return

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('Restaurant-Roll-Call-eeffceef3580.json', scope)

gc = gspread.authorize(creds)

# open the three sheets we need
now_open = gc.open_by_key(SHEET_ID).get_worksheet(0)
announced = gc.open_by_key(SHEET_ID).get_worksheet(1)
closing_changing = gc.open_by_key(SHEET_ID).get_worksheet(2)

# get all of the values from each sheet, which comes as a 2D array
now_open_json = now_open.get_all_values()
announced_json = announced.get_all_values()
closing_changing_json = closing_changing.get_all_values()

currentYear = datetime.now().year
currentMonth = datetime.now().month
currentDay = datetime.now().day

last_day = calendar.monthrange(currentYear, currentMonth)

monthYear = str(currentMonth) + str(currentYear)

sheet_to_json_onefile(now_open_json, announced_json, closing_changing_json, './restaurants.geojson')

# run function on each 2D array, writing the result to a separate geojson file.
# sheet_to_json_1(now_open_json, './now_open.geojson')
# sheet_to_json_3(announced_json, './announced.geojson')
# sheet_to_json_2(closing_changing_json, './closing_changing.geojson')
#
# # upload to static.startribune.com
# s3 = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )
#
# s3_path = 'assets/features/thomas/'
#
# output1 = s3_path + 'now_open.geojson'
# output2 = s3_path + 'announced.geojson'
# output3 = s3_path + 'closing_changing.geojson'
#
# s3.upload_file('now_open.geojson', AWS_S3_BUCKET, output1)
# s3.upload_file('announced.geojson', AWS_S3_BUCKET, output2)
# s3.upload_file('closing_changing.geojson', AWS_S3_BUCKET, output3)
#
# if last_day == currentDay:
#     archive1 = s3_path + monthYear + '_' + 'now_open.geojson'
#     archive2 = s3_path + monthYear + '_' + 'announced.geojson'
#     archive3 = s3_path + monthYear + '_' + 'closing_changing.geojson'

    # s3.upload_file('now_open.geojson', AWS_S3_BUCKET, archive1)
    # s3.upload_file('announced.geojson', AWS_S3_BUCKET, archive2)
    # s3.upload_file('closing_changing.geojson', AWS_S3_BUCKET, archive3)
