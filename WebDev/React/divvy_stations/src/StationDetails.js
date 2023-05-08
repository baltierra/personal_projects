import React from "react";

class StationDetails extends React.Component {
  constructor(props) {
    super(props);
  }

  render = () => {
    if (this.props.details) {
      //#5: Display the actual details of the selected station instead
      //of the placeholder text you see below.
      return (
        <div className="border shadow p-5 text-center">
          <h3>{this.props.name || "My Station"}</h3>
          <p>
            <span className="badge bg-primary rounded-pill">
              {this.props.details.num_bikes_available}
            </span>
            <span className="ps-4">
              {`Bikes Available: ${this.props.details.num_bikes_available}`}
            </span>
          </p>
          <p>
            <span className="badge bg-primary rounded-pill">
              {this.props.details.num_ebikes_available}
            </span>
            <span className="ps-4">
              {`E-Bikes Available: ${this.props.details.num_ebikes_available}`}
            </span>
          </p>
        </div>
      );
    } else {
      return <div className="col-sm-4"></div>;
    }
  };
}

export default StationDetails;
