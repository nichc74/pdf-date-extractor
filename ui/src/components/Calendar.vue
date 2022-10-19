<template>
  <div id="calendarContainer">
      <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
      >
          <v-card min-width="200px">
              {{ selectedEvent.name }}
              <v-card-text>
                  {{selectedEvent.snippet}}
              </v-card-text>
          </v-card>
      </v-menu>
      <b-button
        id="todayBttn"
        type="is-primary"
        outlined
        v-on:click="setToday"
      >
        Today
      </b-button>
      <b-button type="is-primary" v-on:click="prev">PREV</b-button>
      <b-button type="is-primary" v-on:click="next">NEXT</b-button>
      {{displayMonthYear}}
      <v-calendar
          ref="calendar"
          :events="otherEvents"
          @click:event="showEvent"
          v-model="focus"
          :type="type"
          now="2022-10-17"
      ></v-calendar>
  </div>
</template>

<script>
export default {
  name: 'EventCalendar',
  props: {
    otherEvents: Array
  },
  data: () => {
    return {
      today: new Date().toISOString().substring(0, 10),
      focus: '',
      // defaults to month
      type: "month",
      selectedOpen: false,
      selectedElement: undefined,
      selectedEvent: {},
      displayMonthYear: '',
      events: [
        {
          name: 'Some Event 1',
          start: '2022-10-17',
          color: "green",
          snippet: "Some test snippet"
        },
        {
          name: 'Some Event 2',
          start: '2022-10-01',
          end: '2022-10-02',
          color: "green",
          snippet: "Some snippet"
        },
        {
          name: 'Some Event 3',
          start: '2022-10-15',
          end: '2022-10-10',
          color: "green",
          snippet: "Some snippet"
        },
      ],
    };
  },
  mounted () {
    this.$refs.calendar.checkChange()
    this.displayMonthYear = this.$refs.calendar.title
  },
  methods: {
      showEvent({ nativeEvent, event }) {
        const open = () => {
            this.selectedEvent = event;
            this.selectedElement = nativeEvent.target;
            requestAnimationFrame(() =>
                requestAnimationFrame(
                    () => (this.selectedOpen = true)
                )
            );
        };
        if (this.selectedOpen) {
            this.selectedOpen = false;
            requestAnimationFrame(() =>
            requestAnimationFrame(() => open())
            );
        } else {
            open();
        }
        nativeEvent.stopPropagation();
    },
    setToday () {
      this.focus = ''
      this.displayMonthYear = this.$refs.calendar.title
    },
    prev () {
      this.$refs.calendar.prev()
      this.displayMonthYear = this.$refs.calendar.title
    },
    next () {
      this.$refs.calendar.next()
      this.displayMonthYear = this.$refs.calendar.title
    },
  }
};
</script>

<style>
#calendarContainer {
  height: 800px;
  width: 75%;
  display: flex;
  margin-left: 12.5%;
  margin-right: 12.5%;
  margin-top: 5%;
}
</style>

