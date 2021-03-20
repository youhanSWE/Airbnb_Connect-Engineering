import requests
import pymongo
import logging


def get_package_detail(track_no):

    """
    This function is used to send request to Fedex API and retrive a response with delivery information of a packge
    @param track_no: tracking number given by carrier (Fedex); a 16-digit string
    @return: return an JSON file in this format:
    {
        'Tracking No': str(track_no),
        'Status': key_status,
    }
    """
    logging.basicConfig(level=logging.INFO)
    try:
        header = {
            'Origin': 'https://www.fedex.com',
            'Referer': 'https://www.fedex.com/apps/fedextrack/?tracknumbers=%s&locale=en_CA&cntry_code=ca_english' % (str(track_no)),
        }

        data = {
            'action': 'trackpackages',
            'data': '{"TrackPackagesRequest":{"appType":"WTRK","appDeviceType":"DESKTOP","uniqueKey":"",'
                    '"processingParameters":{},"trackingInfoList":[{"trackNumberInfo":{"trackingNumber":"%s",'
                    '"trackingQualifier":"","trackingCarrier":""}}]}}' % (str(track_no)),
            'format': 'json',
            'locale': 'en_CA',
            'version': '1'
        }

        url = "https://www.fedex.com/trackingCal/track"

        logging.info('Sending request to Fedex...')

        response = requests.post(url, data=data, headers=header)

        if response.status_code > 299:
            logging.error('Request failed, error code : ', response.status_code)
            return
        else:
            logging.info("Response received successfully by Fedex")

        res_json = response.json()

        if res_json['TrackPackagesResponse']['packageList'][0]['errorList'][0]['message'] != "":
            logging.info(res_json['TrackPackagesResponse']['packageList'][0]['errorList'][0]['message'])
            # exists the function if package id is wrong
            return

        key_status = res_json['TrackPackagesResponse']['packageList'][0]['keyStatus']

        # changes the scheduled delivery date and time depends on delivery status
        result = {
            'Tracking No': str(track_no),
            'Status': key_status,
        }

        logging.info('Tracking no.: ' + result['Tracking No'] + ' is ' + result['Status'])

        return result

    except Exception as e:
        logging.error('Error occurred : \n Error Message: ' + str(e))
