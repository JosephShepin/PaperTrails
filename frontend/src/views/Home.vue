<template>
  <div class="home">
    <!-- candidate search -->
    <div v-show="step == 1" :class="{ 'center': step == 1}" class="container shadow p-3 mb-5 bg-white rounded">
      <h1>Welcome to Lorem Ipsum</h1>
      <br>
      <input class="form-control" v-model="inputName" placeholder="Enter Candidate Name">
      <br>
      <button :disabled="inputName.length <= 5" class="btn btn-primary" @click="searchCandidates()">Search</button>
    </div>
    <!-- candidate select -->
    <div v-show="step == 2" class="shadow p-3 mb-5 bg-white rounded">
      <h1>Select Candidate</h1>
      <hr>
      <div class="candidates">
        <div v-for="candidate in candidateResults" @click="selectCandidate(candidate)" :key="candidate" class="candidate">
          <p class="name">{{ candidate.name }}</p>
          <div class="party-container">
            <p class="party" :class="{ 'dem': candidate.party_full.toLowerCase().includes('democrat'),  'rep': candidate.party_full.toLowerCase().includes('republican')}">{{ candidate.party_full }}</p>
          </div>
          <p class="years">Years Ran: {{candidate.election_years.join(', ') }}</p>
          <p class="state">{{ candidate.state == 'US' ? '': 'State: ' + candidate.state }}</p>
          <p class="state">Office: {{ candidate.office_full }}</p>
        </div>
      </div>
    </div>
    <!-- candidate results -->
    <div v-show="step == 3" class="shadow p-3 mb-5 bg-white rounded">
      <h1>Candidate Results</h1>
      <hr>
      <div class="dashboard">
        
      </div>
    </div>
  </div>
</template>

<script>
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
  },
  data(){
    return {
      step: 1,
      inputName: 'Joseph Biden',
      candidateResults: {},
    //   candidateResults: [
    //     {
    //         "candidate_id": "P60012143",
    //         "inactive_election_years": null,
    //         "district_number": 0,
    //         "office_full": "President",
    //         "state": "US",
    //         "last_f2_date": "2015-08-23",
    //         "district": "00",
    //         "office": "P",
    //         "party_full": "DEMOCRATIC PARTY",
    //         "has_raised_funds": false,
    //         "election_districts": [
    //             "00"
    //         ],
    //         "incumbent_challenge_full": "Open seat",
    //         "incumbent_challenge": "O",
    //         "load_date": "2016-11-17T06:10:49+00:00",
    //         "name": "BIDEN, JOE R",
    //         "active_through": 2016,
    //         "candidate_status": "N",
    //         "candidate_inactive": false,
    //         "principal_committees": [],
    //         "last_file_date": "2015-08-23",
    //         "cycles": [
    //             2016
    //         ],
    //         "party": "DEM",
    //         "first_file_date": "2015-08-23",
    //         "election_years": [
    //             2016
    //         ],
    //         "federal_funds_flag": false
    //     }
    // ],
    }
  },
  methods: {
    async selectCandidate(candidate){
      console.log(process.env.VUE_APP_SERVER_URL)
      const result = await fetch(`${process.env.VUE_APP_SERVER_URL}/candidate-data`,{
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
          'candidateid': candidate.candidate_id,
        },
        body: JSON.stringify(candidate)
      })
      if (result.status == 200){
        const response = await result.json()
        console.log(response)
      }
      this.step+=1
    },

    async searchCandidates() {
      const result = await fetch(`https://api.open.fec.gov/v1/candidates/search?api_key=${process.env.VUE_APP_FEC_API_KEY}&name=${this.inputName}`)
      if (result.status == 200) {
        const parsedResponse = await result.json()
        this.candidateResults = parsedResponse.results
        this.step+=1
      }
    }
  }
}
</script>

<style lang="sass" scoped>
.container
  position: absolute
  left: 50%
  transform: translateX(-50%)
  display: flex
  flex-direction: column
  max-width: 950px !important
  align-items: center
  justify-content: center

  
.shadow
  margin: 10px
  margin-top: -40px

.address-input
  width: 100%
  max-width: 600px
  text-align: center

.candidates
  display: flex
  flex-direction: column
  justify-content: flex-start !important
  .candidate
    transition: .2s all ease-in-out
    border-radius: 10px
    padding: 5px 0 5px 10px
    &:hover
      background: #F2F3F4
    .name
      font-size: 30px
    .party-container
      color: white
      .dem
        color: #2E86C1
      .rep
        color: #CB4335
      .party
        margin-top: -15px
    .years
      margin-top: -10px
    .state
      margin-top: -10px
      
      
    
  
</style>