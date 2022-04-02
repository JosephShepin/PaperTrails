import requests
import re

def requestFEC(cat, params):
    url = 'https://api.open.fec.gov/v1/'
    params_string = ""
    for k,v in params.items():
        params_string += "&" + k + "=" + v
    return requests.get(url + cat + '?api_key=' + FEC_API_KEY + params_string)

def getCommittee(candidate_data, cycle):
  committees = candidate_data['results'][0]['principal_committees']
  for c in committees:
    for y in c['cycles']:
      if y==cycle:
        return c['committee_id']
  return None

def fetchDonors(committee_id, cycle):
  r = requestFEC('schedules/schedule_a/by_employer/', {'sort':'-total', 'committee_id':committee_id, 'cycle':str(cycle), 'per_page':'100'})
  donors = {'Unemployed':0, 'Self Employed':0}
  unemployed_re = re.compile('unemployed|not employed|information requested|none')
  self_re = re.compile('self')
  for donor in r.json()['results']:
    if not donor['employer']:
      donors['Unemployed'] += donor['total']
      continue

    donor_str = donor['employer'].lower()
    if unemployed_re.search(donor_str):
      donors['Unemployed'] += donor['total']
    elif self_re.search(donor_str):
      donors['Self Employed'] += donor['total']
    else:
      donors[donor_str.title()] = donor['total']
  for k,v in donors.items():
    donors[k] = round(v,2)
  return donors

def fetchAllData(candidate_data, cycle):
    com = getCommittee(candidate_data, cycle)
    don = fetchDonors(com, cycle)
    return {'donors':don}