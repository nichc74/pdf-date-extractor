<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <div>
        <Calendar/>
        <div class="buttonsWrapper">
          <b-button id="pdfUploadBtn" type="is-primary">Upload PDFs</b-button>
          <b-button id="apiButton" v-on:click="handleButtonClick" type="is-info">API Test</b-button>
        </div>
        <FileUploader/>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
import Calendar from './components/Calendar';
import FileUploader from './components/FileUploader';

export default {
  name: 'App',
  components: {
    Calendar,
    FileUploader
  },
  data: () => ({
    parsedPdfData: {}
  }),
  mounted () {
    axios.post('http://127.0.0.1:8000/extractor/parse-pdfs/', {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => {
        this.parsedPdfData = response.data
        console.log(response)
      }
    )
  },
  methods: {
    handleButtonClick() {
      console.log('Im being clicked!')
      axios.post('http://127.0.0.1:8000/extractor/parse-pdfs/', {
        headers: {
          'Content-Type': 'application/json',
        }
      }).then(response => {
          console.log('Im in the response')
          this.parsedPdfData = response.data
          console.log(response)
        }
      )
    }
  }
};
</script>

<style>
.buttonsWrapper {
  display: flex;
  justify-content: center;
  margin-top: 25px;
}

#pdfUploadBtn {
  margin-right: 10px;
}
</style>
