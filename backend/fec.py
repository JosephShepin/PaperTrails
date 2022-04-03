import requests
import re
import os

FEC_API_KEY = os.getenv("FEC_API_KEY")

def requestFEC(cat, params):
    url = 'https://api.open.fec.gov/v1/'
    params_string = ""
    for k,v in params.items():
        params_string += "&" + k + "=" + v
    return requests.get(url + cat + '?api_key=' + FEC_API_KEY + params_string)

def getCommittee(candidate_data, cycle):
  committees = candidate_data['principal_committees']
  for c in committees:
    for y in c['cycles']:
      if y==cycle:
        return c['committee_id']
  return None

def fetchDonors(committee_id, cycle):
  r = requestFEC('schedules/schedule_a/by_employer/', {'sort':'-total', 'committee_id':committee_id, 'cycle':str(cycle), 'per_page':'100'})
  companies = {}
  individuals = 0
  unemployed_re = re.compile('unemployed|not employed|information requested|none')
  self_re = re.compile('self')
  for donor in r.json()['results']:
    if not donor['employer']:
      individuals += donor['total']
      continue
    donor_str = donor['employer'].lower()
    if unemployed_re.search(donor_str):
      individuals += donor['total']
    elif self_re.search(donor_str):
      individuals += donor['total']
    else:
      companies[donor_str.title()] = donor['total']
  return {'individuals':round(individuals, 2)}, {'companies':companies}

def fetchMoneyRaised(committee_id, cycle):
    r = requestFEC('committee/' + committee_id + '/totals/', {'cycle':str(cycle)})
    return r.json()['results'][0]['receipts']

def fetchAllData(candidate_data, cycle):
    com = getCommittee(candidate_data, cycle)
    don = fetchDonors(com, cycle)
    return {'donors':don}
    