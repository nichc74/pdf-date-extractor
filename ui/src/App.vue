<template>
  <v-app>
    <v-main>
      <div>
        <b-loading :is-full-page="true" v-model="isLoading"></b-loading>
        <Calendar :events="logOfExtractedDates"/>
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
    logOfExtractedDates: [],
    isLoading: false,
  }),
  methods: {
    handleFileUploads(event){
      this.files = event.target.files;
    },
    submitPDFs() {
      let formData = new FormData();
      this.isLoading = true

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
        self.isLoading = false
        self.$buefy.notification.open({
          message: 'Files uploaded successfully!',
          type: 'is-success'
        })
      }).catch(function(error){
        console.log(error)
        self.isLoading = false
        self.$buefy.notification.open({
          message: 'Oops! Something went wrong. Please try again.',
          type: 'is-danger'
        })
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
