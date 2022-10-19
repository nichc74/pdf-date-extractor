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
        <Calendar :otherEvents="logOfExtractedDates"/>
        <div class="fileUploader">
          <label class="pdfLabel">
              PDFs
              <input type="file" id="files" ref="files" multiple @change="handleFileUploads( $event )"/>
          </label>
          <b-button id="uploadSubmitBtn" v-on:click="submitPDFs()" type="is-info">Submit</b-button>
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
import Calendar from './components/Calendar';

export default {
  name: 'App',
  components: {
    Calendar,
  },
  data: () => ({
    files: '',
    logOfExtractedDates: []
  }),
  methods: {
    handleFileUploads(event){
      this.files = event.target.files;
    },
    submitPDFs() {
      let formData = new FormData();

      // Append files to formData to prepare to send
      for(let i = 0; i < this.files.length; i++) {
        let currPDF = this.files[i]
        console.log(currPDF)
        formData.append('pdf[' + i + ']', currPDF)
      }

      var self = this;
      axios.post('http://127.0.0.1:8000/extractor/parse-pdfs/',
        formData,
        {
          headers: {
              'Content-Type': 'multipart/form-data',
          }
        }
      ).then(function(response) {
        let data = response.data
        self.logOfExtractedDates = data.log_of_extracted_dates
      }).catch(function(error){
        console.log(error)
        console.log('FAILURE!!');
      });
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

.fileUploader {
  display: flex;
  justify-content: center;
  margin-top: 25px;
}

.pdfLabel {
  display: flex;
  align-items: center;
}
</style>
