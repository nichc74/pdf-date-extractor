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
      <v-calendar
          :events="events"
          @click:event="showEvent"
          v-model="focus"
          :type="type"
          now="2022-10-17"
      ></v-calendar>
  </div>
</template>

<script>
export default {
  name: 'CodingBeautyCalendar',
  data: () => {
    return {
      today: new Date().toISOString().substring(0, 10),
      focus: '',
      // defaults to month
      type: "month",
      selectedOpen: false,
      selectedElement: undefined,
      selectedEvent: {},
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

