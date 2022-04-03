<template>
  <div class="home">
    <!-- candidate search -->
    <div
      v-show="true"
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
              @click="pickCandidate(year, candidate)"
              v-for="year in candidate.election_years"
              :key="year"
            >
              {{ year }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- <Results :year="pickedYear" :selectedCandidate="pickedCandidate" v-show="step == 3"/> -->
  </div>
</template>

<script>
import Results from "@/components/Results";
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
    Results
  },
  computed: {
    chartData() {
      const labels = [];
      const data = [];
      const colors = [
        "#5668e2",
        "#8a56e2",
        "#cf56e2",
        "#e256ae",
        "#e25668",
        "#e28956",
        "#e2cf56",
        "#aee256",
        "#68e256",
        "#56e289",
        "#56e2cf",
        "#56aee2",
        "#5668e2",
        "#5668e2",
        "#8a56e2",
        "#cf56e2",
      ];
      if (this.donors.super_pacs != null) {
        if (this.donors.super_pacs.length > 12) {
          this.donors.super_pacs.length = 12;
        }
        this.donors.super_pacs.forEach(({ name, total }) => {
          labels.push(name);
          data.push(total);
        });
        colors.length = labels.length;
        return {
          labels: labels,
          datasets: [
            {
              backgroundColor: colors,
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
        let count = 0;
        this.donors.donors.companies.forEach((x) => {
          if (count < 20) {
            labels.push(x[0]);
            data.push(x[1]);
          }
          count++;
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
      pickedCandidate,
      pickedYear,
      svgMap: "", ///
      candidateResults: {}, //
      selectedCandidate: { party: "", party_full: "" },
      articles: {}, //
      donors: {}, //
      focused: false,
      loading: false,
      chartOptions: {//
        responsive: true,
      },
      plugins: {
        legend: {
          position: "right",//
        },
      },//
    };
  },
  methods: {
    pickCandidate(year, candidate){
      this.pickedCandidate = candidate
      this.pickedYear = year
    },

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
