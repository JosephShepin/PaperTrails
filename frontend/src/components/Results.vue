<template>
       <div
      class="main-row"
      style="display: flex; padding: 10px; margin-top: -40px"
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

        <div class="shadow p-3 mb-2 bg-white rounded" style="margin: 0">
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
        <div class="shadow p-3 mb-5 bg-white rounded" style="margin: 0">
          <!-- articles -->
          <div class="large-articles-container">
            <div class="related-articles">
              <h2>Related News</h2>
              <hr />
            </div>
          </div>
          <div class="btn btn-primary" @click="getNews()">Get News</div>
          <div class="articles-container">
            <div class="articles">
              <div
                v-for="article in articles"
                :key="article"
                class="article"
                @click="openArticle(article.url)"
              >
                <img :src="article.image" class="thumbnail" />
                <div class="data">
                  <div class="title">{{ formatTitle(article.title) }}</div>
                  <div class="published-at">
                    {{ convertDate(article.published_at) }}
                  </div>
                  <div class="author">{{ article.author }}</div>
                </div>

                <br />
              </div>
            </div>
          </div>
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
                  <td>${{ addCommas(state[1]) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="shadow p-3 mb-5 bg-white rounded"
          v-show="donors.super_pacs != null && donors.super_pacs.length > 0"
        >
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
                    Super PAC Ad Spending
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
              </div>

              <div class="table-wrapper">
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
                      <td>{{ titleCase(name) }}</td>
                      <td>${{ addCommas(total) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            svgMap: "",
            candidateResults: {},
            articles: {},
            donors: {},
            chartOptions: {
        responsive: true,
        },
        plugins: {
            legend: {
            position: "right",
            },
        },
            }
    },
    props: {
        selectedCandidate:{
            type: Object
        },
        year: {
            type: Number
        }
    },
    async mounted() {
            // async selectCandidate(year, candidate) {
    let { year, candidate} = this;
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
    methods: {
 
        openArticle(url) {
      window.open(url, "_blank");
    },
       addCommas(x) {
      if (x == null || x == undefined) return "";
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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
    }
}
</script>
