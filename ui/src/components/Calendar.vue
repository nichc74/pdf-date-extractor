<template>
  <div id="calendarContainer">
    <v-menu
      v-model="selectedOpen"
      :close-on-content-click="false"
      :activator="selectedElement"
      offset-x
    >
    <v-card class="eventCardContainer" min-width="200px">
      <div class="cardHeader">
        {{ selectedEvent.name }}
      </div>
      <div class="eventSnippet">
        {{selectedEvent.snippet}}
      </div>
      <b-button type="is-primary" v-on:click="previewPdfHandler(selectedEvent.path)">Preview PDF</b-button>
    </v-card>
    </v-menu>
    <div class="wrapper">
      <div class="calendarHeader">
        <b-button
          class="todayBttn"
          type="is-primary"
          outlined
          v-on:click="setToday"
        >
          Today
        </b-button>
        <b-button class="prevBttn" type="is-primary" v-on:click="prev">PREV</b-button>
        <b-button type="is-primary" v-on:click="next">NEXT</b-button>
      </div>
      <!-- This is gross but leaving here for sake of MVP -->
      <div class="monthYearHeader">
        <div v-if="$refs.calendar">
          {{ $refs.calendar.title }}
        </div>
        <div v-else>
          {{displayMonthYear}}
        </div>
      </div>
      <v-calendar
        ref="calendar"
        :events="otherEvents"
        @click:event="showEvent"
        v-model="focus"
        :type="type"
        now="2022-10-17"
      ></v-calendar>
    </div>
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
      type: "month",
      focus: '',
      selectedOpen: false,
      selectedElement: undefined,
      selectedEvent: {},
      displayMonthYear: '',
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
    previewPdfHandler(filePath) {
      window.open(filePath, '_blank');
    },
    setToday () {
      this.focus = ''
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
  }
};
</script>

<style>
.todayBttn, .prevBttn {
  margin-right: 8px;
}

.monthYearHeader {
  font-weight: bold;
  font-size: 32px;
}

.calendarHeader {
  justify-content: flex-start;
  margin-bottom: 8px;
}

.eventCardContainer {
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.eventSnippet {
  margin: 8px 0px;
}

.cardHeader {
  font-weight: bold;
  color: #2f5a89
}

.wrapper {
  height: 800px;
  width: 75%;
  display: flex;
  margin-left: 12.5%;
  margin-right: 12.5%;
  margin-top: 5%;
  display: flex;
  flex-direction: column;
}
</style>

