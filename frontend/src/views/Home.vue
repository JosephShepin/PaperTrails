<template>
  <div class="home">
    <!-- candidate search -->
    <div v-show="step == 1" :class="{ 'center': step == 1}" class="container shadow p-3 mb-5 bg-white rounded">
      <h1>Welcome to Lorem Ipsum</h1>
      <br>
      <input class="form-control" v-model="inputName" placeholder="Enter Candidate Name">
      <br>
      <button :disabled="inputName.length <= 5" class="btn btn-primary" @click="searchCandidates()">Search Candidates</button>
    </div>
    <!-- candidate select -->
    <div v-show="step == 2" class="shadow p-3 mb-5 bg-white rounded">
      <h1>Select Candidate And Year</h1>
      <hr>
      <div class="candidates">
        <div v-for="candidate in candidateResults" :key="candidate" class="candidate">
          <p class="name">{{ candidate.name }}</p>
          <div class="party-container">
            <p class="party" :class="{ 'dem': candidate.party_full.toLowerCase().includes('democrat'),  'rep': candidate.party_full.toLowerCase().includes('republican')}">{{ candidate.party_full }}</p>
          </div>
          <p class="state">{{ candidate.state == 'US' ? '': 'State: ' + candidate.state }}</p>
          <p class="state">Office: {{ candidate.office_full }}</p>
          <div class="years-row">
          <div class="year" @click="selectCandidate(candidate, year)" v-for="year in candidate.election_years" :key="year">
              {{ year }}
          </div>
          </div>
          
        </div>
      </div>
    </div>
    <!-- candidate results -->
    <div v-show="step == 3" class="shadow p-3 mb-5 bg-white rounded">
      <h1>Candidate Information</h1>
      <hr>
      <div class="dashboard">
        <div class="btn btn-primary" @click="getNews()">Get News</div>
        <!-- donors -->
        <!-- {{ donors }} -->
        <div class="donor" v-for="(key, value) in donors" :key="key">
        <p>${{ key.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }} {{ value }}</p>

        </div>
        <!-- articles -->
        <h2 style="text-align: center">Related Articles</h2>
        <hr>
        <div class="articles-container" style="display: flex; justify-content: center">
          <div class="articles">
            <div v-for="article in newsResults" :key="article" class="article" @click="window.open(article.url, '_blank')">
              <img :src="article.image" class="thumbnail"/>
              <div class="source"><b>{{ article.source }}</b></div>
              <div class="title">{{ article.title }}</div>
              <div class="author">{{ article.author }}</div>
              <br>
            </div>
          </div>
        </div>
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
      selectedCandidate: {},
      newsResults: {},
      donors: {},
    //   newsResults: [
    //     {
    //         "author": null,
    //         "title": "Opinion: Good riddance to this terrible Trump-era policy decision",
    //         "description": "It's past time to say good riddance to Title 42: It was bad policy during the Trump administration, and it has been bad policy under Biden, writes Raul A. Reyes.",
    //         "url": "https://www.cnn.com/2022/04/01/opinions/title-42-biden-good-riddance-reyes/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220331115023-04-us-mexico-border-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-04-01T23:32:01+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "New proof of life video surfaces showing American kidnapped in Afghanistan 2 years ago",
    //         "description": "The family of an American citizen taken hostage in Afghanistan more than two years ago welcomed an apparent proof of life video that was published on Friday and called on the Biden administration to take \"bold and decisive action\" to bring him home.",
    //         "url": "https://www.cnn.com/2022/04/01/politics/mark-frerichs-proof-of-life-video/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220401130340-mark-frerichs-proof-of-life-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-04-01T17:30:19+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "Biden administration announces official end to Title 42, the Trump-era pandemic restrictions at the US border",
    //         "description": "The Biden administration will end Trump-era pandemic restrictions that effectively blocked migrants from entering the United States on May 23, the US Centers for Disease Control and Prevention announced Friday.",
    //         "url": "https://www.cnn.com/2022/04/01/politics/immigration-title-42-repeal-cdc/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220331115023-04-us-mexico-border-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-04-01T17:01:02+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "White House hosts 'Jeopardy!' star Amy Schneider to mark Transgender Day of Visibility",
    //         "description": "\"Jeopardy!\" champion Amy Schneider visited the White House on Thursday to mark the International Transgender Day of Visibility as the Biden administration rolled out a series of measures in support of transgender Americans.",
    //         "url": "https://www.cnn.com/2022/03/31/politics/transgender-day-of-visibility-day-biden-administration/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220331173410-amy-schneider-033122-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-03-31T22:56:20+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "Chris Paul and Taraji P. Henson appointed to Biden's HBCU advisory board",
    //         "description": "President Joe Biden will announce Thursday that he is appointing more than a dozen top education leaders, celebrities and athletes to his board of advisers on historically Black colleges and universities, the White House said.",
    //         "url": "https://www.cnn.com/2022/03/31/politics/biden-hbcu-advisory-board-appointees/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220331144030-01-biden-hbcu-advisory-board-appointees-split-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-03-31T20:12:11+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "What Biden's shock-and-awe campaign means for high gas prices",
    //         "description": "President Joe Biden is taking a go-big-or-go-home approach toward easing the supply shock caused by Russia's invasion of Ukraine.",
    //         "url": "https://www.cnn.com/2022/03/31/politics/high-gas-prices-joe-biden-analysis/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/190916194106-strategic-petroleum-reserve-usa-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-03-31T19:31:38+00:00"
    //     },
    //     {
    //         "author": null,
    //         "title": "Biden is trying to ramp up production of critical minerals. Here's how it's supposed to help consumers",
    //         "description": "It's a move the administration hopes will kickstart the electric vehicle and renewable energy supply chain.",
    //         "url": "https://www.cnn.com/2022/03/31/politics/biden-critical-minerals-ev-batteries-climate/index.html",
    //         "source": "CNN",
    //         "image": "https://cdn.cnn.com/cnnnext/dam/assets/220331131900-ev-charging-2021-super-169.jpg",
    //         "category": "general",
    //         "language": "en",
    //         "country": "us",
    //         "published_at": "2022-03-31T17:50:20+00:00"
    //     }
    // ]
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
    async getNews(){
      const results = await fetch(`http://api.mediastack.com/v1/news?access_key=${process.env.VUE_APP_NEWS_API_KEY}&keywords=${this.selectedCandidate.name.replaceAll(',','')}&sort=published_desc&countries=us&languages=en&limit=15`)
      if (results.status == 200) {
        const data = await results.json()
        this.newsResults = data.data.filter((article) => article.image != null).slice(0,8)
      }
    },
    async selectCandidate(candidate, year){
      this.selectedCandidate = candidate
      console.log(process.env.VUE_APP_SERVER_URL)
      const response = await fetch(`${process.env.VUE_APP_SERVER_URL}/candidate-data`,{
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
          'candidateid': candidate.candidate_id,
          'year': year,
        },
        body: JSON.stringify(candidate)
      })
      if (response.status == 200){
        const result = await response.json()
        console.log(result)
        this.donors = result.donors


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
.articles
  max-width: 1000px
  display: flex
  flex-flow: row wrap
  justify-content: flex-start
  .article
    max-width: 200px
    .source
      font-size: 15px
      padding-top: 10px

.thumbnail
  width: 180px
  border-radius: 5px

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
    .years-row
      display: flex
      gap: 8px
      margin-top: -5px
      .year
        transition: .1s all ease-in-out
        padding: 4px 4px 2px 4px
        border-radius: 3px
        border: 1px solid black
        &:hover
          background: #EBEDEF
    .years
      font-size: 20px
      margin-top: -10px
    .state
      margin-top: -10px
      
      
    
  
</style>