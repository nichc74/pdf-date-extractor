<template>
    <div id="fileUploader">
        File Uploader Component
        <label>
            PDFs
            <input type="file" id="files" ref="files" multiple @change="handleFileUploads( $event )"/>
        </label>
        <b-button id="uploadSubmitBtn" v-on:click="submitPDFs()" type="is-info">Submit</b-button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'FileUploader',
    data: () => ({
        files: ''
    }),
    methods: {
        handleFileUploads(event){
            this.files = event.target.files;
        },
        submitPDFs() {
            console.log('Submitting PDFs')
            let formData = new FormData();

            // Append files to formData to prepare to send
            for(let i = 0; i < this.files.length; i++) {
                let currPDF = this.files[i]
                console.log(currPDF)
                formData.append('pdf[' + i + ']', currPDF)

            }
            
            // Make post request to upload files to django server
            axios.post('http://127.0.0.1:8000/extractor/parse-pdfs/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                }
            ).then(function(response) {
                console.log(response.data)
                console.log('SUCCESS!!');
            }).catch(function(){
                console.log('FAILURE!!');
            });
        }
    }
};
</script>

<style>
#uploadSubmitBtn {
}
</style>
  
  