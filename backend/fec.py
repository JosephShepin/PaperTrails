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

    individuals = {'Unemployed':0, 'Self Employed':0, 'Retired':0, 'Miscellaneous':0}
    unemployed_re = re.compile('unemployed|not employed')
    self_re = re.compile('self')
    retired_re = re.compile('retired')
    misc_re = re.compile('information requested|none|n/a')

    for donor in r.json()['results']:
        if not donor['employer']:
            individuals['Miscellaneous'] += donor['total']
            continue
        donor_str = donor['employer'].lower()
        if misc_re.search(donor_str):
            individuals['Miscellaneous'] += donor['total']
        elif unemployed_re.search(donor_str):
            individuals['Unemployed'] += donor['total']
        elif self_re.search(donor_str):
            individuals['Self Employed'] += donor['total']
        elif retired_re.search(donor_str):
            individuals['Retired'] += donor['total']
        else:
            companies[donor_str.title()] = donor['total']

    for k,v in individuals.items():
        individuals[k] = round(v, 2)
    return {'individuals':individuals, 'companies':companies}

def fetchMoneyRaised(committee_id, cycle):
    r = requestFEC('committee/' + committee_id + '/totals/', {'cycle':str(cycle)})
    return r.json()['results'][0]['receipts']

def fetchContributionsByState(candidate_id, cycle):
    r = requestFEC('schedules/schedule_a/by_state/by_candidate', {'candidate_id':candidate_id, 'cycle':str(cycle), 'per_page':'100'})
    contributions = {}
    for state in r.json()['results']:
        contributions[state['state']] = [state['total'], state['state_full']]
    return contributions

def fetchAllData(candidate_id, candidate_data, cycle):
    com = getCommittee(candidate_data, cycle)
    don = fetchDonors(com, cycle)
    con = fetchContributionsByState(candidate_id, cycle)
    return {'donors':don, 'contributors':con}

