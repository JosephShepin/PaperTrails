import requests
import re
import os
import pandas as pd 
import plotly.express as px

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
    companies = []

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
            companies.append([donor_str.title(), donor['total']])

    for k,v in individuals.items():
        individuals[k] = round(v, 2)
    return {'individuals':individuals, 'companies':companies}

def fetchFinancials(committee_id, cycle):
    r = requestFEC('committee/' + committee_id + '/totals/', {'cycle':str(cycle)})
    financials = r.json()['results'][0]
    return {'Total Funds Raised':financials['receipts'],'Total Expenditures':financials['disbursements']}

def fetchContributionsByState(candidate_id, cycle):
    r = requestFEC('schedules/schedule_a/by_state/by_candidate', {'candidate_id':candidate_id, 'cycle':str(cycle), 'per_page':'100'})
    contributions = []
    for state in r.json()['results']:
        contributions.append([state['state'], state['total'], state['state_full']])
    contributions = sorted(contributions, key=lambda x: x[1])
    return contributions

def getContributionMap(candidate_data, contributions):
    party = candidate_data['party'].lower()
    colors = px.colors.sequential.Greys
    if re.compile('dem').search(party):
        colors = px.colors.sequential.Blues
    elif re.compile('rep').search(party):
        colors = px.colors.sequential.Reds

    df = pd.DataFrame(contributions, columns = ['State', 'Contribution (USD)', 'full'])

    fig = px.choropleth(df,
                        locations='State', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='Contribution (USD)',
                        color_continuous_scale=colors, 
                        )
    return fig.to_image(format="svg")

def getSuperPACDonations(candidate_id, cycle):
    r = requestFEC('schedules/schedule_e/by_candidate/', {'candidate_id':candidate_id, 'cycle':str(cycle), 'sort':'-total', 'per_page':'20'})
    pacs = []
    for i in r.json()['results']:
        pacs.append( {'name':i['committee_name'], 'total':i['total']})
    return pacs

def fetchAllData(candidate_id, candidate_data, cycle):
    com = getCommittee(candidate_data, cycle)
    don = fetchDonors(com, cycle)
    con = fetchContributionsByState(candidate_id, cycle)
    fin = fetchFinancials(com, cycle)
    img = getContributionMap(candidate_data, con)
    pac = getSuperPACDonations(candidate_id, cycle)
    return {'donors':don, 'contributors':con, 'map':"".join(map(chr, img)), 'financials':fin, 'super_pacs':pac}

