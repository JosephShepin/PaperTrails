<template>
  <div class="home">
    <!-- candidate search -->
    <div
      v-show="step == 1"
      :class="{ center: step == 1 }"
      style="margin-top: 0px; border-radius: 10px !important"
      class="container shadow p-3 mb-5 bg-white rounded"
      :style="{ border: focused ? '1px solid #808B96' : 'none' }"
    >
      <h1>Welcome to Lorem Ipsum</h1>
      <br />
      <input
        @focus="focused = true"
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
      <div
        v-show="loading"
        class="spinner-border text-secondary"
        role="status"
      ></div>
      <hr />
      <div class="candidates">
        <div
          v-for="candidate in candidateResults"
          :key="candidate"
          class="candidate"
          :class="{
            dem: candidate.party_full.toLowerCase().includes('democrat'),
            rep: candidate.party_full.toLowerCase().includes('republican'),
          }"
        >
          <p class="name">{{ titleCase(candidate.name) }}</p>
          <div class="party-container">
            <p
              class="party"
              :class="{
                dem: candidate.party_full.toLowerCase().includes('democrat'),
                rep: candidate.party_full.toLowerCase().includes('republican'),
              }"
            >
              {{ titleCase(candidate.party_full) }}
            </p>
          </div>
          <p class="state">
            {{ candidate.state == "US" ? "" : "State: " + candidate.state }}
          </p>
          <p class="state">Office: {{ candidate.office_full }}</p>
          <p>Select Another Year:</p>
          <div class="years-row">
            <div
              class="year"
              @click="selectCandidate(year, candidate)"
              v-for="year in candidate.election_years"
              :key="year"
            >
              {{ year }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="main-row"
      style="display: flex; padding: 10px; margin-top: -40px"
      v-show="step == 3"
    >
      <div class="main-col" style="flex: 1">
        <div
          class="candidate-info shadow mb-2 p-3 bg-white rounded"
          style="margin: 0; display: flex; justify-content: space-between"
        >
          <div>
            <div style="display: flex">
              <h1 style="margin-top: -30px">
                <b>{{ titleCase(selectedCandidate.name) }}</b>
              </h1>
              <div class="pill" :style="{ background: color }">
                {{ selectedCandidate.party }}
              </div>
            </div>
            <p v-show="selectedCandidate.state != 'US'">
              <b>State:</b> {{ selectedCandidate.state }}
            </p>
            <p>
              <b>Position Status:</b>
              {{ selectedCandidate.incumbent_challenge_full }}
            </p>
            <p><b>Office:</b> {{ selectedCandidate.office_full }}</p>
            <p><b>Selected Year: </b> {{ selectedYear }}</p>
            <div v-if="selectedCandidate.election_years != null">
              <p><b>Pick Another Year:</b></p>
              <div class="years-row">
                <div
                  class="year"
                  @click="selectCandidate(year)"
                  v-for="year in selectedCandidate.election_years.filter(
                    (x) => x != selectedYear
                  )"
                  :key="year"
                >
                  {{ year }}
                </div>
                <div
                  v-show="loading"
                  class="spinner-border"
                  :class="{
                    'text-primary': selectedCandidate.party_full
                      .toLowerCase()
                      .includes('democrat'),
                    'text-danger': selectedCandidate.party_full
                      .toLowerCase()
                      .includes('republican'),
                  }"
                  role="status"
                ></div>
              </div>
            </div>
          </div>
          <div class="">
            <div v-if="donors.picture != null">
              <img
                style="
                  width: 200px;
                  border-radius: 3px;
                  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
                "
                :src="donors.picture"
              />
            </div>
          </div>
        </div>

        <div
          v-if="donors.financials != null"
          class="shadow p-3 mb-2 bg-white rounded"
          style="margin: 0"
        >
          <p class="amount" style="color: green">
            ${{ addCommas(donors.financials["Total Funds Raised"]) }}
          </p>
          <p class="tag">Funds Raised</p>
          <p class="amount" style="color: red">
            ${{ addCommas(donors.financials["Total Expenditures"]) }}
          </p>
          <p class="tag" style="margin-bottom: -5px">Total Expenditure</p>
        </div>

        <div class="shadow p-3 mb-5 bg-white rounded" style="margin: 0">
          <Bar
            :chart-options="chartOptions"
            :chart-data="donorChartData"
            chart-id="companies-chart"
            dataset-id-key="label"
            width="400"
            height="200"
          />
          <h2 style="margin-bottom: -5px; margin-top: 10px; text-align: center">
            Top Individual Donations By Employer
          </h2>
        </div>
      </div>
      <div class="main-col" style="flex: 1">
        <div
          style="
            margin-top: 5px;
            display: flex;
            flex-direction: column;
            align-items: center;
          "
          class="shadow p-3 mb-5 bg-white rounded"
        >
          <h2
            style="margin-top: 15px; margin-bottom: -25px; text-align: center"
          >
            Campaign Donations By State
          </h2>
          <div v-html="svgMap"></div>

          <div class="table-wrapper">
            <table class="table" v-if="donors.contributors != null">
              <thead>
                <tr>
                  <th scope="col">State</th>
                  <th scope="col">Amount (USD)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="state in donors.contributors.reverse()" :key="state">
                  <td>{{ state[2] }}</td>
                  <td>{{ addCommas(state[1]) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="shadow p-3 mb-5 bg-white rounded">
          <div class="spending">
            <div class="">
              <div
                class=""
                style="
                  display: flex;
                  justify-content: center;
                  width: 100%;
                  position: relative;
                  overflow: hidden;
                "
              >
                <div class="">
                  <h2 style="margin-top: 15px; text-align: center">
                    Campaign Donations By State
                  </h2>

                  <Doughnut
                    style="max-width: 600px; width: 100%"
                    :chart-data="chartData"
                    chart-id="spending-chart"
                    dataset-id-key="label"
                    :cssClasses="{}"
                    width="200"
                    height="200"
                  />
                </div>
                <!-- <div
                  class=""
                  style="
                    width: 100%;
                    background: white;
                    height: 120px;
                    position: absolute;
                    top: 0;
                  "
                > -->
                <!-- <h2 style="margin-top: 15px; text-align: center">
                    Campaign Donations By State
                  </h2> -->
                <!-- </div> -->
              </div>

              <div class="table-wrapper" v-if="donors.super_pacs != null">
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col">PAC</th>
                      <th scope="col">Amount (USD)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="{ name, total } in this.donors.super_pacs"
                      :key="name"
                    >
                      <td>{{ name }}</td>
                      <td>{{ total }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar, Doughnut } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
);

export default {
  name: "Home",
  components: {
    Bar,
    Doughnut,
  },
  computed: {
    chartData() {
      const labels = [];
      const data = [];

      if (this.donors.super_pacs != null) {
        if (this.donors.super_pacs.length > 12) {
          this.donors.super_pacs.length = 12;
        }
        this.donors.super_pacs.forEach(({ name, total }) => {
          labels.push(name);
          data.push(total);
        });
        return {
          labels: labels,
          datasets: [
            {
              backgroundColor: ["#41B883", "#E46651", "#00D8FF", "#DD1B16"],
              data: data,
            },
          ],
        };
      }
      return {
        labels: [],
        datasets: [
          {
            backgroundColor: [],
            data: [],
          },
        ],
      };
    },
    color() {
      if (
        this.selectedCandidate != undefined &&
        this.selectedCandidate != null
      ) {
        if (
          this.selectedCandidate.party_full.toLowerCase().includes("republican")
        ) {
          return "#CB4335";
        }
        if (
          this.selectedCandidate.party_full.toLowerCase().includes("democrat")
        ) {
          return "#2E86C1";
        }
      }
      return "green";
    },
    stateChartData() {
      const labels = [];
      const data = [];
      if (this.donors.contributors != null) {
        if (this.donors.contributors.length > 20) {
          this.donors.contributors.length = 20;
        }
        this.donors.contributors.reverse().forEach((x) => {
          labels.push(x[0]);
          data.push(x[1]);
        });
        return {
          labels: labels,
          datasets: [
            {
              label: "Money Donated (USD)",
              backgroundColor: this.color,
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
    donorChartData() {
      const labels = [];
      const data = [];
      if (this.donors.donors != null) {
        if (this.donors.donors.length > 20) {
          this.donors.donors.length = 20;
        }
        this.donors.donors.companies.forEach((x) => {
          labels.push(x[0]);
          data.push(x[1]);
        });
        return {
          labels: labels,
          datasets: [
            {
              label: "Money Donated (USD)",
              backgroundColor: this.color,
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
      inputName: "Joseph Biden",
      step: 1,
      selectedYear: 0,
      svgMap: "",
      candidateResults: {},
      selectedCandidate: { party: "", party_full: "" },
      articles: {},
      donors: {},
      focused: false,
      loading: false,
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
    convertDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-us", {
        weekday: "long",
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
    formatTitle(title) {
      if (title != null) {
        if (title.length > 180) {
          return title.substring(0, 180) + "...";
        }
        return title;
      }
      return "";
    },
    titleCase(value) {
      if (value == null || value == undefined) {
        return "";
      }
      return value
        .toLowerCase()
        .replace(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
    },
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
        )}&sort=published_desc&countries=us&languages=en&sources=cnn,fox,bbc&limit=15`
      );
      if (results.status == 200) {
        const data = await results.json();
        this.articles = data.data
          .filter((article) => article.image != null)
          .slice(0, 8);
      }
    },
    async selectCandidate(year, candidate) {
      this.loading = true;
      console.log("selecting candidate");

      if (candidate != null) {
        console.log("setting new candidate");
        this.selectedCandidate = candidate;
      }
      this.selectedYear = year;
      console.log(process.env.VUE_APP_SERVER_URL);
      console.log("fetching data...");
      const response = await fetch(
        `${process.env.VUE_APP_SERVER_URL}/candidate-data`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            candidateid: this.selectedCandidate.candidate_id,
            year: year,
          },
          body: JSON.stringify(this.selectedCandidate),
        }
      );
      if (response.status == 200) {
        const result = await response.json();
        console.log(result);
        this.loading = false;
        this.donors = result;
        this.svgMap = result.map;
      }
      if (this.step == 2) {
        this.step += 1;
      }
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

    addCommas(x) {
      if (x == null || x == undefined) return "";
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
  },
};
</script>

<style lang="sass" scoped>
@import url('https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;500;600&family=Space+Mono&display=swap');

.home
  margin-top: 50px
  font-family: 'League Spartan', sans-serif
  font-size: 20px
.large-related-articles
  display: flex
  justify-content: center
  position: relative
  left: -10px
  .related-articles
    max-width: 1180px
    width: 100%
    text-align: center
    h2
      font-size: 35px
      font-weight: bold
      margin-bottom: -10px
.info-container
  display: flex
  p
    margin-top: -10px
.bar-charts-container
  display: flex
  justify-content: center
.bar-charts
  display: flex
  gap: 10px
  max-width: 1500px
  width: 100%
  .chart
    .title
      text-align: center
      font-size: 25px
      margin-bottom: -10px
.rounded
  margin: 0
.articles-container
  // display: flex
  // justify-content: center
  .articles
    gap: 10px
    // max-width: 1200px
    // display: flex
    // flex-flow: row wrap
    // justify-content: center

    .article
      display: flex
      // max-width: 210px
      border-radius: 2px
      // box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px
      padding: 10px
      transition: all .14s ease-in-out
      &:hover
        transform: scale(1.005)

    .thumbnail
      width: 190px
      height: 120px
      object-fit: cover
      border-radius: 3px
      margin-bottom: 10px
    .data
      padding-left: 30px
      .title
        font-size: 28px
        font-weight: bold
      .published-at
        font-size: 20px

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
    transition: .1s all ease-in-out
    border-radius: 10px
    padding: 5px 0 10px 10px
    &.dem
      &:hover
        background: rgba(46, 134, 193, .1)
    &.rep
      &:hover
        background: rgba(203, 67, 53, .08)
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
      font-size: 20px
      margin-top: -10px
    .state
      margin-top: -10px

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

.amount
  font-size: 40px
  font-weight: bold
  margin-bottom: 5px

.tag
  font-size: 20px
  font-weight: bold

.pill
  color: white
  font-weight: bold
  text-align: center
  border-radius: 20px
  margin-top: -20px
  margin-left: 15px
  width: 60px
  height: 26px

.table-wrapper
  width: 100%
  height: 200px !important
  overflow: auto

.spending
  // display: flex
  // flex-direction: column
  // align-items: center
</style>
