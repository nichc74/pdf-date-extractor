import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.config.productionTip = false
Vue.use(Buefy)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
