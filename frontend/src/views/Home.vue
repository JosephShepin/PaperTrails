<template>
  <div class="home">
    <!-- candidate search -->
    <div
      v-show="step == 1"
      :class="{ center: step == 1 }"
      class="container shadow p-3 mb-5 bg-white rounded"
    >
      <h1>Welcome to Lorem Ipsum</h1>
      <br />
      <input
        class="form-control"
        v-model="inputName"
        placeholder="Enter Candidate Name"
      />
      <br />
      <button
        :disabled="inputName.length <= 5"
        class="btn btn-primary"
        @click="searchCandidates()"
      >
        Search Candidates
      </button>
    </div>
    <!-- candidate select -->
    <div v-show="step == 2" class="shadow p-3 mb-5 bg-white rounded">
      <h1>Select Candidate And Year</h1>
      <hr />
      <div class="candidates">
        <div
          v-for="candidate in candidateResults"
          :key="candidate"
          class="candidate"
        >
          <p class="name">{{ candidate.name }}</p>
          <div class="party-container">
            <p
              class="party"
              :class="{
                dem: candidate.party_full.toLowerCase().includes('democrat'),
                rep: candidate.party_full.toLowerCase().includes('republican'),
              }"
            >
              {{ candidate.party_full }}
            </p>
          </div>
          <p class="state">
            {{ candidate.state == "US" ? "" : "State: " + candidate.state }}
          </p>
          <p class="state">Office: {{ candidate.office_full }}</p>
          <div class="years-row">
            <div
              class="year"
              @click="selectCandidate(candidate, year)"
              v-for="year in candidate.election_years"
              :key="year"
            >
              {{ year }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- candidate results -->
    <div
      v-show="step == 3"
      class="shadow p-3 mb-5 bg-white rounded"
      style="max-width: 2000px"
    >
      <h1>Candidate Information</h1>
      <hr />
      <div class="dashboard">
        <div class="btn btn-primary" @click="getNews()">Get News</div>
        <div class="info-container">
          <h4 style="margin-top: 20px; margin-bottom: -10px;">General Information</h4>
          <hr>
          <br>
          <p><b>Name: </b> {{ selectedCandidate.name }}</p>
          <p><b>{{ selectedCandidate.state == "US" ? "" : "State: " + selectedCandidate.state }}</b></p>
          <p><b>Party: </b>{{ selectedCandidate.party }}</p>
          <p><b>Incumbent/Challenger:</b> {{ selectedCandidate.incumbent_challenge_full }}</p>
          <p><b>Office:</b> {{ selectedCandidate.office_full }}</p>
          <p><b>Political Activism Through:</b> {{ selectedCandidate.active_through }}</p>
          <p></p>
        </div>
        <br>
        <!-- donors -->
        <div class="bar-charts-container">
          <h4>Financial Donors</h4>
          <hr>
          <div class="bar-charts">
            <div class="chart"  style="flex: 1">
              <p style="text-align: center; font-size: 20px; margin-bottom: -10px">Top Corporate Donors</p>
              <Bar
                class="shadow-sm p-3 mb-5 bg-white rounded"
                style="width: 100%; height: 400px;"
                :chart-options="chartOptions"
                :chart-data="donorChartData"
                chart-id="companies-chart"
                dataset-id-key="label"
                width="400"
                height="200"
              />
            </div>
            <div class="chart" style="flex: 1">
              <p>hello world</p>
            </div>

          </div>
        </div>

        <!-- articles -->
        <div
          style="
            display: flex;
            justify-content: center;
            position: relative;
            left: -10px;
          "
        >
          <div style="max-width: 980px; width: 100%; text-align: center">
            <h2 style="font-size: 25px; margin-bottom: -10px">
              Related Articles
            </h2>
            <hr />
          </div>
        </div>
        <div
          class="articles-container"
          style="display: flex; justify-content: center"
        >
          <div class="articles">
            <div
              v-for="article in newsResults"
              :key="article"
              class="article"
              @click="openArticle(article.url)"
            >
              <img :src="article.image" class="thumbnail" />
              <!-- <div class="source">
                <b>{{ article.source }}</b>
              </div> -->
              <!-- {{ article }} -->
              <div class="title">{{ article.title }}</div>
              <div class="author">{{ article.author }}</div>
              <br />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "Home",
  components: {
    Bar,
  },
  computed: {
    donorChartData() {
      const labels = [];
      const data = [];
      if (this.donors.companies != null) {
        for (const [key, value] of Object.entries(this.donors.companies)) {
          labels.push(key);
          data.push(value);
        }
        return {
          labels: labels,
          datasets: [
            {
              label: "Money Donated (USD)",
              backgroundColor: "#2874A6",
              data: data,
            },
          ],
        };
      } else {
        return {
          labels: [],
          datasets: [{ data: [] }],
        };
      }
    },
  },
  data() {
    return {
      step: 1,
      inputName: "Joseph Biden",
      candidateResults: {},
      selectedCandidate: {},
      newsResults: {},
      donors: {},
      chartOptions: {
        responsive: true,
      },
      plugins: {
        legend: {
          position: "right",
        },
      },
    };
  },
  methods: {
    openArticle(url) {
      window.open(url, "_blank");
    },
    async getNews() {
      const results = await fetch(
        `http://api.mediastack.com/v1/news?access_key=${
          process.env.VUE_APP_NEWS_API_KEY
        }&keywords=${this.selectedCandidate.name.replaceAll(
          ",",
          ""
        )}&sort=published_desc&countries=us&languages=en&sources=-dvidshub&limit=15`
      );
      if (results.status == 200) {
        const data = await results.json();
        this.newsResults = data.data
          .filter((article) => article.image != null)
          .slice(0, 8);
      }
    },
    async selectCandidate(candidate, year) {
      this.selectedCandidate = candidate;
      console.log(process.env.VUE_APP_SERVER_URL);
      const response = await fetch(
        `${process.env.VUE_APP_SERVER_URL}/candidate-data`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            candidateid: candidate.candidate_id,
            year: year,
          },
          body: JSON.stringify(candidate),
        }
      );
      if (response.status == 200) {
        const result = await response.json();
        console.log(result);
        this.donors = result.donors;
      }
      this.step += 1;
    },

    async searchCandidates() {
      const result = await fetch(
        `https://api.open.fec.gov/v1/candidates/search?api_key=${process.env.VUE_APP_FEC_API_KEY}&name=${this.inputName}`
      );
      if (result.status == 200) {
        const parsedResponse = await result.json();
        this.candidateResults = parsedResponse.results;
        this.step += 1;
      }
    },
  },
};
</script>

<style lang="sass" scoped>
.info-container
  p
    margin-top: -10px
.bar-charts
  display: flex
  max-width: 1500px
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
  height: 100px
  object-fit: cover
  border-radius: 5px
  margin-bottom: 10px

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
      background: #F2F4F4
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
          background: #34495E
          color: white
    .years
      font-size: 20px
      margin-top: -10px
    .state
      margin-top: -10px
</style>
