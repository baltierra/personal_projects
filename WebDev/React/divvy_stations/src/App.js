import React from "react";
import NavBar from "./NavBar";
import StationList from "./StationList";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedStationIdentifier: null,
      stations: [],
    };
  }

  loadAllStations = async (e) => {
    const httpResponse = await fetch(
      "https://gbfs.divvybikes.com/gbfs/en/station_information.json"
    );
    const stationList = await httpResponse.json();

    //#7: Sort the list alphabetically
    const sortFunction = (a, b) => {
      const nameA = a.name.toUpperCase();
      const nameB = b.name.toUpperCase();

      if (nameA < nameB) {
        return -1;
      }

      if (nameA > nameB) {
        return 1;
      } else {
        return 0;
      }
    };

    const sortedStationList = stationList.data.stations.sort(sortFunction);

    //#1: Display the list of stations
    this.setState({ stations: sortedStationList });
  };

  //#2: Display the list of stations when the page initially loads
  componentDidMount() {
    this.loadAllStations();
  }

  findNearestStation = async (e) => {
    navigator.geolocation.getCurrentPosition((gps) => {
      if (this.state.stations.length > 0) {
        let nearestStation = this.state.stations[0];
        let nearestDistance = 10000000;
        this.state.stations.forEach((station) => {
          const distance = Math.sqrt(
            (station.lat - gps.coords.latitude) ** 2 +
              (station.lon - gps.coords.longitude) ** 2
          );
          if (distance < nearestDistance) {
            nearestDistance = distance;
            nearestStation = station;
          }
        });
        //#6: Display the nearest station as the only station in the station list
        this.setState({ stations: [nearestStation] });
      }
    });
  };

  render() {
    return (
      <div className="container-fluid p-0">
        <NavBar
          onClickLoadAll={this.loadAllStations}
          onClickNearest={this.findNearestStation}
        />
        <StationList stations={this.state.stations} />
      </div>
    );
  }
}

export default App;
